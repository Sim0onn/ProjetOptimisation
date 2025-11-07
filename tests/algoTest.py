from math import inf
from src.utils.generators.generatorInstance import generatorInstance

graph = generatorInstance('fixtures/graphs/graph_10.csv', 10)
nb_trucks = 3


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



def greedy_on_key_nodes(start, pickups, deliveries, shortest_dist):
    """
    Heuristique gloutonne sur le graphe contracté des 'key nodes' en utilisant shortest_dist.
    Retourne une liste ordonnée de key nodes (p.ex. [start, p1, p2, ..., delivery]).
    """
    key_nodes = [start] + list(set(pickups) | set(deliveries))
    current = start
    remaining = set(pickups) | set(deliveries)
    order = [start]

    while remaining:
        # ne garder que les candidats atteignables (distance finie)
        candidates = [c for c in remaining if shortest_dist[current].get(c, inf) < inf]
        if not candidates:
            print(f"⚠️ Aucune ville d'intérêt atteignable depuis {current} (sur key_nodes). Arrêt.")
            break
        next_node = min(candidates, key=lambda c: shortest_dist[current][c])
        order.append(next_node)
        remaining.discard(next_node)
        current = next_node

    # s'assurer que la livraison finale est dans l'ordre (si elle était dans deliveries)
    for d in deliveries:
        if d not in order:
            if shortest_dist[current].get(d, inf) < inf:
                order.append(d)
            else:
                print(f"⚠️ Impossible d'ajouter la livraison finale {d} depuis {current} (inatteignable).")
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














# -------------------- Exécution --------------------

dist = build_distance_matrix(graph)
shortest_dist, nxt = floyd_warshall_with_next(dist)

pickup_cities, deliveries, mapping = extract_delivery_data(graph)
if not pickup_cities or not deliveries:
    raise ValueError("Aucune donnée de livraison disponible.")

# Sélection d’un couple dépôt ↔ client logique
start_city, end_city = choose_start_and_end(pickup_cities, deliveries)
client_name = deliveries[0][1]
demanded_objs = deliveries[0][2]

print(f"\n=== PLAN CLIENT ===")
print(f"Départ depuis le dépôt : {start_city}")
print(f"Livraison pour le client : {client_name}")
print(f"Ville du client : {end_city}")
print(f"Objets demandés : {[f'{o.type}:{o.name}' for o in demanded_objs]}")
print(f"Provenance possible : {mapping[client_name]}")

delivery_cities = [end_city]


# 1) calculer l'ordre sur les nœuds d'intérêt (pickups + delivery) via shortest_dist
order_nodes = greedy_on_key_nodes(start_city, pickup_cities, delivery_cities, shortest_dist)

# 2) déployer en route réelle (avec intermédiaires)
full_route, total_distance = expand_order_to_full_route(order_nodes, nxt, shortest_dist)

print("\n=== ORDER (key nodes) ===")
print(" -> ".join(order_nodes))
print("\n=== ROUTE COMPLETE ===")
print(" -> ".join(full_route))
print(f"Distance totale estimée : {total_distance:.2f} km")
