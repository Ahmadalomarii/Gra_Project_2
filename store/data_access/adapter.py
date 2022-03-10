from store.data_access import data_type



class adapter_storage:

    def add_car(self, car):
       return data_type.add_car(car)


    def reserve_car(self, id_car, name_of_user):

        return data_type.reserve_car(id_car, name_of_user)
    def unreserve_car(self, id_car):
        return data_type.unreserve_car( id_car)

    def add_user(self, user):
        return data_type.add_car(user)


    def log_in(self, user_or_admin, username, password):
        return data_type.log_in( user_or_admin, username, password)


    def get_car_by_name(self,name_of_car):
        return data_type.get_car_by_name(name_of_car)

    def get_all_car(self):
        #print(f"i am in get all cars {len(data_type.get_all_car())}")
        return data_type.get_all_car()

    def get_user_by_id(self,user_id):
        return data_type.get_user_by_id(user_id)

    def get_user_by_name(self,user_name):
        return data_type.get_user_by_name(user_name)