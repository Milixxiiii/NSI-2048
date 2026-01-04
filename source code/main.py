#on importe les modules nécessaires

from pathlib import Path
from random import choice, randint
from copy import deepcopy
import time
import os
import tkinter as tk

#on définit des varibles de base

taille_grille = 4
bg = "#DBA2D9"
default_proba = "90% - 10%"
default_touches = "zqsd"
proba = [2 for i in range(int(default_proba[0]))] + [4 for i in range(int(default_proba[-3]))]
icon_path = Path(__file__).parent.parent / "ressources" / "icone.ico"


#fonction affichage de la grille dans la console
def afficheGrille(grille):
    os.system("cls")
    for x in grille:
        print(x)



#fonction qui sélectionne les zéros
def select_zero(liste):

    """ retourne les coordonnées 0 d'une matrice(grille) sous forme d'une liste de tuples

    Args:
        liste : grille des 2048 sous la forme d'une liste de liste
 
    """

    case_zero = []

    for x in range(len(liste)):
        for element in range(len(liste[x])):
            if liste[x][element] == 0:
                case_zero.append((x, element))

    return case_zero

#fonction qui initialise le jeu en créant la varible de départ
def initialisation(taille):

    """retourne une liste représentant un jeu de 2048
    
    args:
        taille: taille de la grille avec laquelle on veut jouer

    
    """
    #on crée la grille de jeu
    grille_jeu = [[0 for y in range(taille)] for x in range(taille)]

    #on execute la boucle 2 fois pour que les 2 cubes de base apparaissent :
    for i in range(2):

        #on sélectionne une case vide au hasard
        vide = select_zero(grille_jeu)
        remplacement = choice(vide)

        #on remplace la case choisi par un bloc aléatoire
        grille_jeu[remplacement[0]][remplacement[1]] = choice(proba)
    
    #on renvoie la grille de jeu généré
    return grille_jeu


#fonction d'apparition d'un cube
def apparition(grille):
    """fait apparaitre un chiffre à un endroit aléatoire de la grille
    
    args:
        grille: grille actuelle du jeu
    """

    #creation de la nouvelle grille:

    #on choisit une case vide au hasard:
    vide = select_zero(grille)
    nouvelle_case = choice(vide)

    #on fait apparaitre un nouveau chiffre sur cette case et on retourn la nouvelle grille :
    grille[nouvelle_case[0]][nouvelle_case[1]] = choice(proba)




#fonction qui déplace les cubes vers la gauche sur une ligne
def mouvement_ligne(ligne):

    """retourne une liste et fusionne certains cubes à la mannière d'un 2048

    args:
        ligne: la ligne à laquelle on veut faire effectuer le déplacement
    """

    #nouvelle variables : une temporaire sans les 0(cases vides) et la nouvelle
    ligne_temp = [x for x in ligne if x != 0]
    nvl_ligne = []

    #boucles qui gère l'addition des termes ou non
    i = 0    
    while i < len(ligne_temp):
        valeur = ligne_temp[i]
        if i == len(ligne_temp)-1:              #si c'est la dernière itération ajoute la dernière valeur à nvl_ligne
            nvl_ligne.append(ligne_temp[i])
            i += 1
        elif valeur == ligne_temp[i+1]:         #si la valeur concerné et la suivante sont la même on ajoute la somme à nvl_lignes
            nvl_ligne.append(valeur*2)          #et on itère de 2 pour éviter deux fusions
            i += 2
        else:                                   #sinon si la valeur ne peut pas fusionner on l'ajoute à nvl_lignes
            nvl_ligne.append(valeur)
            i += 1
    
    #on complète la liste avec des 0 à droite pour que la taille soit respecté
    #et que tout les chiffres soient décalés à gauche
    while len(nvl_ligne) < len(ligne):
        nvl_ligne.append(0)

    return nvl_ligne


#fonction qui inverse une liste ([1, 2, 3] -> [3, 2, 1])
def inverse_ligne(ligne):
    """retourne une liste inversé"""
    return ligne[::-1]

