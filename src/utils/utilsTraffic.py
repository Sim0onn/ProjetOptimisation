from src.classes.graph import Graph
import random

vitesseBase = 90
consoBase = 0.33

coeffFluide = 1
coeffModere = 1.15
coeffLourd = 1.3

importanceTemps = 0.4
importanceConso = 0.6

def generateTrafficGraphs(base_graph):
    trafficGraphs = []

    for i in range(11):
        trafficGraph = Graph()

        match i:
            case 0:  # 8h
                congestionMin, congestionMax = 1.2, 1.5
            case 1:  # 9h
                congestionMin, congestionMax = 1.1, 1.4
            case 2:  # 10h
                congestionMin, congestionMax = 1.0, 1.2
            case 3:  # 11h
                congestionMin, congestionMax = 1.0, 1.2
            case 4:  # 12h
                congestionMin, congestionMax = 1.1, 1.3
            case 5:  # 13h
                congestionMin, congestionMax = 1.0, 1.2
            case 6:  # 14h
                congestionMin, congestionMax = 1.0, 1.1
            case 7:  # 15h
                congestionMin, congestionMax = 1.0, 1.3
            case 8:  # 16h
                congestionMin, congestionMax = 1.1, 1.4
            case 9:  # 17h
                congestionMin, congestionMax = 1.2, 1.5
            case 10:  # 18h
                congestionMin, congestionMax = 1.1, 1.4


        for road in base_graph.getAllRoads():
            start_city = road.getStartCity().getName()
            end_city = road.getEndCity().getName()
            distance = road.getDistance()

            congestionTraffic = random.uniform(congestionMin, congestionMax)

            tempsTrajet = (distance / vitesseBase) * congestionTraffic

            if congestionTraffic < 1.2:
                consoTrajet = distance * consoBase * coeffFluide * congestionTraffic
            elif congestionTraffic < 1.4:
                consoTrajet = distance * consoBase * coeffModere * congestionTraffic
            else:
                consoTrajet = distance * consoBase * coeffLourd * congestionTraffic

            nouveauPoids = (importanceTemps * tempsTrajet) + (importanceConso * consoTrajet)

            trafficGraph.addCity(start_city)
            trafficGraph.addCity(end_city)
            trafficGraph.addRoad(start_city, end_city, nouveauPoids)

        trafficGraphs.append(trafficGraph)

    return trafficGraphs

                
                



