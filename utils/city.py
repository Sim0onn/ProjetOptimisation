from utils.warehouse import Warehouse

class City():
    def __init__(self,name):
        self.name = name
        self.warehouses = []

    def add_warehouse(self,warehouse):
        self.warehouses.append(warehouse)