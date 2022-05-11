from store.models import User, Store, Clothes
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
                    result = cursor.fetchall()
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
    def add_clothes(self, new_clothes):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO clothes"
                               "(name,size,color,order_count,description,rating,rating_count,price,image,store_id,type,gender)"
                               " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                               (new_clothes.name, new_clothes.size, new_clothes.color, new_clothes.order_count,
                                new_clothes.description
                                , new_clothes.rating, new_clothes.rating_count, new_clothes.price, new_clothes.image,
                                new_clothes.store_id
                                , new_clothes.type, new_clothes.gender))
                mysql.connection.commit()
                result = cursor.fetchall()
                cursor.close()

        except Exception as inst:
            print(f"Error in add_clothes {inst}")

    def update_clothes(self, id_old_clothes, new_clothes):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "UPDATE  clothes SET name=%s,size=%s,color=%s,order_count=%s,description=%s,rating=%s,rating_count=%s,"
                    "price=%s,store_id=%s,type=%s,gender=%s WHERE id=%s"

                    , (new_clothes.name, new_clothes.size, new_clothes.color, new_clothes.order_count,
                       new_clothes.description
                       , new_clothes.rating, new_clothes.rating_count, new_clothes.price, new_clothes.store_id
                       , new_clothes.type, new_clothes.gender, id_old_clothes))

                mysql.connection.commit()
                result = cursor.fetchall()
                cursor.close()

        except Exception as inst:
            print(f"Error in update_clothes {inst}")

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
                cursor.execute(
                    "INSERT INTO store(name,phone,rating,rating_count,image,location,password) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (store.name, store.phone, store.rating, store.rating_count, store.image, store.location,
                     store.password))
                mysql.connection.commit()
                result = cursor.fetchall()
                cursor.close()

        except Exception as inst:
            print(f"Error in add_store {inst}")

    def get_clothes_by_id(self, id_of_clothes):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM `clothes` WHERE id =%s LIMIT 1", (id_of_clothes,))
                mysql.connection.commit()
                i = cursor.fetchone()

                clothes = Clothes(id=i[0], name=i[1], size=i[2], color=i[3], order_count=i[4], description=i[5],
                                  rating=i[6], rating_count=i[7], price=i[8], image=i[9], store_id=i[10],
                                  type=i[11], gender=i[12])

                cursor.close()
                return clothes

        except Exception as inst:
            print(f"Error in sql get_all_clothes {inst}")

    def get_all_clothes(self, store_id):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM `clothes` WHERE store_id =%s", (store_id,))
                mysql.connection.commit()
                result = cursor.fetchall()
                list_of_clothes = []
                for i in result:
                    clothes = Clothes(id=i[0], name=i[1], size=i[2], color=i[3], order_count=i[4], description=i[5],
                                      rating=i[6], rating_count=i[7], price=i[8], image=i[9], store_id=i[10],
                                      type=i[11], gender=i[12])
                    list_of_clothes.append(clothes)

                cursor.close()

                return list_of_clothes

        except Exception as inst:
            print(f"Error in sql get_all_clothes {inst}")

    def get_clothes_top_8_rating(self):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM `clothes` ORDER BY rating LIMIT 9")
                mysql.connection.commit()
                result = cursor.fetchall()
                list_of_clothes = []
                for i in result:
                    clothes = Clothes(id=i[0], name=i[1], size=i[2], color=i[3], order_count=i[4], description=i[5],
                                      rating=i[6], rating_count=i[7], price=i[8], image=i[9], store_id=i[10],
                                      type=i[11], gender=i[12])
                    list_of_clothes.append(clothes)

                cursor.close()

                return list_of_clothes

        except Exception as inst:
            print(f"Error in sql get_clothes_top_8_rating {inst}")

    def get_clothes_top_12_price(self):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM `clothes` ORDER BY price DESC LIMIT 12")
                mysql.connection.commit()
                result = cursor.fetchall()
                list_of_clothes = []
                for i in result:
                    clothes = Clothes(id=i[0], name=i[1], size=i[2], color=i[3], order_count=i[4], description=i[5],
                                      rating=i[6], rating_count=i[7], price=i[8], image=i[9], store_id=i[10],
                                      type=i[11], gender=i[12])
                    list_of_clothes.append(clothes)

                cursor.close()

                return list_of_clothes

        except Exception as inst:
            print(f"Error in sql get_clothes_top_12_price {inst}")

    def get_user_by_email(self, email):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM user WHERE email =%s", (email,))
                result = cursor.fetchall()
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
                result = cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
                if result:
                    attemp_user = User(name=result[0][0], id=result[0][1], email=result[0][2], password=result[0][3])
                    return attemp_user
                return None
        except Exception as inst:
            print(f"Error in get_user_by_id {inst}")
            return 1

    def get_store_by_phone(self, phone_of_store):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM store WHERE phone =%s", (phone_of_store,))
                result = cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
                if result:
                    store = Store(id=result[0][0], name=result[0][1], phone=result[0][2], rating=result[0][3]
                                  , rating_count=result[0][4], image=result[0][5], location=result[0][6],
                                  password=result[0][7])
                    return store
                return None


        except Exception as inst:
            print(f"Error in get_store_by_phone {inst}")
            return 1

    def get_store_by_id(self, id_of_store):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM store WHERE id =%s", (id_of_store,))
                result = cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
                if result:
                    store = Store(id=result[0][0], name=result[0][1], phone=result[0][2], rating=result[0][3]
                                  , rating_count=result[0][4], image=result[0][5], location=result[0][6],
                                  password=result[0][7])
                    return store
                return None


        except Exception as inst:
            print(f"Error in get_store_by_phone {inst}")
            return 1

    def get_store_name_by_clothes_id(self, clothes_id):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT store_id FROM clothes WHERE id =%s", (clothes_id,))
                result = cursor.fetchone()
                mysql.connection.commit()
                cursor.close()
                if result:
                    id_store = result[0]
                    store = self.get_store_by_id(id_store)

                    return store
                else:
                    print("Error in get_store_name_by_clothes_id")
                    return None


        except Exception as inst:
            print(f"Error in get_store_name_by_clothes_id {inst}")
            return 1

    def delete_clothes_by_id(self, id_clothes):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("DELETE FROM clothes WHERE id = %s", (id_clothes,))
                mysql.connection.commit()
                result = cursor.fetchall()

                cursor.close()

        except Exception as inst:
            print(f"Error in sql delete_clothes_by_id {inst}")

    def get_row_from_wishlist(self, id_clothes, id_user):
        try:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "SELECT * FROM wishlist WHERE id_clothes=%s AND id_user =%s",
                    (id_clothes, id_user))
                mysql.connection.commit()
                result = cursor.fetchall()
                cursor.close()
                return result

        except Exception as inst:
            print(f"Error in get_row_from_wishlist {inst}")

    def add_clothes_to_wishlist(self, id_clothes, id_user):
        try:
            result = self.get_row_from_wishlist(id_clothes, id_user)

            if len(result) == 0:
                with app.app_context():
                    cursor = mysql.connection.cursor()
                    cursor.execute(
                        "INSERT INTO wishlist(id_clothes,id_user) VALUES(%s,%s)",
                        (id_clothes, id_user))
                    mysql.connection.commit()
                    result = cursor.fetchall()
                    cursor.close()
                    return True

            else:
                return False

        except Exception as inst:
            print(f"Error in add_clothes_to_wishlist {inst}")
