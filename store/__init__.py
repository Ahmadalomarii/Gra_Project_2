from flask import Flask,render_template
#from flask_sqlalchemy import SQLAlchemy


# from store.data_access.database import DataBase

from flask_login import LoginManager
from flask_mysqldb import MySQL

UPLOAD_FOLDER = 'C:/Users/AHMAD/Desktop/Task_4/store/static/uploads'

app =Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SECRET_KEY'] ='7ba926ebd4dfccd59b49e21d'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'store_clothes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


mysql = MySQL(app)
from store.data_access.sql import DataBaseSQL
db = DataBaseSQL()



login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from store import routes
