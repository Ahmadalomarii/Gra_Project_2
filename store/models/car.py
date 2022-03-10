import itertools

class Car :
    id_iter = itertools.count()
    name =None
    price =None
    maker = None
    color = None
    year = None
    description =None
    img_url = None
    reserve = ""

    def __init__(self,id,name,price,maker,color,year,description,img_url):
        if id !=-1:
            self.id = id
        else:
            self.id = next(Car.id_iter)

        self.name = name
        self.price = price
        self.maker =maker
        self.color =color
        self.year = year
        self.description = description
        self.img_url = img_url
        self.reserve = ""

