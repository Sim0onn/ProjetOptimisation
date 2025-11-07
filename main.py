import time
from src.utils.generators.generatorGraph import generatorGraph
from src.utils.generators.generatorInstance import generatorInstance
import os 
from dotenv import load_dotenv

# start = time.time()
# graph = generatorGraph('graphe_50_villes.csv')
# end = time.time()
# print(graph)
# print(end-start)

load_dotenv()
NB_INSTANCES = str(os.getenv("NB_INSTANCES"))

generatorInstance(NB_INSTANCES)
