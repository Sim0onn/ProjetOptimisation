import random
from src.utils.commands import *
from math import inf
from src.utils.generators.generatorInstance import generatorInstance

# -------- Paramètres --------
NB_TRUCKS = loadVar("NB_TRUCKS", int)
TABU_MAX_ITER = 100
TABU_TENURE = 10
RANDOM_SEED = loadVar("SEED2",int)

random.seed(RANDOM_SEED)


# -------- Construction de la matrice de distances (graphe de base) --------
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
    """Floyd–Warshall renvoyant (shortest_dist, next_node)."""
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


# -------- Extraction des données de livraison (pickup / deliveries / mapping) --------
def extract_delivery_data(graph):
    """
    Retourne :
      - pickups: liste (ensemble) des villes contenant des entrepôts utiles
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


# -------- Recherche Tabou (optimisation des key nodes) --------
def tabu_search_on_key_nodes(start, pickups, end_city, shortest_dist, max_iter=100, tabu_tenure=10):
    """
    Recherche Tabou appliquée à la séquence des 'key nodes' :
      start : ville de départ (depôt)
      pickups : liste de villes à visiter
      end_city : ville du client
      shortest_dist : matrice des plus courts chemins
    Retourne : liste de villes (start, ... pickups optimisés ..., end_city)
    """
    if not pickups:
        return [start, end_city]

    # solution initiale : ordre glouton proche ou aléatoire
    # pour stabilité, on commence par un ordre aléatoire reproductible
    current_solution = [start] + random.sample(pickups, len(pickups)) + [end_city]

    def total_distance(route):
        total = 0.0
        for i in range(len(route) - 1):
            total += shortest_dist[route[i]].get(route[i + 1], inf)
        return total

    best_solution = list(current_solution)
    best_cost = total_distance(best_solution)
    tabu_list = []
    iteration = 0

    while iteration < max_iter:
        iteration += 1
        neighbors = []
        # générer voisins par swap de deux pickups (ne pas toucher au start et end)
        for i in range(1, len(current_solution) - 2):
            for j in range(i + 1, len(current_solution) - 1):
                neighbor = list(current_solution)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)

        best_neighbor = None
        best_neighbor_cost = inf

        for neighbor in neighbors:
            cost = total_distance(neighbor)
            move_signature = tuple(neighbor[1:-1])  # identité de la permutation (séquence pickups)
            if move_signature not in tabu_list and cost < best_neighbor_cost:
                best_neighbor = neighbor
                best_neighbor_cost = cost

        if not best_neighbor:
            break  # aucun voisin admissible

        current_solution = best_neighbor
        tabu_list.append(tuple(current_solution[1:-1]))
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

        if best_neighbor_cost < best_cost:
            best_solution = list(best_neighbor)
            best_cost = best_neighbor_cost

    return best_solution


# -------- Déploiement de l'ordre des key nodes vers la route complète --------
def expand_order_to_full_route(order, nxt, shortest_dist):
    """
    Déploie l'ordre de key nodes en itinéraire réel (tous les nœuds intermédiaires).
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
            # pas de chemin disponible : retourner la route construite jusqu'à présent
            print(f"⚠️ Pas de chemin entre {u} et {v} selon shortest_dist.")
            return full, total
        segment = reconstruct_path(u, v, nxt)
        if not segment:
            print(f"⚠️ Impossible de reconstruire le segment {u}->{v}.")
            return full, total
        # éviter duplication du nœud précédemment ajouté
        if full and segment[0] == full[-1]:
            segment = segment[1:]
        full.extend(segment)
        total += shortest_dist[u][v]
    return full, total


# -------- Répartition simple des clients sur les camions --------
def assign_clients_to_trucks(deliveries, nb_trucks):
    trucks = {i: [] for i in range(nb_trucks)}
    for idx, client in enumerate(deliveries):
        truck_id = idx % nb_trucks
        trucks[truck_id].append(client)
    return trucks


