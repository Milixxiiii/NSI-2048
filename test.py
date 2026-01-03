import time
import os

lst =[
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [2, 0, 0, 0],
    [2, 0, 0, 0],
]

def inverse_grille(grille):
    new_grille = [[0 for x in grille]for x in grille[0]]
    for x in range(len(grille)):
        for i in range(len(grille[0])):
            new_grille[i][x] = grille[x][i]
    
    return new_grille

def afficheGrille(grille):
    os.system("cls")
    for x in grille:
        print(x)

afficheGrille(lst)
time.sleep(2)
lst = inverse_grille(lst)
afficheGrille(lst)



