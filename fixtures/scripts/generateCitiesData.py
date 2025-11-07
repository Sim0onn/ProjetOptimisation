import csv
import random
import os

def generateCitiesData(nb_it: str):
    
    file_name = f"cities_{nb_it}.csv"
    full_file_path = os.path.join("cities", file_name)

    try:
        with open(full_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            writer.writerow(['City_name', 'Nb_warehouses', 'Nb_customers'])

            for i in range(1, nb_it + 1):
                city_name = f"Ville_{i:04d}"

                num_warehouses = random.randint(0, 3)
                num_customers = random.randint(0, 3)

                writer.writerow([city_name, num_warehouses, num_customers])

    except IOError as e:
        print(f"ERREUR lors de la création du fichier '{full_file_path}': {e}")
