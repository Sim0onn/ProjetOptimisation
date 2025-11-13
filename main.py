import time
import matplotlib.pyplot as plt
import pandas as pd
from src.utils.commands import update_env_seed
from src.utils.algorithms.algoGenetics import algoGenetics
from src.utils.algorithms.algoTaboo import algoTaboo

def run_executions(nb):
    results = []

    for i in range(nb):
        print(f"----------------------- itération {i} -----------------------")
        update_env_seed(i)

        # --- Tabou ---
        start = time.time()
        taboo_distance, taboo_route = algoTaboo()
        taboo_time = time.time() - start
        print(f"Tabou → {taboo_distance:.2f} km en {taboo_time:.2f}s")

        results.append({
            "iteration": i,
            "algo": "Tabou",
            "distance": taboo_distance,
            "time": taboo_time
        })

        # --- Génétique ---
        start = time.time()
        genetics_distance, genetics_route = algoGenetics()
        genetics_time = time.time() - start
        print(f"Génétique → {genetics_distance:.2f} km en {genetics_time:.2f}s")

        results.append({
            "iteration": i,
            "algo": "Génétique",
            "distance": genetics_distance,
            "time": genetics_time
        })

    df = pd.DataFrame(results)
    return df


# --- Exécution ---
df_results = run_executions(20)

# Résumé statistique directement affiché
print("\n--- Statistiques globales ---")
print(df_results.groupby("algo")[["distance", "time"]].agg(["mean", "std", "min", "max"]))

# --- Graphiques ---
plt.figure(figsize=(6,4))
df_results.boxplot(column="distance", by="algo")
plt.title("Distribution des distances par algorithme")
plt.suptitle("")
plt.ylabel("Distance (km)")
plt.show()

plt.figure(figsize=(6,4))
df_results.boxplot(column="time", by="algo")
plt.title("Distribution des temps d'exécution par algorithme")
plt.suptitle("")
plt.ylabel("Temps (s)")
plt.show()

