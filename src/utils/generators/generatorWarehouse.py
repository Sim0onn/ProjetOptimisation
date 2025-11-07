from src.classes import Warehouse
import pandas as pd
import os 
from dotenv import load_dotenv
load_dotenv()
NB_INSTANCES = str(os.getenv("NB_INSTANCES"))

def generatorWarehouse(start=0, nb_it = NB_INSTANCES):
    warehouse = Warehouse()

    df = pd.read_csv(f'fixtures/objects/objects_{nb_it}.csv')
    selected_df = df.iloc[start:start+10]
    tableau_tuples = list(selected_df.itertuples(index=False, name=None))

    for type, name in tableau_tuples:
        warehouse.addObject(type,name)
    return warehouse

