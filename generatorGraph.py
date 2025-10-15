import random 
import pandas as pd
from generatorObjects import generatorObjects
from src.classes import Graph

def generatorGraph(n: int):

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

    # Filtrage des arêtes qui ne concernent que ces villes
    df_filtered = df[
        (df['City1'].isin(villes_aleatoires)) &
        (df['City2'].isin(villes_aleatoires))
    ]

    graph = Graph()

    for name in villes_aleatoires:
        graph.addCity(name)
        graph.nodes[name].addWarehouse(generatorObjects(100))


    for _, row in df_filtered.iterrows():
        city1 = row['City1']
        city2 = row['City2']
        distance = row['Distance']
        graph.addEdge(city1, city2, distance)

    return graph

graph = generatorGraph(20)
print(graph)