#fonction qui inverse une grille :
def inverse_grille(grille):
    """retourne une liste de listes dont les coordonnées x et y ont été inversées"""
    new_grille = [[0 for x in grille]for x in grille[0]]    #création d'une nouvelle grile
    for x in range(len(grille)):
        for i in range(len(grille[0])):
            new_grille[i][x] = grille[x][i]                 #on inverse la coordonnés x et y
    
    return new_grille


#fonctions qui gère tout les mouvements
def mouvement_grille(grille, direction):

    """retourne une grille(liste de liste) où un mouvement de 2048 a été appliqué et modifie aussi directement la grille fournie

    args:
        grille: liste de liste représentant notre jeu de 2048
        direction: chaine de caractère("haut", "bas", "droite", "gauche")
    """

    #on sauvegarde la grille de départ pour comparer plus loin    
    anc_grille = deepcopy(grille)

    #match case pour agir différemment selon la direction
    match direction.lower().strip():

        case "gauche":                                  
            i = 0                                       
            for ligne in grille: 
                #pour chaque ligne :                    
                grille[i] = mouvement_ligne(ligne)      #pour chaque ligne de la grille on applique le mouvement de ligne
                i += 1                                  #la variable i sert à compter les itérations pour modifier directement la grille
        
        case "droite":
            i = 0
            for ligne in grille: 
                #pour chaque ligne:                     
                ligne = inverse_ligne(ligne)            #içi il faut inverser chaque ligne pour faire le déplacement à gauche
                ligne = mouvement_ligne(ligne)          #on applique le mouvement de ligne à gauche
                grille[i] = inverse_ligne(ligne)        #on réinverse pour remettre la ligne dans le bon sens
                i += 1                                  #on retrouve la variable i
        
        case "bas":
            grille[:] = inverse_grille(grille)          
            i = 0
            for ligne in grille:
                #pour chaque ligne :                   #sur tout ce bloc il faut faire 2 inversions pour que ce soit bon(horizontale et verticale)
                ligne = inverse_ligne(ligne)           
                ligne = mouvement_ligne(ligne)         #on applique le mouvement de la ligne à gauche puis on remet dans le bon sens
                grille[i] = inverse_ligne(ligne)       #le [:] sert à sélectionner toutes les valeurs(on écrase l'ancienne valeur)
                i += 1                                  #on retrouve la varible i
            grille[:] = inverse_grille(grille)
        
        case "haut":
            grille[:] = inverse_grille(grille)      
            i = 0
            for ligne in grille:
                grille[i] = mouvement_ligne(ligne)     #même principe que pour le haut mais avec l'inversion horiztonale en moins
                i += 1
            grille[:] = inverse_grille(grille)
        
        case _:
            return 'erreur : direction incorrecte'      #cas par défaut en cas d'erreur de frappe
            

    if anc_grille != grille:
        apparition(grille)                              #si la grille a changé un nouveau bloc apparait
    
    return grille


#procédure qui initialise la fenetre du jeu
def lancer_fenetre(window):
    window.title("2048 - Python")
    window.iconbitmap(icon_path)
    window.geometry("720x480")
    window.minsize(360, 240)
    window.config(bg=bg)


def titre(texte, lieu, bg_color):
    return tk.Label(
        lieu,
        text=texte,
        bg=bg_color,
        fg="black",
        font=("courrier", 40)
    )

def sous_titre(texte, lieu, bg_color):
    return tk.Label(
        lieu,
        text = texte,
        bg = bg_color,
        fg = "grey",
        font=("Arial", 15)
    )


def ecran_accueil(window):

    for widget in window.winfo_children():
        widget.destroy()
    
    bg_frame1 = "#ECF5B3"
    bg_frame2 = "#DBA2D9"

    frame1 = tk.Frame(window, bg=bg_frame1)
    frame2 = tk.Frame(window, bg=bg_frame2)

    label_title = titre("Un Jeu de 2048 en PYTHON \n - \n Cours de NSI", frame1, bg_frame1)
    label_title.pack()

    label_credits = sous_titre("\nPar Nail, Merwan et Milo", frame1, bg_frame1)
    label_credits.pack()

    lancer_bouton = tk.Button(
        frame2,
        text="Lancer",
        bg="pink",
        fg='black',
        font=("Arial", 25),
        command=lambda: lancer_jeu(window)
    )

    param_bouton = tk.Button(
        frame2,
        text="Paramètres",
        bg="purple",
        fg='black',
        font=("Arial", 25),
        command=lambda: parametres(window)
    )

    bestScore_bouton = tk.Button(
        frame2,
        text= "Meilleurs Scores",
        bg= "light yellow",
        font=("Arial", 25),
        command= lambda: best_score(window)
    )

    lancer_bouton.grid(row=0, column=1, padx=20)
    param_bouton.grid(row=0, column=0, padx=20)
    bestScore_bouton.grid(row=0, column = 2, padx=20,)

    frame1.pack(expand=True)
    frame2.pack(expand=True)

