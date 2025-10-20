from src.classes.warehouse import Warehouse
from src.classes.client import Client

class City():
    def __init__(self,name):
        self.name = name
        self.warehouses = []
        self.clients = []
    
    def getName(self):
        return self.name
    
    def setName(self,name):
        self.name = name

    def addWarehouse(self,warehouse):
        self.warehouses.append(warehouse)
    
    def createWarehouse(self):
        self.warehouses.append(Warehouse())

    def returnWarehouse(self):
        for ware in self.warehouses:
            return ware.getStock()
    
    def numberOfWarehouses(self):
        return len(self.warehouses)