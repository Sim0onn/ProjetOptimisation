from .generatorGraph import generatorGraph
from .generatorObjects import generatorObjects

def generatorInstance(graph_file: str, num_objects: int):
    graph = generatorGraph(graph_file)
    
    cities = graph.getCities()
    for city in cities:
        graph.cities[city].addWarehouse(generatorObjects(10))  
        graph.cities[city].warehouses[0].printStock()
