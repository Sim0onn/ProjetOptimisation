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

    # Lecture du fichier complet, sans limitation à 10 lignes
    df = pd.read_csv(f'fixtures/objects/objects_{nb_it}.csv')

    # Nombre d'objets à attribuer au client
    n_objets = random.randint(3, 5)

    # Tirage aléatoire dans tout le fichier
    indices = random.sample(range(len(df)), n_objets) if len(df) >= n_objets else list(range(len(df)))
    sample_df = df.iloc[indices]

    # Transformation en liste de tuples (type, name)
    tableau_tuples = list(sample_df.itertuples(index=False, name=None))

    # Ajout des objets au client
    for type, name in tableau_tuples:
        customer.addObject(type, name)

    return customer
