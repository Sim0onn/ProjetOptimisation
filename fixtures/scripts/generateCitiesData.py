import csv
import random
import os

def generateCitiesData(city_count: int, output_directory: str):
    
    file_name = f"cities_{city_count}.csv"
    full_file_path = os.path.join(output_directory, file_name)
    
    #print(f"Génération du fichier '{full_file_path}'...")
    
    try:
        with open(full_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            writer.writerow(['City_name', 'Nb_warehouses', 'Nb_customers'])

            for i in range(1, city_count + 1):
                city_name = f"Ville_{i:04d}"

                num_warehouses = random.randint(0, 3)
                num_customers = random.randint(0, 3)

                writer.writerow([city_name, num_warehouses, num_customers])
                
        #print(f"-> Fichier '{full_file_path}' créé avec succès.")

    except IOError as e:
        print(f"ERREUR lors de la création du fichier '{full_file_path}': {e}")
