from src.utils.generators.generatorInstance import generatorInstance

graph = generatorInstance()

pickup_cities = [...]   # villes où il faut collecter
delivery_cities = [...] # villes où il faut livrer
end_city = "city_X"     # ville finale
nb_trucks = 3



def build_distance_matrix(graph):
    cities = list(graph.getCities().keys())
    n = len(cities)
    dist = {c1: {} for c1 in cities}

    for road in graph.getAllRoads():
        c1 = road.getCity1().getName()
        c2 = road.getCity2().getName()
        d = road.getDistance()
        dist[c1][c2] = d
        dist[c2][c1] = d  # graphe non orienté
    return dist

def extract_delivery_data(graph):
    pickup_cities = set()
    end_city = None

    for city_name, city_obj in graph.getCities().items():
        # Vérifier s'il y a des clients
        if not city_obj.customers:
            continue

        # Pour chaque client de la ville
        for customer in city_obj.customers:
            end_city = city_name  # la ville du client est la destination finale
            for obj in customer.objects:  # objets commandés
                # Chercher dans tous les entrepôts du graphe où cet objet est disponible
                for city_name2, city_obj2 in graph.getCities().items():
                    for warehouse in city_obj2.warehouses:
                        for wh_obj in warehouse.stock:
                            if wh_obj.type == obj.type and wh_obj.name == obj.name:
                                pickup_cities.add(city_name2)

    return list(pickup_cities), end_city






def greedy_route(start_city, pickup_cities, delivery_cities, end_city, dist):
    route = [start_city]
    visited = set([start_city])

    remaining_pickups = set(pickup_cities)
    remaining_deliveries = set(delivery_cities)

    current = start_city
    while remaining_pickups or remaining_deliveries:
        candidates = list(remaining_pickups or remaining_deliveries)
        next_city = min(candidates, key=lambda c: dist[current][c])
        route.append(next_city)
        visited.add(next_city)
        current = next_city
        if next_city in remaining_pickups:
            remaining_pickups.remove(next_city)
        elif next_city in remaining_deliveries:
            remaining_deliveries.remove(next_city)

    route.append(end_city)
    return route


def two_opt(route, dist):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best)-2):
            for j in range(i+1, len(best)):
                if j - i == 1:
                    continue
                new_route = best[:i] + best[i:j][::-1] + best[j:]
                if route_distance(new_route, dist) < route_distance(best, dist):
                    best = new_route
                    improved = True
    return best

def route_distance(route, dist):
    return sum(dist[route[i]][route[i+1]] for i in range(len(route)-1))

def assign_cities_to_trucks(cities, nb_trucks):
    # division naïve : par blocs
    chunk_size = len(cities) // nb_trucks
    return [cities[i:i+chunk_size] for i in range(0, len(cities), chunk_size)]




dist = build_distance_matrix(graph)

pickup_cities, end_city = extract_delivery_data(graph)
if not pickup_cities or not end_city:
    raise ValueError("Impossible de générer un plan de livraison : pas de clients ou d'objets disponibles.")

start_city = list(graph.getCities().keys())[0]  # première ville du graphe
delivery_cities = [end_city]

route, total_distance = greedy_route(
    start_city,
    pickup_cities,
    delivery_cities,
    end_city,
    dist
)

print("\n=== PLAN DE LIVRAISON ===")
print(" → ".join(route))
print(f"Distance totale estimée : {total_distance:.2f} km")

