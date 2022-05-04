
class Store:
    id=0
    name = None
    phone=None
    rating= None
    rating_count= None
    image=None
    location=None
    password=None


    def __init__(self,id,name,phone,rating,rating_count,image,location,password):
        self.id = id
        self.name = name
        self.phone = phone
        self.rating = rating
        self.rating_count = rating_count

        self.image =image
        print(f"///////////{type(image)}  {type(self.image)} {image} {type(image)}")

        self.location=location
        self.password = password