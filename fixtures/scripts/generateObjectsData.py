import csv
import random
import os

def generateObjectsData(item_count: int, output_directory: str):

    file_name = f"{output_directory}_{item_count}.csv"
    full_file_path = os.path.join(output_directory, file_name)

    #print(f"Génération du fichier '{full_file_path}'...")

    categories = [
        "Unspecified", "Food", "Flammable", "Explosive", "Toxic",
        "Radioactive", "Corrosive", "Oxidizing", "Pressurized", "Fragile"
    ]
    
    data_rows = []
    for i in range(1, item_count + 1):
        object_name = f"Object_{i:05d}"
        chosen_category = random.choice(categories)
        data_rows.append([chosen_category, object_name])
        
    random.shuffle(data_rows)

    try:
        with open(full_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Category', 'Object'])  
            writer.writerows(data_rows)    
                
        #print(f"-> Fichier '{full_file_path}' créé avec succès.")

    except IOError as e:
        print(f"ERREUR lors de la création du fichier '{full_file_path}': {e}")
