from src.utils.generators.generatorObjects import generatorObjects

print("Génération des objets...")
datas = generatorObjects(10, 'objects_160.csv')
print("Objets générés :")
datas.printStock()