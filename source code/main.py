from random import choice, randint

taille = 4
proba = [2 for i in range(9)] + [4 for i in range(1)]
grille_jeu = [[0 for y in range(taille)] for x in range(taille)]

def afficheGrille(grille):
    for x in grille:
        print(x)

def select_zero(liste):

    case_zero = []

    for x in range(len(liste)):
        for element in range(len(liste[x])):
            if liste[x][element] == 0:
                case_zero.append((x, element))

    return case_zero


def __init__(grille):

    for loop in range(2):
        vide = select_zero(grille)
        remplacement = choice(vide)
        grille[remplacement[0]][remplacement[1]] = choice(proba)

__init__(grille_jeu)
afficheGrille(grille_jeu)

def haut(grille):
    