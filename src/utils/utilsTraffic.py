from src.classes.graph import Graph
import random
import os
from dotenv import load_dotenv
load_dotenv()

VITESSE_BASE = float(os.getenv("VITESSE_BASE", 90))
CONSO_BASE = float(os.getenv("CONSO_BASE", 0.33))

COEFF_FLUIDE = float(os.getenv("COEFF_FLUIDE", 1))
COEFF_MODERE = float(os.getenv("COEFF_MODERE", 1.15))
COEFF_LOURD = float(os.getenv("COEFF_LOURD", 1.3))

IMPORTANCE_TEMPS = float(os.getenv("IMPORTANCE_TEMPS", 0.4))
IMPORTANCE_CONSO = float(os.getenv("IMPORTANCE_CONSO", 0.6))

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
            start_city = road.getCity1().getName()
            end_city = road.getCity2().getName()
            distance = road.getDistance()

            congestionTraffic = random.uniform(congestionMin, congestionMax)

            tempsTrajet = (distance / VITESSE_BASE) * congestionTraffic

            if congestionTraffic < 1.2:
                consoTrajet = distance * CONSO_BASE * COEFF_FLUIDE * congestionTraffic
            elif congestionTraffic < 1.4:
                consoTrajet = distance * CONSO_BASE * COEFF_MODERE * congestionTraffic
            else:
                consoTrajet = distance * CONSO_BASE * COEFF_LOURD * congestionTraffic

            nouveauPoids = (IMPORTANCE_TEMPS * tempsTrajet) + (IMPORTANCE_CONSO * consoTrajet)

            trafficGraph.addCity(start_city)
            trafficGraph.addCity(end_city)
            trafficGraph.addRoad(start_city, end_city, nouveauPoids)

        trafficGraphs.append(trafficGraph)

    return trafficGraphs

                
                



