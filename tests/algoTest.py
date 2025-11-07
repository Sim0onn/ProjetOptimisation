from math import inf
from src.utils.generators.generatorInstance import generatorInstance

graph = generatorInstance()

nb_trucks = 2


def build_distance_matrix(graph):
    """Matrice initiale : inf quand pas d'arête directe, 0 sur la diagonale."""
    cities = list(graph.getCities().keys())
    dist = {u: {v: inf for v in cities} for u in cities}
    for u in cities:
        dist[u][u] = 0.0

    for road in graph.getAllRoads():
        c1 = road.getCity1().getName().strip()
        c2 = road.getCity2().getName().strip()
        d = road.getDistance()
        # garder la plus petite si multiples arêtes
        if d < dist[c1].get(c2, inf):
            dist[c1][c2] = d
            dist[c2][c1] = d

    return dist


def floyd_warshall_with_next(dist):
    """Floyd–Warshall renvoyant (shortest_dist, next_node)"""
    nodes = list(dist.keys())
    d = {u: {v: dist[u][v] for v in nodes} for u in nodes}
    nxt = {u: {v: (v if d[u][v] < inf else None) for v in nodes} for u in nodes}

    for k in nodes:
        for i in nodes:
            if d[i][k] == inf:
                continue
            for j in nodes:
                if d[k][j] == inf:
                    continue
                via = d[i][k] + d[k][j]
                if via < d[i][j]:
                    d[i][j] = via
                    nxt[i][j] = nxt[i][k]
    return d, nxt


def reconstruct_path(u, v, nxt):
    """Reconstruit la séquence u -> ... -> v (vide si pas de chemin)."""
    if u not in nxt or nxt[u].get(v) is None:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path


def extract_delivery_data(graph):
    """
    Retourne :
      - pickups: toutes les villes contenant des entrepôts utiles
      - deliveries: liste de tuples (ville_client, nom_client, objets_demandes)
      - mapping: { nom_client : [villes_source_possibles] }
    """
    pickups = set()
    deliveries = []
    mapping = {}

    for city_name, city_obj in graph.getCities().items():
        if not getattr(city_obj, "customers", []):
            continue
        for customer in city_obj.customers:
            customer_name = getattr(customer, "name", "?")
            demanded_objs = getattr(customer, "objects", [])
            deliveries.append((city_name, customer_name, demanded_objs))
            mapping[customer_name] = []

            for obj in demanded_objs:
                for city_name2, city_obj2 in graph.getCities().items():
                    for warehouse in getattr(city_obj2, "warehouses", []):
                        for wh_obj in getattr(warehouse, "stock", []):
                            if wh_obj.type == obj.type and wh_obj.name == obj.name:
                                pickups.add(city_name2)
                                mapping[customer_name].append(city_name2)

    return list(pickups), deliveries, mapping



def greedy_on_key_nodes(start, pickups, end_city, shortest_dist):
    """
    Heuristique gloutonne sur le graphe contracté des 'key nodes' :
    - start : ville de départ (dépôt)
    - pickups : villes à visiter pour récupérer les objets
    - end_city : ville du client
    """
    # Key nodes = dépôt + pickups + client final
    key_nodes = [start] + list(pickups) + [end_city]

    current = start
    remaining = set(pickups)  # on ne visite que les pickups avant le client
    order = [start]

    while remaining:
        candidates = [c for c in remaining if shortest_dist[current].get(c, inf) < inf]
        if not candidates:
            print(f"⚠️ Aucune ville de pickup atteignable depuis {current}. Arrêt.")
            break
        next_node = min(candidates, key=lambda c: shortest_dist[current][c])
        order.append(next_node)
        remaining.discard(next_node)
        current = next_node

    # ajouter enfin la ville du client
    if shortest_dist[current].get(end_city, inf) < inf:
        order.append(end_city)
    else:
        print(f"⚠️ Impossible d’ajouter le client final {end_city} depuis {current}.")

    return order




