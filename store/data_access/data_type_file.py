import json

from store.models.car import Car
from store.models.user import User

class FileData:
    def __init__(self):
        self.load_from_json()

    def load_from_file(self):

        file_user = open("File _Json/File_User.json", "r")
        file_admin = open("File _Json/File_Admin.json", "r")
        file_Car = open("File _Json/File_Car.json", "r")

        users_info = json.loads(file_user.read())
        admins_info = json.loads(file_admin.read())
        cars_info = json.loads(file_Car.read())
        print(f"i am in load from json{users_info}")

        for i in users_info:
            dict_list = dict(i).values()
            list_of_user.append(list(dict_list))
        for i in admins_info:
            dict_list = dict(i).values()
            list_of_admin.append(list(dict_list))
        for i in cars_info:
            dict_list = dict(i).values()
            list_of_car.append(list(dict_list))

        for i in list_of_user:
            user = User(username=i[0], email_address=i[1], password=i[2], type_user=i[3])
            self.list_of_user.append(user)

        for i in list_of_admin:
            admin = User(username=i[0], email_address=i[1], password=i[2], type_user=i[3])
            self.list_of_admin.append(admin)

        for i in list_of_car:
            car = Car(name=i[0], price=i[1], maker=i[2], color=i[3], year=i[4], description=i[5], img_url=i[6])
            self.list_of_car.append(car)

    def write_to_file(self):

        print(f"i am in write to json{[ob.__dict__ for ob in self.list_of_user]}")

        file_user = open("File _Json/File_User.json", "w")
        file_admin = open("File _Json/File_Admin.json", "w")
        file_Car = open("File _Json/File_Car.json", "w")

        file_user.write(json.dumps([ob.__dict__ for ob in self.list_of_user]))
        file_admin.write(json.dumps([ob.__dict__ for ob in self.list_of_admin]))
        file_Car.write(json.dumps([ob.__dict__ for ob in self.list_of_car]))

        file_user.close()
        file_admin.close()
        file_Car.close()

