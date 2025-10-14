class Graph : 
    def __init__(self,n):
        self.n = n
        self.adj = {}

    def add_edge(self, u, v, w):
        # Si le sommet u n'existe pas encore, on l'initialise
        if u not in self.adj:
            self.adj[u] = []
        # Si le sommet v n'existe pas encore, on l'initialise aussi
        if v not in self.adj:
            self.adj[v] = []

        # Ajouter l'arête u -> v
        self.adj[u].append((v, w))
        # Si ton graphe est non orienté, ajoute aussi v -> u
        self.adj[v].append((u, w))


    def print_neighbors(self):
        for ville, voisins in self.adj.items():
            print(ville, ":", voisins)