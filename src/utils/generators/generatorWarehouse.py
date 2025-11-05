from src.classes import Warehouse
import pandas as pd
import random 
from dotenv import load_dotenv
import os

load_dotenv()
SEED = int(os.getenv("SEED"))

random.seed(SEED)

def generatorWarehouse(nb_it, start):
    W1 = Warehouse()

    df = pd.read_csv(f'fixtures/objects/objects_{nb_it}.csv')
    selected_df = df.iloc[start:start+10]
    tableau_tuples = list(selected_df.itertuples(index=False, name=None))

    for type, name in tableau_tuples:
        W1.addObject(type,name)
    return W1

def generatorCustomers(nb_it):
    W1 = Warehouse()

    df = pd.read_csv(f'fixtures/objects/objects_{nb_it}.csv')
    selected_df = df.iloc[:10]
    n_objets = random.randint(3, 5)  
    indices = random.sample(range(len(selected_df)), n_objets) if len(selected_df) >= n_objets else list(range(len(selected_df)))
    sample_df = selected_df.iloc[indices]
    tableau_tuples = list(sample_df.itertuples(index=False, name=None))

    for type, name in tableau_tuples:
        W1.addObject(type, name)
    return W1