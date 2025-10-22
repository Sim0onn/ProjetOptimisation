import time
from src.utils.generators.generatorGraph import generatorGraph

start = time.time()
graph = generatorGraph('graphe_50_villes.csv')
end = time.time()
print(graph)
print(end-start)