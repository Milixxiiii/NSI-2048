#on importe les modules nécessaires

from pathlib import Path
from random import choice, randint
from copy import deepcopy
import time
import os
import tkinter as tk

#on définit des varibles de base

taille_grille = 4
proba = [2 for i in range(9)] + [4 for i in range(1)]
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
    window.config(bg="#DBA2D9")

def ecran_accueil(window):

    for widget in window.winfo_children():
        widget.destroy()

    frame1 = tk.Frame(window, bg="#ECF5B3")
    frame2 = tk.Frame(window, bg="#DBA2D9")

    label_title = tk.Label(
        frame1,
        text="Un Jeu de 2048 en PYTHON \n - \n Cours de NSI",
        bg="#ECF5B3",
        fg="black",
        font=("courrier", 40)
    )
    label_title.pack()

    label_credits = tk.Label(
        frame1,
        text="\nPar Nail, Merwan et Milo",
        font=("Helvetica", 18),
        bg="#ECF5B3",
        fg='black'
    )
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

    lancer_bouton.grid(row=0, column=0, padx=20)
    param_bouton.grid(row=0, column=1, padx=20)

    frame1.pack(expand=True)
    frame2.pack(expand=True)

def parametres(window):
    for element in window.winfo_children():
        element.destroy()
    print("Ouverture des paramètres")

def lancer_jeu(window):
    print("lancement du 2048")


root = tk.Tk()
lancer_fenetre(root)
ecran_accueil(root)
root.mainloop()






