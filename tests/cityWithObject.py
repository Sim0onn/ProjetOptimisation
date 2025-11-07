from src.utils.generators.generatorGraph import generatorGraph

def main():
    graph = generatorGraph()
    object_type = "Corrosive"
    object_name = "Object_00004"
    city_with_object = graph.getCityFromWarehouses(object_type, object_name)

    if city_with_object:
        print(f"\n La ville '{city_with_object.getName()}' possède l'objet '{object_name}' de type '{object_type}' dans ses entrepôts.")
        warehouses = city_with_object.returnWarehouse()
        for w in warehouses:
            print(f"Type: {w.type}, Name: {w.name}")
    else:
        print(f"\n Aucune ville ne possède l'objet '{object_name}' de type '{object_type}' dans ses entrepôts.")

if __name__ == "__main__":
    main()
