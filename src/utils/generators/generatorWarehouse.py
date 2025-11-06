from src.classes import Warehouse
import pandas as pd

def generatorWarehouse(nb_it, start):
    warehouse = Warehouse()

    df = pd.read_csv(f'fixtures/objects/objects_{nb_it}.csv')
    selected_df = df.iloc[start:start+10]
    tableau_tuples = list(selected_df.itertuples(index=False, name=None))

    for type, name in tableau_tuples:
        warehouse.addObject(type,name)
    return warehouse

