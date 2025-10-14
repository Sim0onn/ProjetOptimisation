from src.classes.stock import Stock

class Truck():
    
    def __init__(self):
        self.stock = Stock()

    def addObject(self,type,name):
        self.stock.addObject(type,name)