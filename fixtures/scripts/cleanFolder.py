import os
import glob

def cleanFolder(directory_path: str, file_pattern: str):

    if not os.path.isdir(directory_path):
        print(f"Le dossier '{directory_path}' n'existe pas encore. Il sera créé.")
        return

    search_path = os.path.join(directory_path, file_pattern)
    files_to_delete = glob.glob(search_path)

    if not files_to_delete:
        print(f"Le dossier '{directory_path}' est déjà vide (aucun fichier '{file_pattern}' trouvé).")
        return
    
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"ERREUR lors de la suppression du fichier {file_path}: {e}")