from configparser import ConfigParser

class config:
    def __init__(self):
        self.file = 'store/store.conf'
        self.confi = ConfigParser()
        self.confi.read(self.file)

    def get_location_for_database_location(self):
        return self.confi['store']['location_database_file']


