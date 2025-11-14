import csv
from src.classes.graph import Graph

import os 
from dotenv import load_dotenv
load_dotenv()
NB_INSTANCES = str(os.getenv("NB_INSTANCES"))

def generatorGraph(nb_it=NB_INSTANCES):
    """
    Génère un Graph à partir du nb de villes entrée en param ou le nombre de la var .env.`.
    """

    path_file = f"fixtures/graphs/graph_{nb_it}.csv"
    graph = Graph()
    
    print(f"Chargement du graphe depuis le fichier : '{path_file}'...")
    
    try:
        with open(path_file, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                end_city = row['End_city']
                start_city = row['Start_city']
                distance = float(row['Distance'])
                
                graph.addRoad(start_city, end_city, distance)

        print(f"-> Chargement terminé. Le graphe contient {graph.getDegree()} villes et {len(graph.getAllRoads())} routes.")
        return graph

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{path_file}' n'a pas été trouvé.")
        return Graph()
    except KeyError as e:
        print(f"Erreur : Colonne manquante dans le CSV : {e}. Vérifiez l'en-tête.")
        return Graph()
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        return Graph()