# -------- Exécution principale --------
def algoTaboo():
    # génération de l'instance
    graph = generatorInstance()
    # matrice et plus courts chemins
    dist = build_distance_matrix(graph)
    shortest_dist, nxt = floyd_warshall_with_next(dist)

    # extraction des données
    pickups, deliveries, mapping = extract_delivery_data(graph)

    # filtrer les clients sans dépôt associé (pour éviter exceptions)
    filtered_deliveries = []
    missing = []
    for city_name, client_name, objs in deliveries:
        if mapping.get(client_name):
            filtered_deliveries.append((city_name, client_name, objs))
        else:
            missing.append((city_name, client_name, objs))
    if missing:
        print("⚠️ Certains clients n'ont aucun dépôt associé ; ils seront ignorés pour cette exécution.")
        for city_name, client_name, objs in missing:
            print(f"  - {client_name} à {city_name} (objets : {[(o.type, o.name) for o in objs]})")

    if not filtered_deliveries:
        raise ValueError("Aucune livraison valide (tous les clients ont des demandes non satisfaites).")

    # affectation clients->camions (round-robin)
    trucks_clients = assign_clients_to_trucks(filtered_deliveries, NB_TRUCKS)

    # pour chaque camion, construire ses tournées
    for truck_id, clients in trucks_clients.items():
        if not clients:
            print(f"\n=== CAMION {truck_id} : aucun client assigné ===")
            continue

        print(f"\n=== CAMION {truck_id} ===")
        truck_route_nodes = []
        truck_full_route = []
        truck_total_distance = 0.0

        # vérifier et choisir dépôt initial (premier pickup du premier client)
        first_client_name = clients[0][1]
        if not mapping.get(first_client_name):
            print(f"⚠️ Le client initial {first_client_name} n'a pas de dépôt — camion ignoré.")
            continue
        start_city_initial = mapping[first_client_name][0]
        last_position = start_city_initial

        for client_data in clients:
            end_city, client_name, demanded_objs = client_data
            relevant_pickups = list(dict.fromkeys(mapping.get(client_name, [])))  # unique + préservation ordre

            # si aucun dépôt pour ce client, on passe
            if not relevant_pickups:
                print(f"⚠️ Client {client_name} ignoré (aucun dépôt).")
                continue

            # Recherche Tabou : optimiser l'ordre des pickups (key nodes)
            order_nodes = tabu_search_on_key_nodes(
                last_position,
                relevant_pickups,
                end_city,
                shortest_dist,
                max_iter=TABU_MAX_ITER,
                tabu_tenure=TABU_TENURE
            )

            # Déploiement de l'ordre en route complète (avec nœuds intermédiaires)
            full_route, total_distance = expand_order_to_full_route(order_nodes, nxt, shortest_dist)

            # mise à jour de la position et accumulation
            if full_route:
                last_position = full_route[-1]
                truck_route_nodes.extend(order_nodes)
                # éviter duplication quand on concatène segments
                if not truck_full_route:
                    truck_full_route.extend(full_route)
                else:
                    # si le premier élément du nouveau segment est identique à la dernière ville actuelle,
                    # on skip le premier pour éviter duplication
                    if full_route[0] == truck_full_route[-1]:
                        truck_full_route.extend(full_route[1:])
                    else:
                        truck_full_route.extend(full_route)
                truck_total_distance += total_distance

        # retour au dépôt initial si nécessaire
        if last_position != start_city_initial:
            order_back = tabu_search_on_key_nodes(last_position, [], start_city_initial, shortest_dist)
            full_back, dist_back = expand_order_to_full_route(order_back, nxt, shortest_dist)
            if full_back:
                if full_back[0] == truck_full_route[-1]:
                    truck_full_route.extend(full_back[1:])
                else:
                    truck_full_route.extend(full_back)
                truck_total_distance += dist_back

        # affichage synthétique
        # print("Key-nodes visités (séquences accumulées) :")
        # print(" -> ".join(truck_route_nodes) if truck_route_nodes else "(aucun)")
        # print("Route complète parcourue :")
        # print(" -> ".join(truck_full_route) if truck_full_route else "(aucune)")
        print(f"Distance totale estimée pour camion {truck_id} : {truck_total_distance:.2f} km")
    return truck_total_distance, truck_full_route

