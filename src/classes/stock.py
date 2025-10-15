from src.classes.object import Object

class Stock():

    def __init__(self):
        self.inventory = []
    
    def addObject(self,type,name):
        self.inventory.append(Object(type,name))
    
    def getStock(self):
        return [i for i in self.inventory]