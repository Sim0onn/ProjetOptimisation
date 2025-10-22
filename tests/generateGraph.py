from src.utils.generators.generatorGraph import generatorGraph

def main():
    # 1️⃣ Génération d'un graphe aléatoire
    graph = generatorGraph(10)  # Choisir 10 villes aléatoires pour le test
    print("✅ Graphe généré avec", graph.getDegree(), "villes.")

    # 2️⃣ Afficher toutes les villes
    print("\n📍 Liste des villes :")
    for city_name in graph.getAllCities():
        city = graph.getCity(city_name)
        print(f" - {city.getName()} ({city.numberOfWarehouses()} entrepôts)")

    # 3️⃣ Afficher toutes les routes
    print("\n🛣️ Liste des routes :")
    for road in graph.getAllRoads():
        print(f" - {road.getStartCity().getName()} -> {road.getEndCity().getName()} : {road.getDistance()} km")

    # 4️⃣ Tester le degré (nombre de connexions) d'une ville
    test_city = graph.getAllCities()[0]  # Prendre la première ville de la liste
    degree = graph.getDegreeNode(test_city)
    print(f"\n🔸 La ville '{test_city}' a {degree} routes sortantes.")

    # 5️⃣ Afficher les routes partant d'une ville
    print(f"\n🚏 Routes partant de '{test_city}':")
    for road in graph.getRoadsFrom(test_city):
        print(f"   -> {road.getEndCity().getName()} ({road.getDistance()} km)")

    # 6️⃣ Tester la gestion des entrepôts
    city_obj = graph.getCity(test_city)
    print(f"\n🏬 Entrepôts à {test_city} : {city_obj.numberOfWarehouses()} entrepôt(s).")
    print("📦 Stock du premier entrepôt :", city_obj.returnWarehouse())

    # 7️⃣ Ajouter une ville et une route manuellement
    print("\n➕ Ajout manuel d'une nouvelle ville 'TESTVILLE' et d'une route vers", test_city)
    graph.addCity("TESTVILLE")
    graph.addRoad("TESTVILLE", test_city, 42.0)

    # Vérification après ajout
    print("Villes après ajout :", graph.getAllCities())
    print("Routes après ajout :")
    for road in graph.getAllRoads():
        print(f" - {road.getStartCity().getName()} -> {road.getEndCity().getName()} : {road.getDistance()} km")

    # 8️⃣ Représentation textuelle du graphe
    print("\n🖼️ Représentation textuelle du graphe :")
    print(graph)

    # 9️⃣ Recherche d'une ville possédant un objet spécifique dans ses entrepôts
    object_type = "Food"
    object_name = "Milk"
    city_with_object = graph.getCityFromWarehouses(object_type, object_name)
    if city_with_object:
        print(f"\n🔍 La ville '{city_with_object}' possède l'objet '{object_name}' de type '{object_type}' dans ses entrepôts.")
    else:
        print(f"\n🔍 Aucune ville ne possède l'objet '{object_name}' de type '{object_type}' dans ses entrepôts.")

if __name__ == "__main__":
    main()
