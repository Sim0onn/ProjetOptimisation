import csv
import random
import os
from dotenv import load_dotenv
load_dotenv()
SEED = int(os.getenv("SEED", 42))

def generateObjectsData(warehouse_count: int, nb_it: int):

    random.seed(SEED)  

    file_name = f"objects_{nb_it}.csv"
    full_file_path = os.path.join("objects", file_name)

    os.makedirs("objects", exist_ok=True)

    categories = [
        "Unspecified", "Food", "Flammable", "Explosive", "Toxic",
        "Radioactive", "Corrosive", "Oxidizing", "Pressurized", "Fragile"
    ]

    data_rows = []
    obj_counter = 1

    for w in range(warehouse_count):
        # Choisir un type aléatoire pour le warehouse
        chosen_category = random.choice(categories)
        for _ in range(10):
            object_name = f"Object_{obj_counter:05d}"
            data_rows.append([chosen_category, object_name])
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
