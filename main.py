import time
from src.utils.generators.generatorGraph import generatorGraph
from src.utils.generators.generatorInstance import generatorInstance

# start = time.time()
# graph = generatorGraph('graphe_50_villes.csv')
# end = time.time()
# print(graph)
# print(end-start)

generatorInstance('fixtures/graphs/graph_50.csv', 10)