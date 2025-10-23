from src.classes.city import City

class Road():
    def __init__(self, city1: City, city2: City, distance: float):
        self.city1 = city1
        self.city2 = city2
        self.distance = round(distance)

    def getCity1(self):
        return self.city1
    
    def getCity2(self):
        return self.city2

    def getDistance(self):
        return self.distance    
    
    def addDistance(self, distance):
        self.distance += distance
