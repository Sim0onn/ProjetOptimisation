import pandas as pd
import random
from src.classes.graph import Graph  
from src.utils.generators.generatorObjects  import generatorObjects 

def generatorGraph(n: int):
    # Lecture du fichier CSV
    df = pd.read_csv("fixtures/cities_data.csv")
    df.columns = df.columns.str.strip()

    # Liste de toutes les villes uniques
    villes = list(set(df['City1']).union(set(df['City2'])))

    # Vérification du nombre demandé
    if n > len(villes):
        raise ValueError(
            f"Nombre demandé ({n}) supérieur au nombre de villes disponibles ({len(villes)})."
        )

    # Sélection aléatoire de n villes
    villes_aleatoires = random.sample(villes, n)

    # Filtrage des arêtes (routes) qui ne concernent que ces villes sélectionnées
    df_filtered = df[
        (df['City1'].isin(villes_aleatoires)) &
        (df['City2'].isin(villes_aleatoires))
    ]

    # Création du graphe
    graph = Graph()

    # Ajout des villes + génération d'entrepôts
    for name in villes_aleatoires:
        graph.addCity(name)
        # On accède directement à l'objet City
        graph.cities[name].addWarehouse(generatorObjects(100))

    # Ajout des routes
    for _, row in df_filtered.iterrows():
        city1 = row['City1']
        city2 = row['City2']
        distance = row['Distance']
        graph.addRoad(city1, city2, distance) 

    return graph
