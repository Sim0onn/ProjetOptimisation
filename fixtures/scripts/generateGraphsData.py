import csv
import random
import os

def generateGraphsData(city_count: int, output_directory: str):

    file_name = f"graph_{city_count}.csv"
    full_file_path = os.path.join(output_directory, file_name)

    cities = [f"Ville_{i:04d}" for i in range(1, city_count + 1)]
    random.shuffle(cities)  
    
    data_rows = []
    existing_edges = set()

    for i in range(city_count):
        start_city = cities[i]
        end_city = cities[(i + 1) % city_count] 
        
        distance = random.randint(50, 3000)
        edge = (start_city, end_city)
        
        data_rows.append([start_city, end_city, distance])
        existing_edges.add(edge)

    num_edges_to_add = int(city_count * 1.5)
    added_edges_count = 0
    max_attempts = num_edges_to_add * 5  

    while added_edges_count < num_edges_to_add and max_attempts > 0:
        start_city = random.choice(cities)
        end_city = random.choice(cities)
        edge = (start_city, end_city)
        
        if start_city != end_city and edge not in existing_edges:
            distance = random.randint(50, 3000)
            data_rows.append([start_city, end_city, distance])
            existing_edges.add(edge)
            added_edges_count += 1
            
        max_attempts -= 1

    try:

        with open(full_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Start_city', 'End_city', 'Distance'])
            writer.writerows(data_rows)

    except IOError as e:
        print(f"ERREUR lors de la création du fichier '{full_file_path}': {e}")
