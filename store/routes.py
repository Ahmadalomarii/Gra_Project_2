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


@login_required
@app.route('/add_clothes_to_wishlist')
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
    return redirect(url_for("store_edit_clothes"))


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


@app.route('/store', methods=['GET', 'POST'])
@login_required
def store_page():
    reserve_form = ReserveCar()
    unreserve_form = UnReserveCar()
    reserved_car = ReservedCar()

    if request.method == "POST":
        if reserve_form.validate_on_submit():
            name_of_car = request.form.get('reserve')
            car_object = db.get_car_by_name(name_of_car=name_of_car)

            if car_object:
                result_of_reserve = db.reserve_car(car_object.id, current_user.username)

                if result_of_reserve:
                    flash(f'Success! You are Reserve car:{car_object.name}', category='Success')
                    return redirect(url_for('store_page'))
                else:
                    flash(f'Fail! This Car Is Reserved ', category='danger')
                    return redirect(url_for('store_page'))

        # if unreserve_form.validate_on_submit():
        #     name_of_car = request.form.get('unreserve')
        #     car_object2 = db.get_car_by_name(name_of_car=name_of_car)
        #     if car_object2:
        #         result_of_unreserve = db.unreserve_car(car_object2.id)
        #         if result_of_unreserve:
        #
        #             return redirect(url_for('store_page'))

        if reserved_car.validate_on_submit():
            name_of_car = request.form.get('reserved')
            car_object3 = db.get_car_by_name(name_of_car=name_of_car)
            if car_object3:
                if car_object3.reserve != "" and car_object3.reserve != current_user.username:
                    flash(f'Fail! This Car Is Reserved ', category='danger')
                    return redirect(url_for('store_page'))

    cars = db.get_all_car()
    return render_template('store.html', items=cars, reserve_form=reserve_form, unreserve_form=unreserve_form,
                           reserved_car=reserved_car)


@app.route('/unreserve_car/<string:name_of_car>')
def unreserve(name_of_car):
    car_object2 = db.get_car_by_name(name_of_car=name_of_car)
    if car_object2:
        result_of_unreserve = db.unreserve_car(car_object2.id)
        if result_of_unreserve:
            return redirect(url_for('store_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(id=88, name=form.username.data,
                              email=form.email_address.data,
                              password=form.password1.data, )
        db.add_user(user_to_create)
        return redirect(url_for('store_page'))
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
            return redirect(url_for('store_page'))
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
        data = []

        item = {"description": "Store Name : " + store_obj.name,
                "image": store_obj.image,
                "location": "Location >> " + store_obj.location,
                "latitude": store_obj.latitude,
                "longitude": store_obj.longitude
                }
        data.append(item)
        json_data = json.dumps(data)
        return render_template('store_overview.html', store_info=store_obj,data=json_data)
    else:
        flash('404-(rou)176', category='danager')
    return redirect(url_for('store_base', store=store_obj))


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


@app.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
    form = AddCarForm()
    if form.validate_on_submit():
        car_to_create = Car(id=-1
                            , name=form.name.data,
                            price=form.price.data,
                            maker=form.maker.data,
                            color=form.color.data,
                            year=form.year.data,
                            description=form.description.data,
                            img_url=form.img_url.data)
        db.add_car(car_to_create)
        flash(f'Success! You are Add Car {car_to_create.name}', category='Success')
        return redirect(url_for('admin_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('store_page.html', form=form)
