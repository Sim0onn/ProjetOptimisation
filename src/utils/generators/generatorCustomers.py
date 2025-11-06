import pandas as pd 
import random 
from dotenv import load_dotenv
import os

from src.classes import Customer

load_dotenv()
SEED = int(os.getenv("SEED"))
NB_INSTANCES = str(os.getenv("NB_INSTANCES"))
random.seed(SEED)

def generatorCustomers(nb, nb_it=NB_INSTANCES):
    customer = Customer(f'client_{nb}')

    df = pd.read_csv(f'fixtures/objects/objects_{nb_it}.csv')
    selected_df = df.iloc[:10]
    n_objets = random.randint(3, 5)  
    indices = random.sample(range(len(selected_df)), n_objets) if len(selected_df) >= n_objets else list(range(len(selected_df)))
    sample_df = selected_df.iloc[indices]
    tableau_tuples = list(sample_df.itertuples(index=False, name=None))

    for type, name in tableau_tuples:
        customer.addObject(type, name)
    return customer