from src.classes.warehouse import Warehouse

class City():
    def __init__(self,name):
        self.name = name
        self.warehouses = []

    def addWarehouse(self,warehouse):
        self.warehouses.append(warehouse)

    def printWarehouse(self):
        for ware in self.warehouses:
            print(ware.getStock())
    
    def numberOfWarehouses(self):
        return len(self.warehouses)