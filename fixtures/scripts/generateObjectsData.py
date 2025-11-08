import csv
import random
import os
from dotenv import load_dotenv
load_dotenv()
SEED = int(os.getenv("SEED", 42))
OBJ_PER_WH = int(os.getenv("OBJ_PER_WH"))


def generateObjectsData(warehouse_count: int, nb_it: int):
    print(warehouse_count)
    random.seed(SEED)

    filename = f"objects_{nb_it}.csv"
    full_file_path = os.path.join("objects", filename)

    os.makedirs("objects", exist_ok=True)

    categories = [
        "Unspecified", "Food", "Flammable", "Explosive", "Toxic",
        "Radioactive", "Corrosive", "Oxidizing", "Pressurized", "Fragile"
    ]

    data_rows = []
    obj_counter = 1

    for w in range(warehouse_count):
        # Choisir un type aléatoire pour le warehouse
        chosencategory = random.choice(categories)
        for  _ in range(OBJ_PER_WH):
            objectname = f"Object{obj_counter:05d}"
            data_rows.append([chosencategory, objectname])
            obj_counter += 1

    # Mélanger éventuellement les lignes entre warehouses si tu veux
    #random.shuffle(data_rows)

    try:
        with open(full_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Category', 'Object'])
            writer.writerows(data_rows)

        print(f"Fichier généré : {full_file_path} ({len(data_rows)} objets, {warehouse_count} warehouses)")
    except IOError as e:
        print(f"ERREUR lors de la création du fichier '{full_file_path}': {e}")
