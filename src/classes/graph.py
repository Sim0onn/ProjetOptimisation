from src.classes.city import City

class Graph:
    def __init__(self):

        self.nodes = {}
        self.edges = {}

    def addCity(self, city_name):

        if city_name not in self.nodes:
            self.nodes[city_name] = City(city_name)
            self.edges[city_name] = {}
        else:
            print(f"La ville '{city_name}' existe déjà.")

    def addEdge(self, city_name1, city_name2, weight=1):

        if city_name1 not in self.nodes:
            self.addCity(city_name1)
        if city_name2 not in self.nodes:
            self.addCity(city_name2)

        self.edges[city_name1][city_name2] = weight
        self.edges[city_name2][city_name1] = weight  

    def getEdge(self, city_name):

        if city_name not in self.nodes:
            raise ValueError(f"La ville '{city_name}' n'existe pas.")
        return self.edges[city_name]

    def getCity(self, city_name):

        return self.nodes.get(city_name, None)

    def __repr__(self):
        repr_str = "Graph:\n"
        for city, neighbors in self.edges.items():
            repr_str += f"  {city} -> {neighbors}\n"
        return repr_str
