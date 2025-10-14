from utils import Object, Warehouse, Graph
import pandas as pd
import random

def objects_generator(n):
    W1 = Warehouse()

    df = pd.read_excel("fixtures/objects_data.xlsx")
    sample_df = df.sample(n=n)
    tableau_tuples_random = list(sample_df.itertuples(index=False, name=None))

    for type, name in tableau_tuples_random:
        W1.add_object(type,name)
    return W1

# datas = objects_generator(100)
# datas.stock.print_stock()

def graph_generator(n: int):

    df = pd.read_excel("fixtures/cities_data.xlsx")
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
        graph.add_city(name)
        graph.nodes[name].add_warehouse(objects_generator(100))


    for _, row in df_filtered.iterrows():
        city1 = row['City1']
        city2 = row['City2']
        distance = row['Distance']
        graph.add_edge(city1, city2, distance)

    return graph

graph = graph_generator(5)
print(graph)
Paris = graph.nodes['Paris'].warehouses
print(Paris[0].stock.print_stock())