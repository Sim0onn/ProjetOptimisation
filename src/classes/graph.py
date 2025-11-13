from src.classes.city import City
from src.classes.road import Road

class Graph:

    def __init__(self):
        self.cities = {}
        self.roads = []

    def getCities(self):
        return self.cities

    def addCity(self, city_name: str):

        if city_name not in self.cities:
            self.cities[city_name] = City(city_name)
        else:
            print(f"La ville '{city_name}' existe déjà.")


    def addRoad(self, city_name1: str, city_name2: str, distance: float = 1.0):
        
        if city_name1 not in self.cities:
            self.addCity(city_name1)
        if city_name2 not in self.cities:
            self.addCity(city_name2)

        city_name1 = self.cities[city_name1]
        city_name2 = self.cities[city_name2]
        
        if not self.roadExists(city_name1, city_name2):
            road = Road(city_name1, city_name2, distance)
            self.roads.append(road)


    def roadExists(self, start_city: City, end_city: City) -> bool:
        for road in self.roads:
            if (road.getCity1() == start_city and
                road.getCity2() == end_city):
                return True
        return False


    def getCity(self, city_name: str):
        return self.cities.get(city_name, None)


    def getRoadsFrom(self, city_name: str):
        if city_name not in self.cities:
            raise ValueError(f"La ville '{city_name}' n'existe pas.")
        city = self.cities[city_name]
        return [road for road in self.roads if road.getStartCity() == city]


    def getAllRoads(self):
        return self.roads


    def getAllCities(self):
        return list(self.cities.keys())


    def getDegree(self):
        return len(self.cities)
    

    def getDegreeNode(self, city_name: str):
        return len(self.getRoadsFrom(city_name))
    

    def getWeight(self, city1_name, city2_name):
        """
        Renvoie le poids (distance ou coût) entre deux villes si la route existe.
        Retourne float('inf') si aucune route ne les relie.
        """
        city1 = self.getCity(city1_name)
        city2 = self.getCity(city2_name)
        if not city1 or not city2:
            return float('inf')

        # Vérifie s’il existe une route directe entre les deux villes
        for road in self.getAllRoads():
            c1 = road.getCity1().getName()
            c2 = road.getCity2().getName()
            if (c1 == city1_name and c2 == city2_name) or (c1 == city2_name and c2 == city1_name):
                return road.getDistance()

        return float('inf')
    

    def getRoad(self, city1_name, city2_name):
        """
        Renvoie la route (objet Road) reliant deux villes, si elle existe.
        Retourne None si aucune route ne les relie.
        """
        city1 = self.getCity(city1_name)
        city2 = self.getCity(city2_name)
        if not city1 or not city2:
            return None

        for road in self.getAllRoads():
            c1 = road.getCity1().getName()
            c2 = road.getCity2().getName()
            if (c1 == city1_name and c2 == city2_name) or (c1 == city2_name and c2 == city1_name):
                return road

        return None




    def __repr__(self):
        repr_str = "Graph:\n"
        for road in self.roads:
            repr_str += f"  {road.getCity1().getName()} <-> {road.getCity2().getName()} ({road.getDistance()} km)\n"
        return repr_str
