import time
from src.utils.generators.generatorGraph import generatorGraph

start = time.time()
graph = generatorGraph(20)
end = time.time()
print(graph)
print(end-start)
first_key = sorted(graph.nodes.keys())[0]
Paris = graph.nodes[first_key].warehouses
print(Paris[0].getStock())
print(graph.nodes[first_key].numberOfWarehouses())
