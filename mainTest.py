from src.classes.graph import Graph
from src.utils import generateTrafficGraphs
from main import graphGenerator

def main():
    base_graph = graphGenerator(20)

    traffic_graphs = generateTrafficGraphs(base_graph)

    for i, traffic_graph in enumerate(traffic_graphs):
        print(f"Graphe pour l'heure {8 + i}h :")
        print(traffic_graph)

if __name__ == "__main__":
    main()