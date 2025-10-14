from utils import Object, Warehouse, Graph
import pandas as pd
import random

def objects_generator(n):
    stock = Warehouse()

    df = pd.read_excel("fixtures/objects_data.xlsx")
    sample_df = df.sample(n=n)
    tableau_tuples_random = list(sample_df.itertuples(index=False, name=None))

    for type, name in tableau_tuples_random:
        stock.stock.add_object(Object(type,name))
    return stock

datas = objects_generator(100)
datas.stock.print_stock()


def graph_generator(n):
    df = pd.read_excel("fixtures/cities_data.xlsx")
    df.columns = df.columns.str.strip()
    villes = list(set(df['City1']).union(set(df['City2'])))
    villes_aleatoires = random.sample(villes, n)
    df_filtered = df[
    (df['City1'].isin(villes_aleatoires)) &
    (df['City2'].isin(villes_aleatoires))
    ]
    graph1 = Graph(n)
    for _, row in df_filtered.iterrows():
        graph1.add_edge(row['City1'], row['City2'], row['Distance'])
    return graph1

# graph = graph_generator(5)
# graph.print_neighbors()
