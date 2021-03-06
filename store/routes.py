import json

from store import app
from flask import render_template, redirect, url_for, flash, request
from store.models import User, Store, Clothes

from store.forms import RegisterForm, RegisterStoreForm, LoginForm, LoginFormStore, ClothesForm, ClothesEditForm

from flask_login import login_user, logout_user, login_required, current_user

from store import login_manager
from store import db
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import MultiDict

import uuid


@login_manager.user_loader
def load_user(user_id):
    return db.get_user_by_id(int(user_id))


@app.route('/')
@app.route('/home')
def home_page():
    clothes_top_8_rating = db.get_clothes_top_8_rating()
    clothes_top_12_price = db.get_clothes_top_12_price()
    return render_template('home.html', clothes_top_8_rating=clothes_top_8_rating,
                           clothes_top_12_price=clothes_top_12_price)
@app.route('/categores')
def categores():
    clothes_13_categores = db.get_clothes_13_categores()
    return render_template('filter_categores_page.html',clothes_13_categores=clothes_13_categores)

@app.route('/stores')
def stores():
    stores = db.get_all_stores()
    return render_template('filter_stores_page.html',stores=stores)

clothes_with_filter=[]
@app.route('/clothes_with_store_filter/<string:id_store>')
def clothes_with_store_filter(id_store):
    global clothes_with_filter
    clothes_with_filter=db.get_all_clothes(id_store)
    return redirect(url_for("clothes_with_filter"))

@app.route('/clothes_with_categores_filter/<string:type>/<string:gender>')
def clothes_with_categores_filter(type,gender):
    global clothes_with_filter
    clothes_with_filter = db.get_clothes_by_categores(type,gender)
    return redirect(url_for("clothes_with_filter"))

@app.route("/clothes_with_filter")
def clothes_with_filter():
    global clothes_with_filter
    if clothes_with_filter:
        return render_template("filter_clothes_page.html",clothes_with_filter=clothes_with_filter)
    else:
        return redirect("home_page")


clothes_obj = None


@app.route('/clothes_inf_page/<string:id_clothes>')
def clothes_inf_page(id_clothes):
    global clothes_obj
    clothes = db.get_clothes_by_id(id_clothes)

    clothes_obj = clothes
    # return render_template('clothes_info.html',clothes=clothes,)
    return redirect(url_for('clothes_inf_page2'))


@app.route('/clothes_inf_page')
def clothes_inf_page2():
    global clothes_obj
    if clothes_obj:
        clothes = clothes_obj
        store = db.get_store_name_by_clothes_id(clothes.id)
        return render_template('clothes_info.html', clothes=clothes, store=store)
    else:
        return redirect(url_for('home_page'))



@app.route('/add_clothes_to_wishlist')
@login_required
def add_clothes_to_wishlist():
    global clothes_obj

    if clothes_obj:
        id = current_user.id
        result = db.add_clothes_to_wishlist(clothes_obj.id, id)
        if result:
            flash(f'Success! You are Add:{clothes_obj.name} To Your Wishlist', category='Success')
        else:
            flash(f'Fail! This Clothes Is In Your Wishlist :(  ', category='danger')
        return redirect(url_for('whishlist'))  ####whishlist page
    else:
        return redirect(url_for('home_page'))


def sort_list_gender(clothes):
    return clothes.gender


@app.route('/whishlist', methods=['GET', 'POST'])
@login_required
def whishlist():
    # clothes = db.get_all_clothes(11)
    clothes = db.get_clothes_in_wishlist(current_user.id)
    if clothes:
        clothes.sort(key=sort_list_gender)
        return render_template('whishlist.html', clothes=clothes)
    return render_template('whishlist.html')


@app.route('/store_delete_clothes_from_whishlist/<string:id_clothes>', methods=['GET', 'POST'])
def store_delete_clothes_from_whishlist(id_clothes):
    id_clothes = int(id_clothes)
    clothes = db.get_clothes_by_id(id_clothes)
    if clothes:
        id = current_user.id
        db.delete_clothes_by_id_from_whishlist(id_clothes, id)
        flash(f'Success! You are Delete Clothes {clothes.name} From Wishlist', category='Success')
        return redirect(url_for("whishlist"))
    else:
        flash("Erorr!Clothes Don't Delete From Wishlist", category='danager')
        return redirect(url_for("whishlist"))
    return redirect(url_for("whishlist"))

@app.route('/store_delete_clothes_from_whishlist_for_store/<string:id_clothes>/<string:id_user>', methods=['GET', 'POST'])
def store_delete_clothes_from_whishlist_for_store(id_clothes,id_user):
    id_clothes = int(id_clothes)
    id_user=int(id_user)
    clothes = db.get_clothes_by_id(id_clothes)
    if clothes:
        db.delete_clothes_by_id_from_whishlist(id_clothes, id_user)
        flash(f'Success! You are Delete Clothes {clothes.name} From Wishlist', category='Success')
        return redirect(url_for("store_reserved_clothes"))
    else:
        flash("Erorr!Clothes Don't Delete From Wishlist", category='danager')
        return redirect(url_for("whishlist"))
    return redirect(url_for("store_reserved_clothes"))


