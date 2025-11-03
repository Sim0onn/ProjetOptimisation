from .generatorGraph import generatorGraph
from .generatorObjects import generatorObjects

def generatorInstance(graph_file: str, num_objects: int):
    graph = generatorGraph(graph_file)
    objects_file = 'objects_' + graph_file.split('_')[-1]
    print(objects_file)
    
    cities = graph.getCities()
    for city in cities:
        graph.cities[city].addWarehouse(generatorObjects(num_objects, objects_file))
        graph.cities[city].warehouses[0].printStock()
