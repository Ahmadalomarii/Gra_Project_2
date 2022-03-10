from configparser import ConfigParser


from store.data_access.dataaccess import DataAccess

file = 'store/store.conf'

config = ConfigParser()
config.read(file)

data_access =DataAccess(config['store']['data_type'])
#print(f"data type is {config['store']['data_type']}")
data_type = data_access.data





