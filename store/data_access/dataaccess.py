from store.data_access.data_type_database import DataBase
from store.data_access.data_type_file import FileData
from store.data_access.data_type_json import JsonData

class DataAccess():
    data = None


    def __init__(self,name_of_data_type):
        self.data = self.set_strategy(name_of_data_type)





    def set_strategy(self,name_of_data_type):
        if name_of_data_type == "FileData":
            return FileData()

        elif name_of_data_type == "DataBase":
            return DataBase()


        elif name_of_data_type =="JsonData":
            return JsonData()
