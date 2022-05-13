
class Clothes:
    id=None
    name=None
    size=None
    color=None
    order_count=None
    description=None
    rating=None
    rating_count=None
    price=None
    image=None
    store_id=None
    type=None
    gender=None

    def __init__(self,id,name,size,color,order_count,description,rating,rating_count,price,image,store_id,type,gender):
        self.id=id
        self.name=name
        self.size=self.set_size(size)
        self.color=color
        self.order_count=order_count
        self.description=description
        self.rating=rating
        self.rating_count=rating_count
        self.price=price
        self.image=image
        self.store_id=store_id
        self.type=self.set_type(type)
        self.gender=self.set_gender(gender)


    def set_size(self,size):
        try:
            size = int(size)
            if size == 1:
                return "XXS"
            elif size == 2:
                return "XS"
            elif size == 3:
                return "S"
            elif size == 4:
                return "M"
            elif size == 5:
                return "L"
            elif size == 6:
                return "XL"
            elif size == 7:
                return "XXL"
            else:
                print("error in class Clothes Line 49 in set size")
                return "ERROR"
        except Exception as a:
            return size



    def set_gender(self,gender):
        try:
            gender = int(gender)
            if gender == 1:
                return "Men's"
            elif gender == 2:
                return "Women's"
            elif gender == 3:
                return "Children-Male"
            elif gender == 4:
                return "Children-Female"
            else:
                print("error in class Clothes Line 62 in set_gender")
                return "ERROR"
        except Exception as a:
            return gender


    def set_type(self,type):
        try:
            type = int(type)
            if type == 1:
                return "Hat"
            elif type == 2:
                return "jacket"
            elif type == 3:
                return "Pants"
            elif type == 4:
                return "Shirt"
            elif type == 5:
                return "Shose"
            elif type == 6:
                return "Sweater"
            elif type == 7:
                return "T-Shirt"
            elif type == 8:
                return "Womens Dress"
            else:
                print("error in class Clothes Line 81 in set type")
                return "ERROR"
        except Exception as a:
            return type








