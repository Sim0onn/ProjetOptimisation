from src.classes.graph import Graph
import random
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ------------------ CONSTANTES ------------------

VITESSE_BASE = float(os.getenv("VITESSE_BASE", 90))
CONSO_BASE = float(os.getenv("CONSO_BASE", 0.33))

COEFF_FLUIDE = float(os.getenv("COEFF_FLUIDE", 1))
COEFF_MODERE = float(os.getenv("COEFF_MODERE", 1.15))
COEFF_LOURD = float(os.getenv("COEFF_LOURD", 1.3))

IMPORTANCE_TEMPS = float(os.getenv("IMPORTANCE_TEMPS", 0.4))
IMPORTANCE_CONSO = float(os.getenv("IMPORTANCE_CONSO", 0.6))

# --------------------------------------------------
#  Génère les 11 graphes horaires (8h → 18h)
# --------------------------------------------------

def generateTrafficGraphs(base_graph):
    """
    Retourne une liste de Graph : [8h, 9h, ..., 18h]
    Chaque graphe contient les poids adaptés à la congestion de l'heure.
    """
    trafficGraphs = []

    horaires = {
        0: (1.2, 1.5),  # 8h
        1: (1.1, 1.4),  # 9h
        2: (1.0, 1.2),  # 10h
        3: (1.0, 1.2),  # 11h
        4: (1.1, 1.3),  # 12h
        5: (1.0, 1.2),  # 13h
        6: (1.0, 1.1),  # 14h
        7: (1.0, 1.3),  # 15h
        8: (1.1, 1.4),  # 16h
        9: (1.2, 1.5),  # 17h
        10: (1.1, 1.4), # 18h
    }

    for i, (congestionMin, congestionMax) in horaires.items():
        trafficGraph = Graph()

        for road in base_graph.getAllRoads():
            start_city = road.getCity1().getName()
            end_city = road.getCity2().getName()
            distance = road.getDistance()

            congestion = random.uniform(congestionMin, congestionMax)
            temps = (distance / VITESSE_BASE) * congestion

            if congestion < 1.2:
                conso = distance * CONSO_BASE * COEFF_FLUIDE * congestion
            elif congestion < 1.4:
                conso = distance * CONSO_BASE * COEFF_MODERE * congestion
            else:
                conso = distance * CONSO_BASE * COEFF_LOURD * congestion

            poids = IMPORTANCE_TEMPS * temps + IMPORTANCE_CONSO * conso

            if start_city not in trafficGraph.getCities():
                trafficGraph.addCity(start_city)
            if end_city not in trafficGraph.getCities():
                trafficGraph.addCity(end_city)

            trafficGraph.addRoad(start_city, end_city, poids)

        trafficGraphs.append(trafficGraph)

    return trafficGraphs


# --------------------------------------------------
#  Génère une table de poids horaire : {(A,B): {8: val, 9: val, ...}}
# --------------------------------------------------

def generateWeightTable(graph):
    """
    Génère une table de poids initiale à partir du graphe de base.
    """
    weight_table = {}
    cities = graph.getAllCities()
    
    for c1 in cities:
        weight_table[c1] = {}
        for c2 in cities:
            if c1 == c2:
                weight_table[c1][c2] = 0
            else:
                road = graph.getRoad(c1, c2)
                weight_table[c1][c2] = road.getDistance() if road else float('inf')
    return weight_table


# --------------------------------------------------
#  Récupère un poids pour une heure donnée (avec interpolation)
# --------------------------------------------------

def getInterpolatedWeight(weight_table, city1, city2, hour):
    """
    Retourne le poids interpolé entre city1 et city2 à une heure donnée.
    Ex : getInterpolatedWeight(table, 'A', 'B', 10.5)
    """
    if (city1, city2) not in weight_table:
        return float("inf")

    h_int = int(hour)
    h_next = min(18, h_int + 1)
    ratio = hour - h_int

    w1 = weight_table[(city1, city2)].get(h_int)
    w2 = weight_table[(city1, city2)].get(h_next, w1)

    if w1 is None:
        return float("inf")

    return (1 - ratio) * w1 + ratio * w2


# --------------------------------------------------
#  Récupère le graphe correspondant à une heure donnée
# --------------------------------------------------

def getGraphAtHour(base_graph, hour):
    """
    Retourne le Graph le plus proche de l'heure donnée.
    """
    index = max(0, min(10, round(hour - 8)))
    graphs = generateTrafficGraphs(base_graph)
    return graphs[index]


def applyDynamicWeights(graph, weight_table, current_time=None):
    """
    Applique des variations de poids en fonction de l'heure (simulation trafic).
    """
    if current_time is None:
        current_time = datetime.now().hour

    peak_hours = range(7, 10)
    evening_hours = range(17, 20)

    for c1 in weight_table:
        for c2 in weight_table[c1]:
            if c1 != c2 and weight_table[c1][c2] != float('inf'):
                base = weight_table[c1][c2]
                if current_time in peak_hours:
                    variation = random.uniform(1.3, 1.7)
                elif current_time in evening_hours:
                    variation = random.uniform(1.1, 1.4)
                else:
                    variation = random.uniform(0.9, 1.1)
                weight_table[c1][c2] = round(base * variation, 2)
    return weight_table
