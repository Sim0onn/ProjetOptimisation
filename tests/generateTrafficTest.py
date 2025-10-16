from src.utils.generators.generatorGraph import generatorGraph
from src.utils.utilsTraffic import generateTrafficGraphs

def main():
    # Générer le graphe de base avec 20 villes
    print("Génération du graphe de base...")
    base_graph = generatorGraph(20)
    print("Graphe de base généré :")
    print(base_graph)

    # Générer les graphes en fonction du trafic
    print("\nGénération des graphes en fonction du trafic...")


    traffic_graphs = generateTrafficGraphs(base_graph)


    # Afficher les graphes générés
    for i, traffic_graph in enumerate(traffic_graphs):
        print(f"\n--- Graphe pour l'heure {8 + i}h ---")
        print(traffic_graph)

if __name__ == "__main__":
    main()