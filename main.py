import time
from src.utils.generators.generatorGraph import generatorGraph
from src.utils.generators.generatorObjects import generatorObjects

# start = time.time()
# graph = generatorGraph('graphe_50_villes.csv')
# end = time.time()
# print(graph)
# print(end-start)

print("Génération des objets...")
datas = generatorObjects(10)
print("Objets générés :")
datas.printStock()