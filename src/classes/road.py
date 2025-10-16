from src.classes.city import City

class Road():
    def __init__(self, start_city: City, end_city: City, distance: float):
        self.start_city = start_city
        self.end_city = end_city
        self.distance = round(distance)

    def getStartCity(self):
        return self.start_city
    
    def getEndCity(self):
        return self.end_city

    def getDistance(self):
        return self.distance    
    
    def addDistance(self, distance):
        self.distance += distance
