import itertools
from flask_login import UserMixin

class User(UserMixin):
    id=0
    name = None
    email= None
    password= None


    def __init__(self,id,name,email,password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password



