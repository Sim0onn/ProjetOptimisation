from src.utils.generators.generatorGraph import generatorGraph

file = 'fixtures/graphs/graph_100.csv'

graph = generatorGraph(file)

if graph and graph.getDegree() > 0:
    print("\n--- Informations sur le graphe chargé ---")
    
    cities = graph.getCities()
    for city in cities:
        print(f"{graph.getCity(city).name}")
    
    roads = graph.getAllRoads()
    for road in roads:
        print(f"{road.getCity1().name} <-> {road.getCity2().name} : {road.distance} km")