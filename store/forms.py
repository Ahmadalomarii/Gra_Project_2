from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField,IntegerField
from wtforms.validators import Length,EqualTo,Email,DataRequired


class RegisterForm(FlaskForm):

    username = StringField(label='User Name :', validators=[Length(min=2,max=30),DataRequired()])
    email_address = StringField(label='Email Address:',validators=[Email(),DataRequired()])
    password1 = PasswordField(label='password:', validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm password:',validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Create Account ')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class AddCarForm(FlaskForm):
    name = StringField(label="Name : ",validators=[Length(min=2,max=30),DataRequired()])
    price = IntegerField(label="Price :",validators=[DataRequired()])
    maker = StringField(label="Maker : ",validators=[Length(min=2,max=30),DataRequired()])
    color = StringField(label="Color : ",validators=[Length(min=2,max=30),DataRequired()])
    year = IntegerField(label="Year :",validators=[DataRequired()])
    img_url = StringField(label="Image url : ",validators=[Length(min=2,max=1024),DataRequired()])
    description = StringField(label="Maker : ",validators=[Length(min=2,max=1024),DataRequired()])
    submit = SubmitField(label='Add New Car')

class ReserveCar(FlaskForm):
    submit = SubmitField(label='Reserve Car')

class UnReserveCar(FlaskForm):
    submit = SubmitField(label='UnReserve Car')

class ReservedCar(FlaskForm):
    submit = SubmitField(label='Reserved ')