@app.route('/map', methods=['GET', 'POST'])
def map():
    # get ids of stores from wish list
    clothes = db.get_clothes_in_wishlist(current_user.id)
    if clothes:
        list_of_id = []
        for i in clothes:
            list_of_id.append(i.store_id)
        set_of_id = set(list_of_id)
        list_of_id = list(set_of_id)
    list_of_store = db.get_stores_from_list_of_id(list_of_id)
    # names_of_clothes=db.get_names_of_clothes_for_one_store_in_whishlist(current_user.id,store_id)
    data = []
    for store in list_of_store:
        item = {"description": "Store Name : " + store.name,
                "image": store.image,
                "location":"Clothes >> "+ db.get_names_of_clothes_for_one_store_in_whishlist(current_user.id, store.id),
                "latitude": store.latitude,
                "longitude": store.longitude
                }
        data.append(item)

    # data = [{
    #     "description": "Location A",
    #     "location": "G133",
    #     "latitude": "32.539019758856654",
    #     "longitude": "35.866449519956426"
    # },
    #     {
    #         "description": "{{name}}",
    #         "location": "MB320",
    #         "latitude": "51.065453",
    #         "longitude": "-114.088841"
    #     },
    #     {
    #         "description": "{{name}}",
    #         "location": "MB322",
    #         "latitude": "51.065453",
    #         "longitude": "-114.088600"
    #     }]

    json_data = json.dumps(data)
    return render_template('map.html', name="YYYYYYYYYYYYYYYYYYY", data=json_data)

