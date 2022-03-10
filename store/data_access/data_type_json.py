import json
from configparser import ConfigParser
from store.models.car import Car
from store.models.user import User
from store.models.car import Car


file = 'store/store.conf'
config = ConfigParser()
config.read(file)

class JsonData:

    def __init__(self):
        self.list_of_cars = []
        self.list_of_users = []
        self.list_of_admins = []
        self.load_car()
        self.load_user()
        self.load_admin()




    def load_car(self):
        list_of_car = []
        file_Car = open(config['store']['location_json_car_file'], "r")
        cars_info = json.loads(file_Car.read())
        for i in cars_info:
            dict_list = dict(i).values()
            list_of_car.append(list(dict_list))


        for i in list_of_car:
            car = Car(id=-1,name=i[1], price=i[2], maker=i[3], color=i[4], year=i[5], description=i[6], img_url=i[7])

            car.reserve =i[8]

            self.list_of_cars.append(car)

    def load_user(self):
        self.list_of_user = []
        file_user = open(config['store']['location_json_user_file'], "r")
        users_info = json.loads(file_user.read())
        for i in users_info:
            dict_list = dict(i).values()
            self.list_of_user.append(list(dict_list))

        for i in self.list_of_user:
            user = User(id = i[0],username=i[1], email_address=i[2], password=i[3], type_user=i[4])
            self.list_of_users.append(user)

    def load_admin(self):
        list_of_admin = []

        file_admin = open(config['store']['location_json_admin_file'], "r")
        admins_info = json.loads(file_admin.read())
        for i in admins_info:
            dict_list = dict(i).values()
            list_of_admin.append(list(dict_list))

        for i in list_of_admin:
            admin = User(id=i[0], username=i[1], email_address=i[2], password=i[3], type_user=i[4])
            self.list_of_admins.append(admin)


    def write_car(self):
        file_Car = open("C:\\Users\\AHMAD\\Desktop\\Task_4\\store\\data_access\\File _Json\\File_Car.json", "w")
        file_Car.write(json.dumps([ob.__dict__ for ob in self.list_of_cars]))
        file_Car.close()

    def write_user(self):
        file_user = open("C:\\Users\\AHMAD\\Desktop\\Task_4\\store\\data_access\\File _Json\\File_User.json", "w")

        file_user.write(json.dumps([ob.__dict__ for ob in self.list_of_users]))

        file_user.close()

    def write_admin(self):
        file_admin = open("C:\\Users\\AHMAD\\Desktop\\Task_4\\store\\data_access\\File _Json\\File_Admin.json", "w")
        file_admin.write(json.dumps([ob.__dict__ for ob in self.list_of_admins]))
        file_admin.close()




    def add_car(self, car):
        self.list_of_cars.append(car)
        self.write_car()

    def reserve_car(self, id_car, name_of_user):

        for i in self.list_of_cars:

            if i.id == id_car and i.reserve == "":
                i.reserve = name_of_user
                self.write_car()
                return True
        return False

    def unreserve_car(self, id_car):
        for i in self.list_of_cars:
            if i.id == id_car and i.reserve != "":
                i.reserve = ""
                self.write_car()
                return True
        return False

    def add_user(self, user):
        if user.type_user == "User":
            self.list_of_users.append(user)
            self.write_user()
            return True
        elif user.type_user == "Admin":
            self.list_of_admins.append(user)
            self.write_admin()
            return True
        return False

    def log_in(self, user_or_admin, username, password):

        if (user_or_admin == "Admin"):
            for i in self.list_of_admins:
                if (username == i.username and password == i.password):
                    return True

            return False
        elif (user_or_admin == "User"):
            for i in self.list_of_users:
                if (username == i.username and password == i.password):
                    return True

            return False

    def get_car_by_name(self, name_of_car):
        for i in self.list_of_cars:
            if i.name == name_of_car:
                return i
        return None

    def get_all_car(self):
        return self.list_of_cars

    def get_user_by_id(self, user_id):
        for i in self.list_of_users:
            if i.id == user_id:
                return i
        return None

    def get_user_by_name(self, user_name):
        for i in self.list_of_users:
            if i.username == user_name:
                return i
        return None



