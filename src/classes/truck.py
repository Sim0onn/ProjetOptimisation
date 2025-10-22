from src.classes.stock import Stock
from src.classes.object import Object

class Truck():
    
    def __init__(self):
        self.stock = []

    def getStock(self):
        return self.stock

    def addObject(self,type,name):
        self.stock.append(Object(type,name))