def expand_order_to_full_route(order, nxt, shortest_dist):
    """
    Déploie l'ordre de key nodes en route complète (tous les nœuds intermédiaires).
    Retourne (full_route_list, total_distance).
    """
    if not order:
        return [], 0.0
    full = [order[0]]
    total = 0.0
    for i in range(len(order) - 1):
        u = order[i]
        v = order[i + 1]
        if shortest_dist[u].get(v, inf) == inf:
            print(f"⚠️ Pas de chemin entre {u} et {v} selon shortest_dist.")
            return full, total
        segment = reconstruct_path(u, v, nxt)
        if not segment:
            print(f"⚠️ Impossible de reconstruire le segment {u}->{v}.")
            return full, total
        # segment commence par u; éviter duplication
        if full and segment[0] == full[-1]:
            segment = segment[1:]
        full.extend(segment)
        total += shortest_dist[u][v]
    return full, total

def choose_start_and_end(pickups, deliveries):
    """
    Retourne un point de départ et un point d'arrivée logiques :
      - départ = un entrepôt (pickup)
      - arrivée = la ville du premier client
    """
    if not pickups or not deliveries:
        raise ValueError("Pas assez de données pour définir départ et arrivée.")
    start_city = pickups[0]
    end_city = deliveries[0][0]  # ville du premier client
    return start_city, end_city

def assign_clients_to_trucks(deliveries, nb_trucks):
    """
    Répartit les clients sur les camions de manière simple (round-robin).
    Retourne un dict : {truck_id: [clients]}
    """
    trucks = {i: [] for i in range(nb_trucks)}
    for idx, client in enumerate(deliveries):
        truck_id = idx % nb_trucks
        trucks[truck_id].append(client)
    return trucks












# -------------------- Exécution --------------------

dist = build_distance_matrix(graph)
shortest_dist, nxt = floyd_warshall_with_next(dist)

pickup_cities, deliveries, mapping = extract_delivery_data(graph)
if not pickup_cities or not deliveries:
    raise ValueError("Aucune donnée de livraison disponible.")

# Répartir les clients sur les camions
def assign_clients_to_trucks(deliveries, nb_trucks):
    trucks = {i: [] for i in range(nb_trucks)}
    for idx, client in enumerate(deliveries):
        truck_id = idx % nb_trucks
        trucks[truck_id].append(client)
    return trucks

trucks_clients = assign_clients_to_trucks(deliveries, nb_trucks)

# Calculer la route pour chaque camion
for truck_id, clients in trucks_clients.items():
    print(f"\n=== CAMION {truck_id} ===")
    truck_route_nodes = []
    truck_full_route = []
    truck_total_distance = 0.0

    # conserver le dépôt initial du camion pour le retour
    start_city_initial = mapping[clients[0][1]][0]  # premier dépôt du premier client

    last_position = start_city_initial  # position actuelle du camion

    for client_data in clients:
        end_city, client_name, demanded_objs = client_data
        relevant_pickups = mapping[client_name]

        # Départ depuis la dernière position du camion
        start_city = last_position

        # 1) calculer l'ordre sur les key nodes (dépôts + client)
        order_nodes = greedy_on_key_nodes(start_city, relevant_pickups, end_city, shortest_dist)

        # 2) déployer la route complète (avec intermédiaires si nécessaires)
        full_route, total_distance = expand_order_to_full_route(order_nodes, nxt, shortest_dist)

        # mettre à jour la dernière position du camion
        last_position = full_route[-1] if full_route else start_city

        # accumuler pour le camion
        truck_route_nodes.extend(order_nodes)
        truck_full_route.extend(full_route if not truck_full_route else full_route[1:])  # éviter duplication
        truck_total_distance += total_distance

    # Ajouter le retour au dépôt initial si ce n’est pas déjà la dernière ville
    if last_position != start_city_initial:
        order_nodes_return = greedy_on_key_nodes(last_position, [], start_city_initial, shortest_dist)
        full_route_return, total_distance_return = expand_order_to_full_route(order_nodes_return, nxt, shortest_dist)
        truck_route_nodes.extend(order_nodes_return[1:])  # éviter duplication
        truck_full_route.extend(full_route_return[1:])
        truck_total_distance += total_distance_return

    # Affichage du résultat pour le camion
    print(" -> ".join(truck_route_nodes))
    print(" -> ".join(truck_full_route))
    print(f"Distance totale estimée pour camion {truck_id} : {truck_total_distance:.2f} km")


