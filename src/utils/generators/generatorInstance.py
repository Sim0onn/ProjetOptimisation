from .generatorGraph import generatorGraph
from .generatorWarehouse import generatorWarehouse
from .generatorCustomers import generatorCustomers
import pandas as pd

def generatorInstance(graph_file: str, nb_it: int):
    cpt_customers = 0
    cpt_warehouses = 0

    graph = generatorGraph(graph_file)
    df = pd.read_csv(f'fixtures/cities/cities_{nb_it}.csv')

    print()

    # Récupérer et trier les villes dans l'ordre numérique
    cities = graph.getCities()
    sorted_cities = sorted(cities.keys(), key=lambda x: int(x.split('_')[1]))
    for city in sorted_cities:
        print(f"\n{'='*60}")
        print(f"VILLE : {city}")
        print(f"{'='*60}")

        city_data = df[df['City_name'] == city]
        if not city_data.empty:
            nb_warehouses = city_data.iloc[0]['Nb_warehouses']
            nb_customers = city_data.iloc[0]['Nb_customers']
            print(f"Configuration de la ville:")
            print(f"- Nombre d'entrepôts : {nb_warehouses}")
            print(f"- Nombre de clients : {nb_customers}")
        else:
            print(f"Attention : Aucune donnée trouvée pour {city} dans le CSV")
            nb_warehouses = 0
            nb_customers = 0

        # Création des entrepôts
        if nb_warehouses > 0:
            print(f"\n--- Création des entrepôts ---")
        for _ in range(nb_warehouses):
            warehouse = generatorWarehouse(nb_it, cpt_warehouses)
            graph.cities[city].addWarehouse(warehouse)
            cpt_warehouses += 10

        # Création des clients
        if nb_customers > 0:
            print(f"\n--- Création des clients ---")
        for _ in range(nb_customers):
            cpt_customers+=1
            customer = generatorCustomers(nb_it,cpt_customers)
            graph.cities[city].addCustomer(customer)

        # Affichage des entrepôts
        if nb_warehouses > 0:
            print(f"\nSTOCK DES ENTREPÔTS:")
            print(f"{'-'*30}")
            for i, wh in enumerate(graph.cities[city].warehouses[:nb_warehouses]):
                print(f"Entrepôt #{i+1}:")
                wh.printStock()
                print(f"{'-'*30}")
        
        # Affichage des clients
        if nb_customers > 0:
            print(f"\nDEMANDES DES CLIENTS:")
            print(f"{'-'*30}")
            for i, customer in enumerate(graph.cities[city].customers[:nb_customers]):
                print(f"Client #{i+1}:")
                customer.printWishlist()
                print(f"{'-'*30}")
        
        print(f"\n{'='*60}\n")
        print('-------------------------------------------------')

    print("\n=== DISTANCES ENTRE LES VILLES ===")
    for road in graph.getAllRoads():
        city1 = road.getCity1().getName()
        city2 = road.getCity2().getName()
        distance = road.getDistance()
        print(f"Distance entre {city1} et {city2} : {distance} km")

    return graph