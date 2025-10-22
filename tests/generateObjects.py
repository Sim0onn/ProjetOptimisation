from src.utils.generators.generatorObjects import generatorObjects

print("Génération des objets...")
datas = generatorObjects(10)
print("Objets générés :")
datas.printStock()