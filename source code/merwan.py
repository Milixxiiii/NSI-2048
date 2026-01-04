def menu():
    print("1 : Lancer la partie")
    print("2 : Changer le thème")
    print("3 : Tableau des scores")
    print("4 : Crédits")
    choix = input("Faites votre choix entre 1 et 4 : ")
    if choix == "1":
        print("La partie commence...")
        # Lancer la partie
    elif choix == "2":
        print ("Changement du thème...")
        # Changer le thème
    elif choix == "3":
        print("Affichage des scores...")
        # Afficher les scores
    elif choix == "4":
        print ("Crédits")
        # Afiicher les crédits
    else:
        print("Choix invalide !")
        menu()
        # Relance le menu
