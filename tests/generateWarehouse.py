from src.utils.generators.generatorWarehouse import generatorWarehouse

print("Génération des objets...")
datas = generatorWarehouse(10, 'objects_100.csv')
print("Objets générés :")
datas.printStock()