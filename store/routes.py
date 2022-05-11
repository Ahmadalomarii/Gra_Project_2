from store import app
from flask import render_template, redirect, url_for, flash, request
from store.models import User, Store ,Clothes

from store.forms import RegisterForm, RegisterStoreForm, LoginForm, LoginFormStore, AddCarForm, ReserveCar, \
    UnReserveCar, ReservedCar,ClothesForm,ClothesEditForm

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
    return render_template('home.html')


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
            filename = secure_filename(str(uuid.uuid1())+form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            store_to_create = Store(id=88, name=form.name.data,
                                phone=form.phone.data,
                                rating=1,
                                rating_count=0,
                                location=form.location.data,
                                password=form.password1.data,
                                image=filename)
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

store_obj=None
@app.route('/store_login', methods=['GET', 'POST'])
def login_store():
    form = LoginFormStore()
    if form.validate_on_submit():
        result_of_login_store = db.log_in("store", email=form.phone.data, password=form.password.data)
        if result_of_login_store:
            flash(f'Success! You are logged in as :{result_of_login_store.name}', category='Success')
            global store_obj
            store_obj=result_of_login_store
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
       return render_template('store_overview.html',store_info=store_obj)
    else:
        flash('404-(rou)176', category='danager')
    return redirect(url_for('store_base', store=store_obj))


@app.route('/store_new_clothes', methods=['GET', 'POST'])
def store_new_clothes():
    global store_obj
    if store_obj:
        form=ClothesForm()
        if request.method == "POST":
            if form.validate_on_submit():
                filename = secure_filename(str(uuid.uuid1()) + form.image.data.filename)
                form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_clothes = Clothes(id=88,name=form.name.data,size=form.size.data,color=form.color.data,
                                      order_count=0,description=form.description.data,rating=1,rating_count=0,
                                      price=form.price.data,image=filename,store_id=store_obj.id,type=form.type.data,
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
    #form = ClothesForm(MultiDict([('name','AHMAd'),('color','RRRRRRRR')]))
    clothes=None
    if store_obj:
        clothes=db.get_all_clothes(store_obj.id)
        # if form.validate_on_submit():
        #     print(f"SSSSSSSSSSSSSSSSSSS {form.hidden_tag()}")

    else:
        return redirect(url_for("login_store"))

    return render_template('store_edit_clothes.html', store_info=store_obj,clothes=clothes)

@app.route('/store_popup_edit_clothes/<string:id_clothes>', methods=['GET', 'POST'])
def store_popup_edit_clothes(id_clothes):
    id_clothes = int(id_clothes)
    global store_obj
    form = ClothesEditForm()
    clothes=None
    if store_obj:
        clothes=db.get_clothes_by_id(id_clothes)
        all_clothes = db.get_all_clothes(store_obj.id)
        # form=ClothesEditForm(MultiDict([('name',clothes.name),('size',clothes.size),('color',clothes.color),('description',clothes.description),
        #                                 ('price',clothes.price),('type',clothes.type),('gender',clothes.gender),('submit',form.validate_on_submit())]))

        if request.method == "POST":
            if form.validate_on_submit():
                new_clothes = Clothes(id=88, name=form.name.data, size=form.size.data, color=form.color.data,
                                      order_count=0, description=form.description.data, rating=1, rating_count=0,
                                      price=form.price.data, image=None, store_id=store_obj.id, type=form.type.data,
                                      gender=form.gender.data)
                db.update_clothes(id_clothes,new_clothes)
                flash(f'Success! You are Update Clothes {new_clothes.name}', category='Success')
                return redirect(url_for("store_edit_clothes"))


    else:
        return redirect(url_for("login_store"))

    return render_template('popup_edit_clothes.html', store_info=store_obj,clothes=all_clothes,form=form)

@app.route('/store_delete_clothes/<string:id_clothes>', methods=['GET', 'POST'])
def store_delete_clothes(id_clothes):
    id_clothes = int(id_clothes)
    global store_obj
    if store_obj:
        clothes=db.get_clothes_by_id(id_clothes)
        if clothes:
            db.delete_clothes_by_id(id_clothes)
            flash(f'Success! You are Delete Clothes {clothes.name}', category='Success')
            return redirect(url_for("store_edit_clothes"))
    else:
        return redirect(url_for("login_store"))

    return render_template('popup_edit_clothes.html', store_info=store_obj,clothes=all_clothes,form=form)


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
