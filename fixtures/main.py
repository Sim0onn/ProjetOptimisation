from scripts.generateCitiesData import *
from scripts.generateGraphsData import *
from scripts.mixObjects import *
from scripts.numberOfWarehouses import *
from scripts.generateObjectsData import *
from scripts.cleanFolder import *
from scripts.duplicateFolder import *

def main():
    
    nb_object_per_wh = 10
    iterations = [10,20, 30, 50, 100, 200, 500, 1000, 2000]

    cleanFolder("objects", "*.csv")
    cleanFolder("customers", "*.csv")

    for i in iterations:
        generateGraphsData(i,"graphs")
        generateCitiesData(i,"cities")
        nb = numberOfWarehouses(f'cities/cities_{i}.csv')
        generateObjectsData(nb*nb_object_per_wh,"objects")
        duplicateFolder("objects", "customers")
        mixObjects("customers")

if __name__ == "__main__":
    main()
