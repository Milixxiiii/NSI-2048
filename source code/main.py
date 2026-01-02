#on importe les modules nécessaires

from tkinter import *
from random import choice, randint
from time import sleep
import os

#on définit des varibles de base

taille = 4
proba = [2 for i in range(9)] + [4 for i in range(1)]
grille_jeu = [[0 for y in range(taille)] for x in range(taille)]


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
    """simple fonction permettant de faire apparaitre un chiffre à un endroit aléatoire de la grille
    
    args:
        grille: grille actuelle du jeu
    returns:
        retourne la même grille mais avec l'apparition d'un nouveau bloc
    """
    vide = select_zero(grille)
    nouvelle_case = choice(vide)
    grille[nouvelle_case[0]][nouvelle_case[1]] = choice(proba)
    return grille



def initialisation(grille):

    """procédure permettant la préparation du jeu 2048
    
    args:
        grille: grille avec laquelle on veut jouer
    
    """

    for loop in range(2):
        vide = select_zero(grille)
        remplacement = choice(vide)
        grille[remplacement[0]][remplacement[1]] = choice(proba)

def gauche(grille):
    
    nbModif = 0
    for line in grille:
        nvl_ligne = []
        for x in line:
            if x != 0:
                nvl_ligne.append(x)
        for x in range(len(line)-len(nvl_ligne)):
            nvl_ligne.insert(0, 0)
        grille[grille.index(line)] = nvl_ligne

    
    if nbModif != 0:
        apparition(grille)



def droite(grille):
    
    nbModif = 0
    for line in grille:
        nvl_ligne = []
        for x in line:
            if x != 0:
                nvl_ligne.insert(0, x)
        for x in range(len(line)-len(nvl_ligne)):
            nvl_ligne.append(0)
        grille[grille.index(line)] = nvl_ligne

    
    if nbModif != 0:
        apparition(grille)


initialisation(grille_jeu)
afficheGrille(grille_jeu)
sleep(2)
gauche(grille_jeu)
afficheGrille(grille_jeu)
sleep(2)
droite(grille_jeu)
afficheGrille(grille_jeu)





