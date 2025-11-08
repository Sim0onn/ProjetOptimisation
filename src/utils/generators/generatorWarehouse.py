from src.classes import Warehouse
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
NB_INSTANCES = str(os.getenv("NB_INSTANCES"))
SEED = int(os.getenv("SEED", 42))


def generatorWarehouse(start=0, nb_it=NB_INSTANCES):
    """
    Génère un entrepôt avec 10 objets consécutifs à partir de l'index `start`.
    """
    warehouse = Warehouse()

    df = pd.read_csv(f'fixtures/objects/objects_{nb_it}.csv')

    selected_df = df.iloc[start:start + 10]

    for type, name in selected_df.itertuples(index=False, name=None):
        warehouse.addObject(type, name)

    return warehouse
