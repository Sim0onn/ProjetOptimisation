"""
genetic_workflow_optimized.py
-------------------
Script autonome : génère l'instance (via generatorInstance),
construit les matrices de distances, extrait les clients et dépôts,
puis calcule des tournées par camion en utilisant un Algorithme Génétique
optimisé pour l'ordre des key nodes (dépôt -> pickups -> client).

Auteur : Rubens
Langue : français soutenu
"""

import random
from math import inf
from typing import List, Tuple
from src.utils.generators.generatorInstance import generatorInstance

# ----------------- paramètres globaux -----------------
NB_TRUCKS = 10
RANDOM_SEED = 4
random.seed(RANDOM_SEED)

# GA paramétrage amélioré
GA_POP_SIZE = 100
GA_GENERATIONS = 150
GA_CROSSOVER_RATE = 0.85
GA_MUTATION_RATE = 0.35
GA_TOURNAMENT_SIZE = 3
GA_ELITE_SIZE = 3  # garder les 3 meilleurs à chaque génération

# ----------------- utilitaires graphe / distance -----------------
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
    nxt = {u: {v: (v if d[u][v] < inf else None) for v in nodes} for u in nodes}
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

def reconstruct_path(u: str, v: str, nxt) -> List[str]:
    if u not in nxt or nxt[u].get(v) is None:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path

# ----------------- extraction clients / pickups / mapping -----------------
def extract_delivery_data(graph):
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

# ----------------- algorithme génétique amélioré -----------------
def fitness_of_permutation(start: str, perm: List[str], end: str, shortest_dist) -> float:
    route = [start] + perm + [end]
    total = 0.0
    for i in range(len(route) - 1):
        total += shortest_dist[route[i]].get(route[i+1], inf)
    return total

def nearest_neighbor_order(start: str, nodes: List[str], shortest_dist) -> List[str]:
    """Heuristique gloutonne pour générer un individu initial."""
    if not nodes:
        return []
    remaining = set(nodes)
    current = start
    order = []
    while remaining:
        next_node = min(remaining, key=lambda x: shortest_dist[current][x])
        order.append(next_node)
        remaining.remove(next_node)
        current = next_node
    return order

def tournament_selection(population: List[List[str]], fitnesses: List[float], k: int) -> List[str]:
    best = None
    best_f = inf
    for _ in range(k):
        idx = random.randrange(len(population))
        if fitnesses[idx] < best_f:
            best_f = fitnesses[idx]
            best = population[idx]
    return list(best)

def ordered_crossover(parent1: List[str], parent2: List[str]) -> Tuple[List[str], List[str]]:
    n = len(parent1)
    if n < 2:
        return list(parent1), list(parent2)
    a, b = sorted(random.sample(range(n), 2))
    child1 = [None]*n
    child2 = [None]*n
    child1[a:b+1] = parent1[a:b+1]
    child2[a:b+1] = parent2[a:b+1]
    def fill(child, donor):
        pos = (b+1)%n
        donor_pos = (b+1)%n
        while None in child:
            if donor[donor_pos] not in child:
                child[pos] = donor[donor_pos]
                pos = (pos+1)%n
            donor_pos = (donor_pos+1)%n
        return child
    return fill(child1, parent2), fill(child2, parent1)

def swap_mutation(individual: List[str], mutation_rate: float) -> List[str]:
    indiv = list(individual)
    if random.random() < mutation_rate and len(indiv)>=2:
        i,j=random.sample(range(len(indiv)),2)
        indiv[i],indiv[j]=indiv[j],indiv[i]
    return indiv

def inversion_mutation(individual: List[str], mutation_rate: float) -> List[str]:
    indiv = list(individual)
    if random.random() < mutation_rate and len(indiv) >= 2:
        i, j = sorted(random.sample(range(len(indiv)), 2))
        indiv[i:j+1] = reversed(indiv[i:j+1])
    return indiv

