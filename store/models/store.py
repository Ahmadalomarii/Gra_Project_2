
class Store:
    id=0
    name = None
    phone=None
    rating= None
    rating_count= None
    image=None
    location=None
    password=None
    longitude=None
    latitude=None


    def __init__(self,id,name,phone,rating,rating_count,image,location,password,longitude,latitude):
        self.id = id
        self.name = name
        self.phone = phone
        self.rating = rating
        self.rating_count = rating_count
        self.image =image
        self.location=self.set_location(location)
        self.password = password
        self.longitude = longitude
        self.latitude=latitude

    def set_location(self, location):
        try:
            location = int(location)
            if location == 1:
                return "IRBID"
            elif location == 2:
                return "AMMAN"
            elif location == 3:
                return "ALJLON"
            else:
                print("error in class Store Line 43 in set_location")
                return "ERROR"
        except Exception as a:
            print(f"error in class Store Line 43 in set_location {a}")
            return location