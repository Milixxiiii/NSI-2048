#on importe les modules nécessaires

from tkinter import *
from random import choice, randint
from copy import deepcopy
import time
import os

#on définit des varibles de base

taille_grille = 4
proba = [2 for i in range(9)] + [4 for i in range(1)]


#fonction affichage de la grille dans la console
def afficheGrille(grille):
    os.system("cls")
    for x in grille:
        print(x)




def select_zero(liste):

    """ Permet dde connaitre les cases "0" d'une grille de 2048

    Args:
        liste : grille des 2048 sous la forme d'une liste de liste

    Returns:
        Une liste contenant les coordonnées des cases "0" sous forme de tuple (x, y)    
    """

    case_zero = []

    for x in range(len(liste)):
        for element in range(len(liste[x])):
            if liste[x][element] == 0:
                case_zero.append((x, element))

    return case_zero


def apparition(grille):
    """procédure qui fait apparaitre un chiffre à un endroit aléatoire de la grille
    
    args:
        grille: grille actuelle du jeu
    """

    #creation de la nouvelle grille:

    #on choisit une case vide au hasard:
    vide = select_zero(grille)
    nouvelle_case = choice(vide)

    #on fait apparaitre un nouveau chiffre sur cette case et on retourn la nouvelle grille :
    grille[nouvelle_case[0]][nouvelle_case[1]] = choice(proba)



def initialisation(taille):

    """fonction permettant la préparation du jeu 2048
    
    args:
        taille: taille de la grille avec laquelle on veut jouer
    
    returns:
        grille_jeu: nouvelle grille de jeu généré
    
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

def mouvement_ligne(ligne):

    ligne_temp = [x for x in ligne if x != 0]
    nvl_ligne = []

    i = 0    
    while i < len(ligne_temp):
        valeur = ligne_temp[i]
        if i == len(ligne_temp)-1:
            nvl_ligne.append(ligne_temp[i])
            i += 1
        elif valeur == ligne_temp[i+1]:
            nvl_ligne.append(valeur*2)
            i += 2
        else:
            nvl_ligne.append(valeur)
            i += 1
    
     
    while len(nvl_ligne) < len(ligne):
        nvl_ligne.append(0)

    return nvl_ligne

def inverse_ligne(ligne):
    return ligne[::-1]

def inverse_grille(grille):
    new_grille = [[0 for x in grille]for x in grille[0]]
    for x in range(len(grille)):
        for i in range(len(grille[0])):
            new_grille[i][x] = grille[x][i]
    
    return new_grille

def mouvement_grille(grille, direction):
        
    anc_grille = deepcopy(grille)

    match direction.lower().strip():

        case "gauche":
            i = 0
            for ligne in grille:
                grille[i] = mouvement_ligne(ligne)
                i += 1
        
        case "droite":
            i = 0
            for ligne in grille:
                ligne = inverse_ligne(ligne)
                ligne = mouvement_ligne(ligne)
                grille[i] = inverse_ligne(ligne)
                i += 1
        
        case "bas":
            grille[:] = inverse_grille(grille)
            i = 0
            for ligne in grille:
                ligne = inverse_ligne(ligne)
                ligne = mouvement_ligne(ligne)
                grille[i] = inverse_ligne(ligne)
                i += 1
            grille[:] = inverse_grille(grille)
        
        case "haut":
            grille[:] = inverse_grille(grille)
            i = 0
            for ligne in grille:
                grille[i] = mouvement_ligne(ligne)
                i += 1
            grille[:] = inverse_grille(grille)
        
        case _:
            return 'erreur : direction incorrecte'
            

    if anc_grille != grille:
        apparition(grille)
    
    return grille


grille_jeu = initialisation(taille_grille)
afficheGrille(grille_jeu)
time.sleep(2)
mouvement_grille(grille_jeu, "haut")
afficheGrille(grille_jeu)




