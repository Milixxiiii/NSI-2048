from random import randint

taille = 4
grille = [[0 for y in range(taille)] for x in range(taille)]

def afficheGrille():
    for x in grille:
        print(x)

def __init__():
    case_zero = []

    for x in range(len(grille)):
        for element in range(len(grille[x])):
            if grille[x][element] == 0:
                case_zero.append((x, element))
    print(case_zero)

__init__()