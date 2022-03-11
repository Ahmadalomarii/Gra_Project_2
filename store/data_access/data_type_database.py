#from flask_sqlalchemy import SQLAlchemy
from store.models.user import User
from store.models.car import Car
from configparser import ConfigParser
import itertools

import sqlite3
from store.config import config


conf = config()



class DataBase:

    def __init__(self):
        self.database = rf"{conf.get_location_for_database_location()}"

    def add_car(self, car):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()
            cur.execute("INSERT INTO car(id,name,price,maker,color,year,description,img_url,reserved) "
                        "VALUES(?,?,?,?,?,?,?,?,?)",
                        (car.id, car.name, car.price, car.maker, car.color, car.year, car.description, car.img_url, ""))
            cur.fetchall()
            cur.connection.commit()
            conn.close()

        except Exception as inst:
            print(f"Error in add_car {inst}")

    def reserve_car(self, id_car, name_of_user):
        try:

            conn = sqlite3.connect(self.database)
            cur = conn.cursor()

            result = cur.execute(
                "SELECT reserved FROM car WHERE id = ? ", (id_car,))
            row = cur.fetchone()

            if row[0] == "":
                cur.execute("UPDATE car SET reserved =? WHERE id = ?", (name_of_user, id_car))
                row = cur.fetchall()

                cur.connection.commit()
                conn.close()
                print(f"reserve_car {row}")
                return True
            else:
                return False



        except Exception as inst:
            print("Error in reserve_car {inst}")

    def unreserve_car(self, id_car):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()

            result = cur.execute(
                "SELECT reserved FROM car WHERE id = ? ", (id_car,))
            row = cur.fetchone()
            if row[0] != "":
                cur.execute("UPDATE car SET reserved =? WHERE id=?", ("", id_car))
                row = cur.fetchall()

                cur.connection.commit()
                conn.close()
                return True
            else:
                return False



        except Exception as inst:
            print(f"Error in unreserve_car{inst}")

    def add_user(self, user):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()

            user_type = user.type_user
            if user_type == "Admin":
                cur.execute("INSERT INTO admin(id,username,email_address,password_hash) VALUES(?,?,?,?)",
                            (user.id, user.username, user.email_address, user.password))
                cur.fetchall()
            elif user_type == "User":
                cur.execute("INSERT INTO user(id,username,email_address,password_hash,budget) VALUES(?,?,?,?,?)",
                            (user.id, user.username, user.email_address, user.password, 000))
                cur.fetchall()

            cur.connection.commit()
            conn.close()

        except Exception as inst:
            print(f"Error in add_user {inst}")

    def log_in(self, user_or_admin, username, password):
        try:

            if (user_or_admin == "Admin"):
                conn = sqlite3.connect(self.database)
                cur = conn.cursor()

                result = cur.execute(
                    "SELECT username FROM admin WHERE username = ? AND password_hash=? ", (username, password))
                row = cur.fetchone()
                if row:
                    #print(f"login admin {row}")
                    return True



            elif (user_or_admin == "User"):

                conn = sqlite3.connect(self.database)
                cur = conn.cursor()

                result = cur.execute(
                    "SELECT username FROM user WHERE username = ? AND password_hash=? ", (username, password))

                row = cur.fetchone()
                if row:
                    #print(f"login user {row}")
                    return True

            return False

        except Exception as inst:
            print(f"Error in log_in {inst}")

    def get_car_by_name(self, name_of_car):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()

            result = cur.execute(
                f"SELECT * FROM car WHERE name =? ", (name_of_car,))
            row = cur.fetchall()
            if row:
                car = Car(row[0][0], row[0][1], row[0][2], row[0][3], row[0][4], row[0][5], row[0][6], row[0][7])
                car.reserve = row[0][8]
                return car

        except Exception as inst:
            print(f"Error in get_car_by_name {inst}")

    def get_all_car(self):
        try:
            list_of_car = []
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()

            result = cur.execute(f"SELECT * FROM car")
            rows = cur.fetchall()

            for i in rows:
                cars = Car(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])

                cars.reserve = i[8]
                list_of_car.append(cars)

            cur.connection.commit()
            conn.close()

            return list_of_car

        except Exception as inst:
            print(f"Error in get_all_car {inst}")

    def get_user_by_id(self, user_id):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()

            result = cur.execute("SELECT * FROM user WHERE id =?", (user_id,))
            row = cur.fetchall()
            if row:
                attem_user = User(row[0][0], row[0][1], row[0][2], row[0][3], "User")
                return attem_user




        except Exception as inst:
            print(f"Error in get_user_by_id {inst}")

    def get_user_by_name(self, user_name):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()

            result = cur.execute("SELECT * FROM user WHERE username = ? ", (user_name,))
            row = cur.fetchall()
            if row:
                attem_user = User(row[0][0], row[0][1], row[0][2], row[0][3], "User")
                return attem_user

        except Exception as inst:
            print(f"Error in get_user_by_name {inst}")
