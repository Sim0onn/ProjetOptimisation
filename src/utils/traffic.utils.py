from src.classes.graph import Graph
import random

vitesseBase = 90
consoBase = 0.33

coeffFluide = 1
coeffModere = 1.15
coeffLourd = 1.3

importanceCout = 1
importanceConso = 1

def generateTrafficGraphs(base_graph):
    for i in range(11):
        match i:
            case 0: #traffic a 8 heures
                congestionTraffic = random.random(1.2,1.5)
            case 1: #traffic a 9 heures
                congestionTraffic = random.random(1.1,1.4)
            case 2: #traffic a 10 heures
                congestionTraffic = random.random(1,1.2)
            case 3: #traffic a 11 heures
                congestionTraffic = random.random(1,1.2)
            case 4: #traffic a 12 heures
                congestionTraffic = random.random(1.1,1.3)
            case 5: #traffic a 13 heures
                congestionTraffic = random.random(1,1.2)
            case 6: #traffic a 14 heures
                congestionTraffic = random.random(1,1.1)
            case 7: #traffic a 15 heures
                congestionTraffic = random.random(1,1.3)
            case 8: #traffic a 16 heures
                congestionTraffic = random.random(1.1,1.4)
            case 9: #traffic a 17 heures
                congestionTraffic = random.random(1.2,1.5)
            case 10: #traffic a 18 heures
                congestionTraffic = random.random(1.1,1.4)

        tempsTrajet = distance/vitesseBase * congestionTraffic

        match congestionTraffic:
            case x if x < 1.2:
                consoTrajet = distance*consoBase * coeffFluide * congestionTraffic
            case x if 1.2 <= x < 1.4:
                consoTrajet = distance*consoBase * coeffModere * congestionTraffic
            case x if x >= 1.4:
                consoTrajet = distance*consoBase * coeffLourd * congestionTraffic
            case _:


                
                



