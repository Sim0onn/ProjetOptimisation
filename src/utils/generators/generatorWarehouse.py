from src.classes import Warehouse
import pandas as pd
import os
import random
from dotenv import load_dotenv

load_dotenv()
NB_INSTANCES = str(os.getenv("NB_INSTANCES"))
SEED = int(os.getenv("SEED", 42))
random.seed(SEED)

def generatorWarehouse(start=0, nb_it=NB_INSTANCES):
    warehouse = Warehouse()

    df = pd.read_csv(f'fixtures/objects/objects_{nb_it}.csv')

    categories = df['Category'].unique().tolist()

    chosen_category = random.choice(categories)

    filtered_df = df[df['Category'] == chosen_category]

    n_objects = min(10, len(filtered_df))
    selected_df = filtered_df.sample(n=n_objects, random_state=SEED + start)

    for type, name in selected_df.itertuples(index=False, name=None):
        warehouse.addObject(type, name)

    return warehouse
