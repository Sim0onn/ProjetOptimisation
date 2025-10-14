from src.classes.stock import Stock

class Warehouse():

    def __init__(self):
        self.stock = Stock()
        
    def add_object(self,type,name):
        self.stock.add_object(type,name)