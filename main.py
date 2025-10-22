import time
from src.utils.generators.generatorGraph import generatorGraph

start = time.time()
graph = generatorGraph('graphe_50_villes.csv')
end = time.time()
print(graph)
print(end-start)
first_key = sorted(graph.cities.keys())[0]
Paris = graph.cities[first_key].warehouses
print(Paris[0].getStock())
print(graph.cities[first_key].numberOfWarehouses())
