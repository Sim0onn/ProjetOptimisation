from src.classes import Warehouse
import pandas as pd

def generatorObjects(n, file):
    W1 = Warehouse()

    df = pd.read_csv(f'fixtures/objects/{file}')
    sample_df = df.sample(n=n, replace=True)
    tableau_tuples_random = list(sample_df.itertuples(index=False, name=None))

    for type, name in tableau_tuples_random:
        W1.addObject(type,name)
    return W1
