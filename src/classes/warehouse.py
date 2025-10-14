from src.classes.stock import Stock

class Warehouse():

    def __init__(self):
        self.stock = Stock()
        
    def addObject(self,type,name):
        self.stock.addObject(type,name)
    
    def getStock(self):
        return self.stock.inventory