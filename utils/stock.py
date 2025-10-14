class Stock():

    def __init__(self):
        self.stock = []
    
    def add_object(self,obj):
        self.stock.append(obj)
    
    def print_stock(self):
        for i in self.stock:
            print("Type : ",i.type," Name : ",i.name)