@app.route('/map_for_all_store', methods=['GET', 'POST'])
def map_for_all_store():
    all_stores=db.get_all_stores()
    data = []
    for store in all_stores:
        item = {"description": "Store Name : " + store.name,
            "image": store.image,
            "location": "Location >> " + store.location,
            "latitude": store.latitude,
            "longitude": store.longitude
            }
        data.append(item)
    json_data = json.dumps(data)

    return render_template('map.html', name="YYYYYYYYYYYYYYYYYYY", data=json_data)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(id=88, name=form.username.data,
                              email=form.email_address.data,
                              password=form.password1.data, )
        db.add_user(user_to_create)
        return redirect(url_for('login_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/register_store', methods=['GET', 'POST'])
def register_store_page():
    form = RegisterStoreForm()

    if request.method == "POST":
        if form.validate_on_submit():
            # print(f"%$%$%$%$%$%${form.image.data.filename}()(){type(form.image.data)}")
            filename = secure_filename(str(uuid.uuid1()) + form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            store_to_create = Store(id=88, name=form.name.data,
                                    phone=form.phone.data,
                                    rating=1,
                                    rating_count=0,
                                    location=form.location.data,
                                    password=form.password1.data,
                                    image=filename,
                                    longitude=form.longitude.data,
                                    latitude=form.latitude.data)
            db.add_store(store_to_create)
        return redirect(url_for('login_store'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a store: {err_msg}', category='danger')

    return render_template('register_store.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        result_of_login_user = db.log_in("user", email=form.username.data, password=form.password.data)

        if result_of_login_user:
            login_user(db.get_user_by_email(form.username.data))
            flash(f'Success! You are logged in as :{form.username.data}', category='Success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danager')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


store_obj = None


@app.route('/store_login', methods=['GET', 'POST'])
def login_store():
    form = LoginFormStore()
    if form.validate_on_submit():
        result_of_login_store = db.log_in("store", email=form.phone.data, password=form.password.data)
        if result_of_login_store:
            flash(f'Success! You are logged in as :{result_of_login_store.name}', category='Success')
            global store_obj
            store_obj = result_of_login_store
            return redirect(url_for("store_base"))
        else:
            flash('phone and password are not match! Please try again', category='danager')

    return render_template('store_login.html', form=form)


@app.route('/store_base', methods=['GET', 'POST'])
def store_base():
    global store_obj
    if store_obj:
        return render_template('store_base.html', store=store_obj)
    else:
        return redirect(url_for("login_store"))


@app.route('/store_overview', methods=['GET', 'POST'])
def store_overview():
    global store_obj
    if store_obj:
        num_of_clothes_in_wishlist = len(db.get_reserved_clothes_from_wishlist_to_store(store_obj.id))
        data = []

        item = {"description": "Store Name : " + store_obj.name,
                "image": store_obj.image,
                "location": "Location >> " + store_obj.location,
                "latitude": store_obj.latitude,
                "longitude": store_obj.longitude
                }
        data.append(item)
        json_data = json.dumps(data)
        return render_template('store_overview.html', store_info=store_obj,data=json_data,num_of_clothes_in_wishlist=num_of_clothes_in_wishlist)
    else:
        flash('404-(rou)176', category='danager')
    return redirect(url_for('store_base', store=store_obj))


@app.route('/store_information/<string:store_id>', methods=['GET', 'POST'])
def store_information(store_id):
    global store_obj
    store_id = int(store_id)
    store_obj=db.get_store_by_id(store_id)
    if store_obj:
        return redirect(url_for('store_information2'))

    return redirect(url_for('clothes_inf_page2'))

@app.route('/store_information2', methods=['GET', 'POST'])
def store_information2():
    global store_obj
    if store_obj:
        num_of_clothes_in_wishlist = len(db.get_reserved_clothes_from_wishlist_to_store(store_obj.id))
        data = []

        item = {"description": "Store Name : " + store_obj.name,
                "image": store_obj.image,
                "location": "Location >> " + store_obj.location,
                "latitude": store_obj.latitude,
                "longitude": store_obj.longitude
                }
        data.append(item)
        json_data = json.dumps(data)
        return render_template('store_information.html', store_info=store_obj,data=json_data,num_of_clothes_in_wishlist=num_of_clothes_in_wishlist)
    else:
        flash('404-(rou)176', category='danager')
    return redirect(url_for('clothes_inf_page2'))

@app.route('/store_new_clothes', methods=['GET', 'POST'])
def store_new_clothes():
    global store_obj
    if store_obj:
        form = ClothesForm()
        if request.method == "POST":
            if form.validate_on_submit():
                filename = secure_filename(str(uuid.uuid1()) + form.image.data.filename)
                form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_clothes = Clothes(id=88, name=form.name.data, size=form.size.data, color=form.color.data,
                                      order_count=0, description=form.description.data, rating=1, rating_count=0,
                                      price=form.price.data, image=filename, store_id=store_obj.id, type=form.type.data,
                                      gender=form.gender.data)
                db.add_clothes(new_clothes)
                flash(f'Success! You are Add Clothes {new_clothes.name}', category='Success')
    else:
        flash('404-(rou)197', category='danager')
        return redirect(url_for('store_base', store=store_obj))

    return render_template('store_new_clothes.html', store_info=store_obj, form=form)


@app.route('/store_edit_clothes', methods=['GET', 'POST'])
def store_edit_clothes():
    global store_obj
    # form = ClothesForm(MultiDict([('name','AHMAd'),('color','RRRRRRRR')]))
    clothes = None
    if store_obj:
        clothes = db.get_all_clothes(store_obj.id)
        # if form.validate_on_submit():
        #     print(f"SSSSSSSSSSSSSSSSSSS {form.hidden_tag()}")

    else:
        return redirect(url_for("login_store"))

    return render_template('store_edit_clothes.html', store_info=store_obj, clothes=clothes)

@app.route('/store_reserved_clothes', methods=['GET', 'POST'])
def store_reserved_clothes():
    global store_obj
    clothes = None
    if store_obj:
        clothes = db.get_reserved_clothes_from_wishlist_to_store(store_obj.id)
        users=db.get_list_of_user_in_wishlist(clothes)

    else:
        return redirect(url_for("login_store"))

    return render_template('store_reserved_clothes.html', store_info=store_obj, clothes_users=zip(clothes,users))

@app.route('/store_popup_edit_clothes/<string:id_clothes>', methods=['GET', 'POST'])
def store_popup_edit_clothes(id_clothes):
    id_clothes = int(id_clothes)
    global store_obj
    form = ClothesEditForm()
    clothes = None
    if store_obj:
        clothes = db.get_clothes_by_id(id_clothes)
        all_clothes = db.get_all_clothes(store_obj.id)
        # form=ClothesEditForm(MultiDict([('name',clothes.name),('size',clothes.size),('color',clothes.color),('description',clothes.description),
        #                                 ('price',clothes.price),('type',clothes.type),('gender',clothes.gender),('submit',form.validate_on_submit())]))

        if request.method == "POST":
            if form.validate_on_submit():
                new_clothes = Clothes(id=88, name=form.name.data, size=form.size.data, color=form.color.data,
                                      order_count=0, description=form.description.data, rating=1, rating_count=0,
                                      price=form.price.data, image=None, store_id=store_obj.id, type=form.type.data,
                                      gender=form.gender.data)
                db.update_clothes(id_clothes, new_clothes)
                flash(f'Success! You are Update Clothes {new_clothes.name}', category='Success')
                return redirect(url_for("store_edit_clothes"))


    else:
        return redirect(url_for("login_store"))

    return render_template('popup_edit_clothes.html', store_info=store_obj, clothes=all_clothes, form=form)


@app.route('/store_delete_clothes/<string:id_clothes>', methods=['GET', 'POST'])
def store_delete_clothes(id_clothes):
    id_clothes = int(id_clothes)
    global store_obj
    if store_obj:
        clothes = db.get_clothes_by_id(id_clothes)
        if clothes:
            db.delete_clothes_by_id(id_clothes)
            flash(f'Success! You are Delete Clothes {clothes.name}', category='Success')
            return redirect(url_for("store_edit_clothes"))
    else:
        return redirect(url_for("login_store"))
    return redirect(url_for("store_edit_clothes"))
    # return render_template('popup_edit_clothes.html', store_info=store_obj,clothes=all_clothes,form=form)#oldddd


