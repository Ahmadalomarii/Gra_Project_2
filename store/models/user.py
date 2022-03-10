import itertools
from flask_login import UserMixin

class User(UserMixin):
    id_iter = itertools.count()
    username = None
    email_address = None
    password= None
    type_user = None

    def __init__(self,id,username,email_address,password,type_user):
        if id !=-1:
            self.id = id
        else:
            self.id =next(User.id_iter)
        self.username = username
        self.email_address = email_address
        self.password = password
        self.type_user = type_user


