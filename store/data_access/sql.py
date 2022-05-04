from store.models import User,Store
from store.models.car import Car

from . import mysql, app




class DataBaseSQL:

    def __init__(self):
        pass

    def log_in(self, user_or_store, email, password):
        try:
            if (user_or_store == "user"):
                with app.app_context():
                    cursor = mysql.connection.cursor()
                    cursor.execute("SELECT * FROM user WHERE email =%s AND password =%s ", (email, password))
                    result=cursor.fetchall()
                    mysql.connection.commit()
                    cursor.close()
                    if result:
                        return True

                    return False



            elif (user_or_store == "store"):
                with app.app_context():
                    cursor = mysql.connection.cursor()
                    cursor.execute("SELECT * FROM store WHERE phone =%s AND password =%s ", (email, password))
                    result = cursor.fetchall()
                    mysql.connection.commit()
                    cursor.close()
                    if result:
                        store = Store(id=result[0][0], name=result[0][1], phone=result[0][2], rating=result[0][3]
                                      , rating_count=result[0][4], image=result[0][5], location=result[0][6],
                                      password=result[0][7])
                        return store

                    return False
        except Exception as inst:
            print(f"Error in add_car {inst}")

    # add clothes to store
    def add_clothes(self, car):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                v1 = cursor.execute("SELECT * FROM `user`")
                v = mysql.connection.commit()
                cursor.close()
                print(f"Done!{v1}! ")




        except Exception as inst:
            print(f"Error in add_car {inst}")

    # reserve clothes from spacif store
    def reserve_clothes(self, id_car, name_of_user):
        try:

            with app.app_context():
                cursor = mysql.connection.cursor()
                v1 = cursor.execute("SELECT * FROM `user`")
                v = mysql.connection.commit()
                cursor.close()
                print(f"Done!{v1}! ")



        except Exception as inst:
            print("Error in reserve_car {inst}")

    # unreserve clothes
    def unreserve_clothes(self, id_car):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                v1 = cursor.execute("SELECT * FROM `user`")
                v = mysql.connection.commit()
                cursor.close()
                print(f"Done!{v1}! ")



        except Exception as inst:
            print(f"Error in unreserve_car{inst}")

    # register a new user in store
    def add_user(self, user):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO user(name,email,password) VALUES(%s,%s,%s)",
                            (user.name, user.email, user.password))
                mysql.connection.commit()
                result = cursor.fetchall()
                cursor.close()

        except Exception as inst:
            print(f"Error in add_user {inst}")


    # add a new store in our system
    def add_store(self, store):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                print(f"******************{type(store.image)}")
                cursor.execute("INSERT INTO store(name,phone,rating,rating_count,image,location,password) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                               (store.name, store.phone,store.rating,store.rating_count,store.image,store.location, store.password))
                mysql.connection.commit()
                result = cursor.fetchall()
                cursor.close()

        except Exception as inst:
            print(f"Error in add_store {inst}")



    def get_clothes_by_id(self, id_of_car):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                v1 = cursor.execute("SELECT * FROM `user`")
                v = mysql.connection.commit()
                cursor.close()
                print(f"Done!{v1}! ")

        except Exception as inst:
            print(f"Error in add_user {inst}")

    def get_all_clothes(self):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                v1 = cursor.execute("SELECT * FROM `user`")
                v = mysql.connection.commit()
                cursor.close()
                print(f"Done!{v1}! ")

        except Exception as inst:
            print(f"Error in add_user {inst}")

    def get_user_by_email(self, email):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM user WHERE email =%s", (email,))
                result =cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
                if result:
                    attemp_user = User(name=result[0][0], id=result[0][1], email=result[0][2], password=result[0][3])
                    return attemp_user
                return None

        except Exception as inst:
            print(f"Error in get_user_by_email {inst}")
            return 1

    def get_user_by_id(self, id):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM user WHERE id =%s", (id,))
                result=cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
                if result:
                    attemp_user = User(name=result[0][0],id= result[0][1],email= result[0][2],password= result[0][3])
                    return attemp_user
                return None
        except Exception as inst:
            print(f"Error in get_user_by_id {inst}")
            return 1

    def get_store_by_phone(self,phone_of_store):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM store WHERE phone =%s", (phone_of_store,))
                result =cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
                if result:
                    store = Store(id=result[0][0], name=result[0][1], phone=result[0][2], rating=result[0][3]
                                  ,rating_count=result[0][4],image=result[0][5],location=result[0][6],password=result[0][7])
                    return store
                return None

        except Exception as inst:
            print(f"Error in get_store_by_phone {inst}")
            return 1



def get_user_by_name(self, user_name):
    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            v1 = cursor.execute("SELECT * FROM `user`")
            v = mysql.connection.commit()
            cursor.close()
            print(f"Done!{v1}! ")

    except Exception as inst:
        print(f"Error in add_user {inst}")
