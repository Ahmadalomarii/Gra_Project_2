from store import app
from flask import render_template, redirect, url_for, flash, request
from store.models.user import User
from store.models.car import Car

from store.forms import RegisterForm, LoginForm, AddCarForm, ReserveCar, UnReserveCar,ReservedCar
from store import db
from flask_login import login_user, logout_user, login_required, current_user

from store import login_manager
from store import db


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
    reserved_car =ReservedCar()

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

        if reserved_car.validate_on_submit() :
            name_of_car = request.form.get('reserved')
            car_object3 = db.get_car_by_name(name_of_car=name_of_car)
            if car_object3:
                if car_object3.reserve !="" and car_object3.reserve !=current_user.username:
                    flash(f'Fail! This Car Is Reserved ', category='danger')
                    return redirect(url_for('store_page'))


    cars = db.get_all_car()
    return render_template('store.html', items=cars, reserve_form=reserve_form, unreserve_form=unreserve_form, reserved_car=reserved_car)

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
        user_to_create = User(id = -1,username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data,
                              type_user="User")
        db.add_user(user_to_create)
        return redirect(url_for('store_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        result_of_login_user = db.log_in("User", username=form.username.data, password=form.password.data)

        if result_of_login_user:
            login_user(db.get_user_by_name(form.username.data))
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


@app.route('/admin_login', methods=['GET', 'POST'])
def Login_Admin():
    form = LoginForm()
    if form.validate_on_submit():
        result_of_login_admin = db.log_in("Admin", username=form.username.data, password=form.password.data)
        if result_of_login_admin:
            flash(f'Success! You are logged in as :{form.username.data}', category='Success')
            return redirect(url_for('admin_page'))
        else:
            flash('Username and password are not match! Please try again', category='danager')

    return render_template('admin_login.html', form=form)


@app.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
    form = AddCarForm()
    if form.validate_on_submit():
        car_to_create = Car(id=-1
                            ,name=form.name.data,
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

    return render_template('admin_page.html', form=form)
