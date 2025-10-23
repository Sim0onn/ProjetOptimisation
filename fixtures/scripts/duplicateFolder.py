# Fichier à enregistrer sous : scripts/file_duplicator.py

import os
import glob
import shutil

def duplicateFolder(source_directory_name: str, destination_directory_name: str):

    if not os.path.isdir(source_directory_name):
        print(f"ERREUR : Le dossier source '{source_directory_name}' est introuvable.")
        return

    if not os.path.isdir(destination_directory_name):
        print(f"Le dossier de destination '{destination_directory_name}' n'existe pas. Création en cours...")
        try:
            os.makedirs(destination_directory_name)
        except OSError as e:
            print(f"ERREUR : Impossible de créer le dossier de destination '{destination_directory_name}': {e}")
            return
            
    search_pattern = os.path.join(source_directory_name, '*.csv')
    csv_files_to_copy = glob.glob(search_pattern)
    
    if not csv_files_to_copy:
        print(f"Aucun fichier CSV à copier n'a été trouvé dans '{source_directory_name}'.")
        return

    #print(f"\nDébut de la copie de {len(csv_files_to_copy)} fichier(s) depuis '{source_directory_name}' vers '{destination_directory_name}'...")
    
    files_copied_count = 0
    for source_file_path in csv_files_to_copy:
        try:
            file_name = os.path.basename(source_file_path)
            destination_file_path = os.path.join(destination_directory_name, file_name)
            
            shutil.copy2(source_file_path, destination_file_path)
            #print(f"  -> Copié : {file_name}")
            files_copied_count += 1
        except Exception as e:
            print(f"ERREUR lors de la copie du fichier {source_file_path}: {e}")

    #print(f"\n--- Opération de duplication terminée. {files_copied_count} fichier(s) copié(s) avec succès. ---")
