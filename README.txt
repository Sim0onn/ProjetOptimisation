Commandes utiles :
lancer un code de test : python -m tests.nomDuFichierSansExtension
exemple : python -m tests.generateTrafficTest

Dépendances :
pip install dotenv
pip install pandas

execution :

- lancer "py fixtures/fixtures.py", cela vas générer les instances dans les CSV
- executer "py main.py", pour lancer les algos
- (optionel) modifier les variables dans le .env pour changer le fichier d'entrée, NB_INSTANCES correspond au fichier d'entrée,
exemple : NB_INSTANCES = 6 correspond aux fichiers graph_6.csv, objects_6.csv et cities_6.csv