def genetic_optimize_pickups(start: str, pickups: List[str], end: str, shortest_dist,
                             pop_size=GA_POP_SIZE, generations=GA_GENERATIONS,
                             crossover_rate=GA_CROSSOVER_RATE, mutation_rate=GA_MUTATION_RATE,
                             tournament_k=GA_TOURNAMENT_SIZE, elite_size=GA_ELITE_SIZE) -> List[str]:
    if not pickups:
        return [start,end]
    # population initiale : 50% aléatoire, 50% heuristique nearest neighbor
    population = [random.sample(pickups, len(pickups)) for _ in range(pop_size//2)]
    population += [nearest_neighbor_order(start, pickups, shortest_dist) for _ in range(pop_size - len(population))]
    fitnesses = [fitness_of_permutation(start, ind, end, shortest_dist) for ind in population]

    best_idx = min(range(len(population)), key=lambda i: fitnesses[i])
    best_sol = list(population[best_idx])
    best_cost = fitnesses[best_idx]

    stagnant = 0
    for gen in range(generations):
        new_pop = sorted(population, key=lambda i: fitness_of_permutation(start, i, end, shortest_dist))[:elite_size]
        while len(new_pop) < pop_size:
            parent1 = tournament_selection(population, fitnesses, tournament_k)
            parent2 = tournament_selection(population, fitnesses, tournament_k)
            if random.random() < crossover_rate:
                child1, child2 = ordered_crossover(parent1, parent2)
            else:
                child1, child2 = list(parent1), list(parent2)
            # mutation adaptative
            mrate = mutation_rate * (1.5 if stagnant>10 else 1.0)
            child1 = swap_mutation(child1, mrate)
            child2 = swap_mutation(child2, mrate)
            child1 = inversion_mutation(child1, mrate)
            child2 = inversion_mutation(child2, mrate)
            new_pop.append(child1)
            if len(new_pop)<pop_size: new_pop.append(child2)
        population = new_pop
        fitnesses = [fitness_of_permutation(start, ind, end, shortest_dist) for ind in population]
        cur_best_idx = min(range(len(population)), key=lambda i: fitnesses[i])
        if fitnesses[cur_best_idx] < best_cost:
            best_cost = fitnesses[cur_best_idx]
            best_sol = list(population[cur_best_idx])
            stagnant = 0
        else:
            stagnant += 1
    return [start] + best_sol + [end]

# ----------------- déploiement en route réelle -----------------
def expand_order_to_full_route(order: List[str], nxt, shortest_dist) -> Tuple[List[str], float]:
    if not order: return [], 0.0
    full = [order[0]]
    total = 0.0
    for i in range(len(order)-1):
        u, v = order[i], order[i+1]
        if shortest_dist[u].get(v, inf)==inf: return full, total
        segment = reconstruct_path(u,v,nxt)
        if full and segment[0]==full[-1]: segment=segment[1:]
        full.extend(segment)
        total+=shortest_dist[u][v]
    return full,total

# ----------------- répartition clients->camions -----------------
def assign_clients_to_trucks(deliveries, nb_trucks):
    trucks = {i: [] for i in range(nb_trucks)}
    for idx, client in enumerate(deliveries):
        truck_id = idx%nb_trucks
        trucks[truck_id].append(client)
    return trucks

# ----------------- exécution principale -----------------
def main():
    graph = generatorInstance()
    dist = build_distance_matrix(graph)
    shortest_dist, nxt = floyd_warshall_with_next(dist)

    pickups, deliveries, mapping = extract_delivery_data(graph)

    filtered_deliveries = []
    for city_name, client_name, objs in deliveries:
        if mapping.get(client_name):
            filtered_deliveries.append((city_name, client_name, objs))
    if not filtered_deliveries:
        raise ValueError("Aucune livraison valide.")

    trucks_clients = assign_clients_to_trucks(filtered_deliveries, NB_TRUCKS)

    for truck_id, clients in trucks_clients.items():
        if not clients: continue
        truck_total_distance = 0.0
        last_position = mapping[clients[0][1]][0]
        for end_city, client_name, objs in clients:
            relevant_pickups = list(dict.fromkeys(mapping[client_name]))
            if not relevant_pickups: continue
            order_nodes = genetic_optimize_pickups(last_position, relevant_pickups, end_city, shortest_dist)
            full_route, dist_route = expand_order_to_full_route(order_nodes, nxt, shortest_dist)
            if full_route: last_position=full_route[-1]; truck_total_distance+=dist_route
        # retour au dépôt initial
        start_city_initial = mapping[clients[0][1]][0]
        if last_position!=start_city_initial:
            back_order = [last_position,start_city_initial]
            full_back, dist_back = expand_order_to_full_route(back_order, nxt, shortest_dist)
            truck_total_distance += dist_back
        print(f"Distance totale estimée pour camion {truck_id} : {truck_total_distance:.2f} km")

if __name__=="__main__":
    main()
