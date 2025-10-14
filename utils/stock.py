from utils.object import Object

class Stock():

    def __init__(self):
        self.stock = []
    
    def add_object(self,type,name):
        self.stock.append(Object(type,name))
    
    def print_stock(self):
        for i in self.stock:
            print("Type : ",i.type," Name : ",i.name)