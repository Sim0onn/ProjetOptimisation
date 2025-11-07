from scripts.generateCitiesData import *
from scripts.generateGraphsData import *
from scripts.numberOfWarehouses import *
from scripts.generateObjectsData import *
from scripts.cleanFolder import *
import os 
from dotenv import load_dotenv

load_dotenv()
OBJ_PER_WH = str(os.getenv("OBJ_PER_WH"))

def main():
    
    iterations = [6,10,20, 30, 50, 100, 200, 500, 1000, 2000]

    cleanFolder("objects", "*.csv")
    cleanFolder("cities", "*.csv")
    cleanFolder("graphs", "*.csv")

    for i in iterations:
        generateGraphsData(i,"graphs")
        generateCitiesData(i,"cities")
        nb = numberOfWarehouses(f'cities/cities_{i}.csv')
        generateObjectsData(nb*OBJ_PER_WH,i)

if __name__ == "__main__":
    main()
