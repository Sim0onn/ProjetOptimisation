from src.classes.warehouse import Warehouse
from src.classes.customer import Customer

class City():
    def __init__(self,name):
        self.name = name
        self.warehouses = []
        self.customers = []
    
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
    
    def addCustomer(self,customer):
        self.customers.append(customer)
    
    def createCustomer(self):
        self.customers.append(Customer())

    def returnCustomer(self):
        for customer in self.customers:
            return customer.getStock()
        
    def numberOfWarehouses(self):
        return len(self.warehouses)
