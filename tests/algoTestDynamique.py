from math import inf
from src.utils.generators.generatorInstance import generatorInstance
from src.utils.utilsTraffic import generateTrafficGraphs

VITESSE_BASE = 60  # km/h
nb_trucks = 3

graph = generatorInstance()
traffic_graphs = generateTrafficGraphs(graph)  # 11 tranches horaires

# -------------------- Fonctions classiques --------------------

def build_distance_matrix(graph):
    cities = list(graph.getCities().keys())
    dist = {u: {v: inf for v in cities} for u in cities}
    for u in cities:
        dist[u][u] = 0.0
    for road in graph.getAllRoads():
        c1 = road.getCity1().getName().strip()
        c2 = road.getCity2().getName().strip()
        d = road.getDistance()
        if d < dist[c1].get(c2, inf):
            dist[c1][c2] = d
            dist[c2][c1] = d
    return dist

def floyd_warshall_with_next(dist):
    nodes = list(dist.keys())
    d = {u: {v: dist[u][v] for v in nodes} for u in nodes}
    nxt = {u: {v: (v if d[u][v]<inf else None) for v in nodes} for u in nodes}
    for k in nodes:
        for i in nodes:
            if d[i][k] == inf: continue
            for j in nodes:
                if d[k][j] == inf: continue
                via = d[i][k] + d[k][j]
                if via < d[i][j]:
                    d[i][j] = via
                    nxt[i][j] = nxt[i][k]
    return d, nxt

def reconstruct_path(u, v, nxt):
    if u not in nxt or nxt[u].get(v) is None:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path

def extract_delivery_data(graph):
    pickups = set()
    deliveries = []
    mapping = {}
    for city_name, city_obj in graph.getCities().items():
        if not getattr(city_obj, "customers", []): continue
        for customer in city_obj.customers:
            cname = getattr(customer, "name", "?")
            objs = getattr(customer, "objects", [])
            deliveries.append((city_name, cname, objs))
            mapping[cname] = []
            for obj in objs:
                for city2, city_obj2 in graph.getCities().items():
                    for wh in getattr(city_obj2, "warehouses", []):
                        for wh_obj in getattr(wh, "stock", []):
                            if wh_obj.type==obj.type and wh_obj.name==obj.name:
                                pickups.add(city2)
                                mapping[cname].append(city2)
    return list(pickups), deliveries, mapping

def greedy_on_key_nodes(start, pickups, end_city, shortest_dist):
    key_nodes = [start] + list(pickups) + [end_city]
    current = start
    remaining = set(pickups)
    order = [start]
    while remaining:
        candidates = [c for c in remaining if shortest_dist[current].get(c, inf)<inf]
        if not candidates: break
        next_node = min(candidates, key=lambda c: shortest_dist[current][c])
        order.append(next_node)
        remaining.discard(next_node)
        current = next_node
    if shortest_dist[current].get(end_city, inf)<inf:
        order.append(end_city)
    return order

def expand_order_to_full_route(order, nxt, shortest_dist):
    if not order: return [], 0.0
    full = [order[0]]
    total = 0.0
    for i in range(len(order)-1):
        u,v = order[i], order[i+1]
        segment = reconstruct_path(u,v,nxt)
        if not segment: return full, total
        if full and segment[0]==full[-1]: segment=segment[1:]
        full.extend(segment)
        total += shortest_dist[u][v]
    return full, total

def assign_clients_to_trucks(deliveries, nb_trucks):
    trucks = {i: [] for i in range(nb_trucks)}
    for idx, client in enumerate(deliveries):
        trucks[idx % nb_trucks].append(client)
    return trucks

def get_time_slot(hour):
    hour = max(8, min(hour, 18))
    return min(int(hour)-8, 10)

# -------------------- Préparation des routes --------------------

dist = build_distance_matrix(graph)
shortest_dist, nxt = floyd_warshall_with_next(dist)
pickup_cities, deliveries, mapping = extract_delivery_data(graph)
trucks_clients = assign_clients_to_trucks(deliveries, nb_trucks)

trucks_routes = {}
for truck_id, clients in trucks_clients.items():
    route_nodes = []
    for client in clients:
        end_city, cname, _ = client
        relevant_pickups = mapping[cname]
        start_city = route_nodes[-1] if route_nodes else relevant_pickups[0]
        order_nodes = greedy_on_key_nodes(start_city, relevant_pickups, end_city, shortest_dist)
        full_route,_ = expand_order_to_full_route(order_nodes,nxt,shortest_dist)
        route_nodes.extend(full_route[1:] if route_nodes else full_route)
    trucks_routes[truck_id] = route_nodes

# -------------------- Simulation journalière corrigée --------------------

trucks_state = {tid:{'hour':8.0,'route_idx':0} for tid in trucks_routes}
day_count = 1
clients_remaining = {tid:list(clients) for tid,clients in trucks_clients.items()}

while any(clients_remaining.values()):
    print(f"\n--- JOUR {day_count} ---")
    for truck_id, clients in clients_remaining.items():
        truck = trucks_state[truck_id]
        route_full = trucks_routes[truck_id]
        current_hour = truck['hour']
        idx = truck['route_idx']
        day_route = []

        while idx < len(route_full)-1:
            u, v = route_full[idx], route_full[idx+1]
            slot = get_time_slot(current_hour)
            g = traffic_graphs[slot]

            # temps de trajet selon le graphe horaire
            distance = dist[u][v]  # distance du graphe statique
            traffic_factor = g.getWeight(u,v)/distance if distance>0 else 1.0
            segment_time = (distance / VITESSE_BASE) * traffic_factor

            if current_hour + segment_time > 18.0:
                # fin de journée
                truck['hour'] = 8.0
                truck['route_idx'] = idx
                break

            current_hour += segment_time
            day_route.append(v)
            idx += 1

        else:
            # fin de route
            truck['hour'] = current_hour
            truck['route_idx'] = idx
            if clients: clients.pop(0)  # client livré

        print(f"Camion {truck_id} : {' -> '.join(day_route)} (heure finale {truck['hour']:.2f})")

    day_count += 1
