from flask import Flask,render_template
#from flask_sqlalchemy import SQLAlchemy

from store.data_access.adapter import adapter_storage
from store.data_access.data_type_database import DataBase
from flask_login import LoginManager



app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SECRET_KEY'] ='7ba926ebd4dfccd59b49e21d'




db = adapter_storage()



login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from store import routes
