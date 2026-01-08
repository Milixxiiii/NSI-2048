scores = []

def lancer_partie():
    print("La partie commence...")
    scores.append(2048)

def changer_theme():
    print("Thème changé")

def afficher_scores():
    if not scores:
        print("Aucun scores")
    else:
        for s in scores:
            print("Scores :", s)

def credits():
    print("Jeu codé par Milo, Naïl et Merwan")

def menu():
    print(""" 
    ___MENU___
    1 : Lancer la partie
    2 : Changer de thème
    3 : Tableau des scores
    4 : Crédits
    0 : Quitter
    """)
    
    choix = input("Faites votre choix entre 0 et 4 : ")
    
    if choix == "1":
        lancer_partie()
        # Lancer la partie
    elif choix == "2":
        changer_theme()
        # Changer le thème
    elif choix == "3":
        afficher_scores()
        # Afficher les scores
    elif choix == "4":
        credits()
        # Afiicher les crédits
    elif choix == "0":
        print("Au revoir !")    #Affiche le message de fermeture
        return
    else:
        print("Choix invalide !")
        # Affiche un message d'erreur

    input("\nEntrée pour revenir au menu...")
    menu()

menu()
