import time
from src.utils.generators.generatorGraph import generatorGraph
from src.utils.generators.generatorInstance import generatorInstance
import os 
from dotenv import load_dotenv
from src.utils.algorithms.algoTaboo import algoTaboo
from src.utils.algorithms.algoGenetics import algoGenetics

def update_env_seed(seed, path=".env"):
    lines = []
    seed_set = False

    # Lire le .env si il existe
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if line.startswith("SEED2="):
                    lines.append(f"SEED2={seed}\n")
                    seed_set = True
                else:
                    lines.append(line)

    # Si aucune ligne SEED= existait → on l'ajoute
    if not seed_set:
        lines.append(f"SEED2={seed}\n")

    # Réécrire proprement
    with open(path, "w") as f:
        f.writelines(lines)

for i in range(20):
    print(f"-----------------------ittérations-{i}-----------------------")
    update_env_seed(i)
    start = time.time()
    algoTaboo()
    end = time.time()
    print(end-start)
    start = time.time()
    algoGenetics()
    end = time.time()
    print(end-start)
    