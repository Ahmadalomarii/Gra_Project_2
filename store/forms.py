from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField,IntegerField,SelectField,FileField,RadioField,FloatField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Length,EqualTo,Email,DataRequired


class RegisterForm(FlaskForm):

    username = StringField(label='User Name :', validators=[Length(min=2,max=30),DataRequired()])
    email_address = StringField(label='Email Address:',validators=[Email(),DataRequired()])
    password1 = PasswordField(label='password:', validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm password:',validators=[EqualTo('password1'),DataRequired()])

    submit = SubmitField(label='Create Account ')

class RegisterStoreForm(FlaskForm):

    name = StringField(label='User Name :', validators=[Length(min=2,max=30),DataRequired()])
    phone = StringField(label='Email Address:',validators=[DataRequired()])
    image= FileField("image", validators=[FileRequired(),FileAllowed(['jpg','jpeg','png'])])
    CITIES= [('1', 'IRBID'), ('2', 'AMMAN'), ('3', 'AJLON')]
    location = SelectField(u'Location', choices=CITIES)
    password1 = PasswordField(label='password:', validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm password:',validators=[EqualTo('password1'),DataRequired()])

    submit = SubmitField(label='Create Account ')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = StringField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class LoginFormStore(FlaskForm):
    phone = StringField(label='Phone', validators=[DataRequired()])
    password = StringField(label='Password:', validators=[DataRequired()])
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

class ClothesForm(FlaskForm):
    name = StringField(label="Name : ",validators=[Length(min=2,max=30),DataRequired()])
    SIZES = [('1', 'XXS'), ('2', 'XS'), ('3', 'S'), ('4', 'M'), ('5', 'L'), ('6', 'XL'), ('7', 'XXL')]
    size=SelectField(label="Size :", choices=SIZES, validators=[DataRequired()])
    color=StringField(label="Color : ",validators=[Length(min=2,max=30),DataRequired()])
    description=StringField(label="Description : ",validators=[Length(min=2,max=100),DataRequired()])
    price=FloatField(label="Price", validators=[DataRequired()])
    image = FileField("image", validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png']),DataRequired()])
    TYPES = [('1', 'Hat'), ('2', 'Jacket'), ('3', 'Pants'), ('4', 'Shirt'), ('5', 'Shose'), ('6', 'Sweater'), ('7', 'T-Shirt'), ('7', 'Womens Drees ')]
    type=SelectField(label="Type :", choices=TYPES, validators=[DataRequired()])
    GENDER= [('1', "Men's  "), ('2', "Women's"), ('3', 'Children-Male'), ('4', 'Children-Female  ')]
    gender=RadioField(label="Gender", choices=GENDER, validators=[DataRequired()])
    submit = SubmitField(label='Add New Clothes')
class ReserveCar(FlaskForm):
    submit = SubmitField(label='Reserve Car')

class UnReserveCar(FlaskForm):
    submit = SubmitField(label='UnReserve Car')

class ReservedCar(FlaskForm):
    submit = SubmitField(label='Reserved ')

