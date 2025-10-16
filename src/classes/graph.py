from src.classes.city import City
from src.classes.road import Road

class Graph:

    def __init__(self):
        self.cities = {}
        self.roads = []


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

        start_city = self.cities[city_name1]
        end_city = self.cities[city_name2]

        if not self.roadExists(start_city, end_city):
            road = Road(start_city, end_city, distance)
            self.roads.append(road)

            reverse_road = Road(end_city, start_city, distance)
            self.roads.append(reverse_road)
        else:
            print(f"La route entre {city_name1} et {city_name2} existe déjà.")


    def roadExists(self, start_city: City, end_city: City) -> bool:
        for road in self.roads:
            if (road.getStartCity() == start_city and
                road.getEndCity() == end_city):
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


    def __repr__(self):
        repr_str = "Graph:\n"
        for road in self.roads:
            repr_str += f"  {road.getStartCity().getName()} -> {road.getEndCity().getName()} ({road.getDistance()} km)\n"
        return repr_str