def parametres(window):

    #nettoyage de l'ancienne fenetre:
    for element in window.winfo_children():
        element.destroy()
    #on change le titre de la fenetre:
    window.title("2048 - Paramètres")

    bg_frames = "#DCE09B"
    #on definit les frames:
    frame1 = tk.Frame(window, bg=bg_frames)
    frame2 = tk.Frame(window, bg=bg)


    #textes:
    title1 = titre("Personnalisation", frame1, bg_frames)

    title2 = titre("Actions", frame2, bg_frames)

    subtitle1 = sous_titre("Taille : ", frame1, bg_frames)

    subtitle2 = sous_titre("Probablités 2 - 4 :", frame1, bg_frames)

    subtitle3 = sous_titre("Touches :", frame1, bg_frames)

    subtitle4 = sous_titre("Pseudo", frame1, bg_frames)

    #champs de saisies
    tailleJeu = tk.Entry(frame1)
    pseudo = tk.Entry(frame1)

    #varibles pour les choix de probas et touches:
    touches_options = ["ZQSD", "Fleches", "WASD"]
    probas_options = ["10% - 90%", "20% - 80%", "30% - 70%", "40% - 60%", "50% - 50%"]

    valeur_probas = tk.StringVar(window)
    valeur_touches = tk.StringVar(window)

    #on définit les valeurs par défaut des menus
    valeur_probas.set(default_proba)
    valeur_touches.set(default_touches)

    #on cree les menus
    #le "*" sert à séparer les liste en option disintinces : 
    # [1, 2, 3] -> "1" "2" "3"
    menu_probas = tk.OptionMenu(frame1, valeur_probas, *probas_options)
    menu_touches = tk.OptionMenu(frame1, valeur_touches, *touches_options)


    #on cree les boutons

    accueil_bouton = tk.Button(
        frame2,
        text="Retour Au Menu",
        bg="pink",
        fg='black',
        font=("Arial", 25),
        command=lambda: ecran_accueil(window)
    )
    lancer_bouton = tk.Button(
        frame2,
        text="Lancer",
        bg="pink",
        fg='black',
        font=("Arial", 25),
        command=lambda: lancer_jeu(window)
    )

    enregistrer_bouton = tk.Button(
        frame2,
        text="Enregistrer",
        bg="pink",
        fg='black',
        font=("Arial", 25),
        command= None
    )
    #on place les éléments avec grid:
    title1.grid(row = 0, column=0)
    title2.grid(row=0, column=0)
    subtitle1.grid(row = 1, column = 0)
    subtitle2.grid(row = 2, column= 0)
    subtitle3.grid(row= 3, column= 0)
    subtitle4.grid(row= 4, column= 0)
    tailleJeu.grid(row = 1, column= 1)
    menu_probas.grid(row = 2, column=1)
    menu_touches.grid(row = 3, column=1)
    pseudo.grid(row = 4, column=1)

    enregistrer_bouton.grid(row=0, column=1, padx=20)
    accueil_bouton.grid(row=0, column=0, padx=20)
    lancer_bouton.grid(row=0, column = 2, padx=20,)

    #on pack les grilles
    frame1.pack(expand=tk.YES)
    frame2.pack(expand=tk.YES)


def lancer_jeu(window):
    for element in window.winfo_children():
        element.destroy()
    print("lancement du 2048")

def fin_de_jeu(window):
    for element in window.winfo_children():
        element.destroy()

def best_score(windows):
    print("les meilleurs scores")
    


root = tk.Tk()
lancer_fenetre(root)
ecran_accueil(root)
root.mainloop()






