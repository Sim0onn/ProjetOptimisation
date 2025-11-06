from src.classes.object import Object


class Customer(): 
    def __init__(self,name):
        self.name = name
        self.objects = []
    
    def getWishlist(self):
        return self.objects
    
    def printWishlist(self):
        for obj in self.objects:
            print(f"{obj.type} : {obj.name}")
    
    def addObject(self,type,name):
        self.objects.append(Object(type,name))
    
    def getObject(self,type,name):
        for obj in self.objects:
            if obj.type == type and obj.name == name:
                return obj
        return None