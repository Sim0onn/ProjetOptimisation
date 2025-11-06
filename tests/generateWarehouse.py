from src.utils.generators.generatorWarehouse import generatorWarehouse


print("Génération des objets...")
datas = generatorWarehouse()
print("Objets générés :")
datas.printStock()