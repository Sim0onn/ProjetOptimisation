from src.classes.stock import Stock

class Warehouse():

    def __init__(self):
        self.stock = Stock()
        
    def getStock(self):
        return self.stock.getStock()
    
    def setStock(self,stock):
        self.stock = stock
    
    def addObject(self,type,name):
        self.stock.addObject(type,name)
    