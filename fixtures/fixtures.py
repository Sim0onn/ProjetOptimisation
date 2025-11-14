import os
from scripts.generateCitiesData import *
from scripts.generateGraphsData import *
from scripts.numberOfWarehouses import *
from scripts.generateObjectsData import *
from scripts.cleanFolder import *

def main():
    # Vérifier et créer les dossiers si nécessaire
    for folder in ["objects", "cities", "graphs"]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    iterations = [6, 10, 20, 30, 50, 100, 200, 500, 1000, 2000]

    cleanFolder("objects", "*.csv")
    cleanFolder("cities", "*.csv")
    cleanFolder("graphs", "*.csv")

    for i in iterations:
        generateGraphsData(i)
        generateCitiesData(i)
        nb = numberOfWarehouses(f'cities/cities_{i}.csv')
        generateObjectsData(nb, i)

if __name__ == "__main__":
    main()
