import csv
import os

def numberOfWarehouses(chemin_fichier: str) -> int:
    
    total_warehouses = 0

    if not os.path.exists(chemin_fichier):
        print(f"ERREUR : Le fichier '{chemin_fichier}' est introuvable.")
        return -1

    try:
        with open(chemin_fichier, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            
            if 'Nb_warehouses' not in reader.fieldnames:
                print(f"ERREUR : La colonne 'Nb_warehouses' n'a pas été trouvée dans le fichier '{chemin_fichier}'.")
                return -1

            for ligne in reader:
                try:
                    nombre_depots = int(ligne['Nb_warehouses'])
                    total_warehouses += nombre_depots
                except (ValueError, TypeError):
                    print(f"AVERTISSEMENT : Ligne ignorée car la valeur n'est pas un nombre valide : {ligne}")
                    continue
        return total_warehouses

    except Exception as e:
        print(f"Une erreur inattendue est survenue lors de la lecture du fichier : {e}")
        return -1
