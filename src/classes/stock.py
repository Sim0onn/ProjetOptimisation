from src.classes.object import Object

class Stock():

    def __init__(self):
        self.inventory = []
    
    def addObject(self,type,name):
        self.inventory.append(Object(type,name))
    
    def getStock(self):
        return [i for i in self.inventory]
    
    def getObject(self,type,name):
        for obj in self.inventory:
            if obj.type == type and obj.name == name:
                return True
        return None