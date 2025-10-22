from src.classes.object import Object
class Warehouse():

    def __init__(self):
        self.stock = []
        
    def getStock(self):
        return self.stock
    
    def printStock(self):
        for obj in self.stock:
            print(f"{obj.type} : {obj.name}")
    
    def addObject(self,type,name):
        self.stock.append(Object(type,name))
    
    def getObject(self,type,name):
        for obj in self.stock:
            if obj.type == type and obj.name == name:
                return obj
        return None