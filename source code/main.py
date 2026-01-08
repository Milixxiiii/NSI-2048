#on importe les modules nécessaires

from pathlib import Path
from random import choice, randint
from copy import deepcopy
import time
import os
import tkinter as tk
from tkinter import messagebox

#on définit des varibles globales

taille_grille = 4 #taille par défaut de la grille
bg = "#DBA2D9"  #couleur de fond de la fenetre
default_probas = "90% - 10%"
default_touches = "zqsd"
proba = []
nom = "player"
score = 0

#on définit les chemins des ressources
icon_path = Path(__file__).parent.parent / "ressources" / "icone.ico"
best_score_file = Path(__file__).parent.parent / "ressources" / "best_score.txt"

#dictionnaire des couleurs
color = {
    0: "#CDC1B4",
    2: "#EEE4DA",
    4: "#EDE0C8",
    8: "#F2B179",
    16: "#F59563",
    32: "#F67C5F",
    64: "#F65E3B",
    128: "#EDCF72",
    256: "#EDCC61",
    512: "#EDC850",
    1024: "#EDC53F",
    2048: "#EDC22E",

    4096: "#3C3A32",
    8192: "#2E2C25",
    16384: "#1F1E1A",
    32768: "#1A1612",
    65536: "#140F0A",

    131072: "#0F0B07",
    262144: "#0B0805",
    524288: "#070503",
    1048576: "#030201",
}


#fonction affichage de la grille dans la console(pour le debug)
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

    for x in range(len(liste)): #parcours des lignes
        for element in range(len(liste[x])): #parcours des éléments de chaque ligne
            if liste[x][element] == 0:
                case_zero.append((x, element))  #si 0 on l'ajoute à la liste des cases vides

    return case_zero

#fonction qui initialise le jeu en créant la varible de départ
def initialisation(taille):

    """retourne une liste représentant un jeu de 2048
    
    args:
        taille: taille de la grille avec laquelle on veut jouer

    
    """

    #varibles glovales
    global proba

    #on récupère les probas choisies par l'utilisateur
    p2, p4 = default_probas.replace("%", "").split(" - ")

    #on crée la grille de jeu
    grille_jeu = [[0 for y in range(taille)] for x in range(taille)]


    #on genere les probas
    proba = [2]*int(p2) + [4]*int(p4)


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
def mouvement_ligne(ligne, compter_score):

    """retourne une liste et fusionne certains cubes à la mannière d'un 2048

    args:
        ligne: la ligne à laquelle on veut faire effectuer le déplacement
    """

    #on utliser la variable globale score
    global score

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
            if compter_score:                   
                score += valeur*2               #on met à jour le score si on doit le compter
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
def mouvement_grille(grille, direction, compter_score = True, apparition_bloc = True):

    """fonction modifiant une grille fournie selon les déplacements d'un 2048

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
                grille[i] = mouvement_ligne(ligne, compter_score)      #pour chaque ligne de la grille on applique le mouvement de ligne
                i += 1                                  #la variable i sert à compter les itérations pour modifier directement la grille
        
        case "droite":
            i = 0
            for ligne in grille: 
                #pour chaque ligne:                     
                ligne = inverse_ligne(ligne)            #içi il faut inverser chaque ligne pour faire le déplacement à gauche
                ligne = mouvement_ligne(ligne, compter_score)          #on applique le mouvement de ligne à gauche
                grille[i] = inverse_ligne(ligne)        #on réinverse pour remettre la ligne dans le bon sens
                i += 1                                  #on retrouve la variable i
        
        case "bas":
            grille[:] = inverse_grille(grille)          
            i = 0
            for ligne in grille:
                #pour chaque ligne :                   #sur tout ce bloc il faut faire 2 inversions pour que ce soit bon(horizontale et verticale)
                ligne = inverse_ligne(ligne)           
                ligne = mouvement_ligne(ligne, compter_score)         #on applique le mouvement de la ligne à gauche puis on remet dans le bon sens
                grille[i] = inverse_ligne(ligne)       #le [:] sert à sélectionner toutes les valeurs(on écrase l'ancienne valeur)
                i += 1                                  #on retrouve la varible i
            grille[:] = inverse_grille(grille)
        
        case "haut":
            grille[:] = inverse_grille(grille)      
            i = 0
            for ligne in grille:
                grille[i] = mouvement_ligne(ligne, compter_score)     #même principe que pour le haut mais avec l'inversion horiztonale en moins
                i += 1
            grille[:] = inverse_grille(grille)
        
        case _:
            return 'erreur : direction incorrecte'      #cas par défaut en cas d'erreur de frappe
            

    if anc_grille != grille and apparition_bloc:
        apparition(grille)                              #si la grille a changé + appartion : True un nouveau bloc apparait
    return grille

def verif_defaite(grille):

    """fonctionretournant True si le joueur ne peut plus jouer

    args:
        grille: liste de liste représentant notre jeu de 2048
    returns:
        bool: True si le joueur ne peut plus jouer, False sinon
    """

    nvl_grille = deepcopy(grille)   #on crée une copie de la grille

    #on effectue tout les mouvements sans compter le score ni faire apparaitre de nouveaux blocs
    mouvement_grille(nvl_grille, direction="haut", compter_score=False)
    mouvement_grille(nvl_grille, direction="bas", compter_score=False)
    mouvement_grille(nvl_grille, direction="gauche", compter_score=False)
    mouvement_grille(nvl_grille, direction="droite", compter_score=False)

    #on compare la nouvelle grille avec l'ancienne
    if grille == nvl_grille:
        return True     #si elles sont identiques le joueur ne peut plus jouer
    else:
        return False    # sinon il peut encore jouer

def verif_2048(grille):

    """
    fonction retournant True si un cube 2048 ou plus est présent dans la grille
    
    args:
        grille: liste de liste représentant notre jeu de 2048
    returns:
        bool: True si un cube 2048 ou plus est présent, False sinon
    """
    for line in grille:     #parcours des lignes
        for element in line:    #parcours des éléments de chaque ligne
            if element >= 2048:
                return True     #si on trouve un cube 2048 ou plus on retourne True
    return False            #sinon on retourne False

#procédure qui initialise la fenetre du jeu
def lancer_fenetre(window):
    """
    procédure qui initialise la fenetre principale du jeu
    
    args:
        window: objet tkinter représentant la fenetre principale
    """
    window.title("2048")   #titre de la fenetre
    window.iconbitmap(icon_path)    #icone de la fenetre
    window.geometry("1920x1080")    #taille de la fenetre
    window.minsize(960, 600)    #taille minimale de la fenetre
    window.config(bg=bg)        #couleur de fond de la fenetre


def titre(texte, lieu, bg_color):
    """
    retourne un label de titre

    args:
        texte: texte du titre
        lieu: frame ou placer le titre
        bg_color: couleur de fond du titre
    returns:
        label: label tkinter représentant le titre
    """
    return tk.Label(
        lieu,
        text=texte,
        bg=bg_color,
        fg="black",
        font=("courrier", 70)
    )

def sous_titre(texte, lieu, bg_color):
    """
    retourne un label de sous-titre

    args:
        texte: texte du sous-titre
        lieu: frame ou placer le sous-titre
        bg_color: couleur de fond du sous-titre
    returns:
        label: label tkinter représentant le sous-titre
    """
    return tk.Label(
        lieu,
        text = texte,
        bg = bg_color,
        fg = "grey",
        font=("Arial", 25)
    )

def maj_param(pseudo, taille, touches, probas):
    """
    procédure qui met à jour les paramètres du jeu

    args:
        pseudo: entrée tkinter du pseudo
        taille: entrée tkinter de la taille de la grille
        touches: variable tkinter des touches choisies
        probas: variable tkinter des probas choisies
    """
    #variables globales
    global nom, taille_grille, default_probas, default_touches

    #on met à jour les variables globales
    nom = pseudo.get()
    taille_grille = int(taille.get())
    default_touches = touches.get()
    default_probas = probas.get()
    
    

def ecran_accueil(window):

    """
    procédure qui affiche l'écran d'accueil du jeu

    args:
        window: objet tkinter représentant la fenetre principale
    """

    #on nettoie la fenetre
    for widget in window.winfo_children():
        widget.destroy()
    
    #on change le titre de la fenetre
    window.title("2048 - Accueil")
    
    #on choisit un fond pour les frames
    bg_frame1 = "#ECF5B3"

    #on crée les frames
    frame1 = tk.Frame(window, bg=bg_frame1)
    frame2 = tk.Frame(window, bg=bg)

    #on crée les textes
    label_title = titre("Un Jeu de 2048 en PYTHON \n - \n Cours de NSI", frame1, bg_frame1)
    label_credits = sous_titre("\nPar Nail, Merwan et Milo", frame1, bg_frame1)

    #on place les textes
    label_title.pack()
    label_credits.pack()

    #on crée les boutons
    lancer_bouton = tk.Button(
        frame2,
        text="Lancer",
        bg="pink",
        fg='black',
        font=("Arial", 25),
        command=lambda: initialisation_interface(window)
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

    #on place les boutons avec grid
    lancer_bouton.grid(row=0, column=1, padx=20)
    param_bouton.grid(row=0, column=0, padx=20)
    bestScore_bouton.grid(row=0, column = 2, padx=20,)

    #on pack les frames
    frame1.pack(expand=True)
    frame2.pack(expand=True)


def parametres(window):

    """
    procédure qui affiche l'écran des paramètres

    args:
        window: objet tkinter représentant la fenetre principale
    """

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

    subtitle1 = sous_titre("Taille : ", frame1, bg_frames)

    subtitle2 = sous_titre("Probablités 2 - 4 :", frame1, bg_frames)

    subtitle3 = sous_titre("Touches :", frame1, bg_frames)

    subtitle4 = sous_titre("Pseudo", frame1, bg_frames)

    #champs de saisies
    tailleJeu = tk.Entry(frame1)
    pseudo = tk.Entry(frame1)

    #on remplit les champs de saisies avec les valeurs actuelles:

    tailleJeu.insert(0, str(taille_grille))
    pseudo.insert(0, nom)

    #varibles pour les choix de probas et touches:
    touches_options = ["zqsd", "Fleches", "wasd"]
    probas_options = ["10% - 90%", "20% - 80%", "30% - 70%", "40% - 60%", "50% - 50%"]

    valeur_probas = tk.StringVar(window)
    valeur_touches = tk.StringVar(window)

    #on définit les valeurs par défaut des menus
    valeur_probas.set(default_probas)
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
        command=lambda: initialisation_interface(window)
    )

    enregistrer_bouton = tk.Button(
        frame2,
        text="Enregistrer",
        bg="pink",
        fg='black',
        font=("Arial", 25),
        command= lambda: maj_param(pseudo, tailleJeu, valeur_touches, valeur_probas)
    )
    #on place les éléments avec grid:
    title1.grid(row=0, column=0)
    subtitle1.grid(row = 1, column = 0)
    subtitle2.grid(row = 2, column= 0)
    subtitle3.grid(row= 3, column= 0)
    subtitle4.grid(row= 4, column= 0)
    tailleJeu.grid(row = 1, column= 1)
    menu_probas.grid(row = 2, column=1)
    menu_touches.grid(row = 3, column=1)
    pseudo.grid(row = 4, column=1)

    enregistrer_bouton.grid(row=1, column=1, padx=20, pady=40)
    accueil_bouton.grid(row=1, column=0, padx=20, pady=40)
    lancer_bouton.grid(row=1, column = 2, padx=20, pady=40)

    #on pack les grilles
    frame1.pack(expand=tk.YES)
    frame2.pack(expand=tk.YES)

def maj_grille(window, canva, grille, taille_case, label_score):

    """
    procédure qui met à jour l'affichage de la grille

    args:
        window: objet tkinter représentant la fenetre principale
        canva: canvas tkinter représentant la zone de jeu
        grille: liste de liste représentant notre jeu de 2048
        taille_case: taille d'une case en pixel
        label_score: label tkinter représentant le score
    """
    for x in range(taille_grille):      #parcours des lignes
        for i in range(taille_grille):  #parcours des éléments de chaque ligne
            #on récupère la case
            case = grille[x][i]

            #on calcule les coordonnées de la case
            x1 = i*taille_case
            y1 = x*taille_case
            x2 = i*taille_case + taille_case
            y2 = x*taille_case + taille_case

            #on dessine la case
            canva.create_rectangle(
                x1, y1, x2, y2,
                fill = color[case]
            )

            #si c'est un bloc > 0 on affiche sa valeur
            if case > 0:
                canva.create_text(
                    x1 + taille_case/2, y1 + taille_case/2,
                    text= str(case),
                    fill= "black",
                    font=("Arial", 30)
                )
    #on met à jour le score
    label_score.configure(text="\nScore : " + str(score))

    #on vérifie si le jeu est fini
    if verif_defaite(grille):
        #si oui on affiche un message de défaite
        messagebox.showinfo(title = "Perdu", message="Plus d'espace Disponible", parent=window)
        fin_de_jeu(window, "defaite", grille)

    #on vérifie si le joueur a gagné
    if verif_2048(grille):
        #si oui on lui demande s'il veut continuer ou non
        if messagebox.askyesno(title= "Gagné", message="Veux-tu finir la partie ?"):
            fin_de_jeu(window, "Victoire", grille)


def initialisation_interface(window):
    """
    procédure qui initialise l'interface de jeu

    args:
        window: objet tkinter représentant la fenetre principale
    """

    #varible globale
    global score 
    
    #on réinitialise le score
    score = 0

    #on nettoie la fenetre
    for element in window.winfo_children():
        element.destroy()
    
    #on change le titre de la fenêtre
    window.title("2048 - Jeu")

    #on crée la grille de jeu
    grille_jeu = initialisation(taille_grille)

    #on crée le canvas(zone de jeu)
    zone_jeu = tk.Canvas(window, width = 800, height = 800, bg="ivory", highlightthickness = 0, borderwidth=0)
    zone_jeu.grid(row = 0, column= 0, pady= 40, padx=50)

    #on crée la frame de l'UI:
    frameUI = tk.Frame(window, bg=bg)

    #on crée les boutons :
    bouton_stop = tk.Button(
        frameUI,
        text="Fin Du Jeu",
        bg="pink",
        fg='black',
        font=("Arial", 25),
        command= lambda: fin_de_jeu(window, "Abandon", grille_jeu)
    )

    bouton_commencer = tk.Button(
        frameUI,
        text="Commencer",
        bg="pink",
        fg='black',
        font=("Arial", 25),
        command= lambda: jeu(window, zone_jeu, label_score, grille_jeu)
    )

    #on crée les textes:

    label_joueur = sous_titre("Joueur : " + nom, frameUI, bg)
    label_score = sous_titre("\nScore :" + str(score), frameUI, bg)

    #calcul de la largeur d'une case    
    #contour
    zone_jeu.create_rectangle(
        0, 0, 800, 800,
        outline="black",
        width=5
    )


    #on place les éléments de l'UI avec grid
    label_joueur.grid(row= 0, column=0)
    label_score.grid(row = 1, column = 0)
    bouton_commencer.grid(row=2, column = 0, pady = 100)
    bouton_stop.grid(row = 3, column = 0, pady=40)
    frameUI.grid(row=0, column=1)






def jeu(window, canva, label_score, grille):

    """
    procédure qui gère le déroulement du jeu

    args:
        window: objet tkinter représentant la fenetre principale
    """

    #on change le titre de la fenetre
    window.title("2048 - Jeu En Cours")

    #on isole les touches:
    if default_touches == "Fleches":
        #si c'est des fleches on les assigne directement
        haut = "<Up>"
        gauche = "<Left>" 
        droite = "<Right>"
        bas = "<Down>"
    else:
        #sinon on recupe les touches choisies
        haut = "<" + default_touches[0] + ">"
        gauche = "<" + default_touches[1] + ">"
        bas = "<" + default_touches[2] + ">"
        droite = "<" + default_touches[3] + ">"

    #on calcule la taille d'une case
    taille_case = 800/taille_grille

    #on fait l'affichage initial de la grille
    maj_grille(window, canva, grille, taille_case, label_score)

    #on bind les touches aux fonctions de déplacement et on met à jour la grille après chaque déplacement
    window.bind(haut, lambda event:[mouvement_grille(grille, "haut"), maj_grille(window, canva, grille, taille_case, label_score)])
    window.bind(bas, lambda event:[mouvement_grille(grille, "bas"), maj_grille(window, canva, grille, taille_case, label_score)])
    window.bind(gauche, lambda event:[mouvement_grille(grille, "gauche"), maj_grille(window, canva, grille, taille_case, label_score)])
    window.bind(droite, lambda event:[mouvement_grille(grille, "droite"), maj_grille(window, canva, grille, taille_case, label_score)])



def fin_de_jeu(window, type_fin, grille):
    """
    procédure qui affiche l'écran de fin de jeu

    args:
        window: objet tkinter représentant la fenetre principale
        type_fin: chaine de caractère représentant le type de fin("Victoire", "Défaite", "Abandon")
        grille: liste de liste représentant notre jeu de 2048
    """

    #on nettoie la fenetre
    for element in window.winfo_children():
        element.destroy()

    #on change le titre de la fenetre
    window.title("2048 - Fin Du Jeu")

    #on calcule la plus grande case :
    case_haute = 0
    for line in grille: #parcours des lignes
        for number in line: #parcours des éléments de chaque ligne
            if number > case_haute:
                #on met a jour la plus grande case
                case_haute = number


    #on crée les frames
    frame_principale = tk.Frame(window, bg="Ivory")
    frame_bouton = tk.Frame(window, bg="Ivory")

    #on crée les textes
    label_typeFin = tk.Label(frame_principale, bg="Ivory", fg="black", text=str(type_fin) + " de " + nom, font=("Helvetica", 80), padx=80, pady= 80)
    label_meilleureCase = tk.Label(frame_principale, bg="Ivory", fg="black", text="\nBloc le plus grand : " + str(case_haute), font=("Arial", 40), pady= 8)
    label_scoreFinal = tk.Label(frame_principale, bg="Ivory", fg="black", text="\nScore Final : " + str(score), font=("Arial", 40), padx=80, pady= 80)

    #on crée les boutons
    bouton_quitter = tk.Button(
        frame_bouton,
        text="Quitter",
        bg="white",
        fg='black',
        font=("Arial", 25),
        command= lambda: fermer(window)
    )

    bouton_rejouer = tk.Button(
        frame_bouton,
        text="Rejouer",
        bg="pink",
        fg='black',
        font=("Arial", 25),
        command=lambda: initialisation_interface(window)
    )

    bouton_meilleurScore = tk.Button(
        frame_bouton,
        text= "Meilleurs Scores",
        bg= "light yellow",
        font=("Arial", 25),
        command= lambda: best_score(window)
    )


    #on affiche les textes
    label_typeFin.pack()
    label_meilleureCase.pack()
    label_scoreFinal.pack()

    #on place les boutons avec grid
    bouton_quitter.grid(row = 0, column= 0, pady = 30, padx = 50)
    bouton_meilleurScore.grid(row = 0, column= 2, pady = 30, padx = 50)
    bouton_rejouer.grid(row = 0, column= 1, pady = 30, padx = 50)
    
    #on enregistre le score dans le fichier des meilleurs scores
    with open(best_score_file, "a") as f:
        f.write(nom + " : " + str(score) + "\n")
    #on affiche les boutons

    #on pack les frames
    frame_principale.pack(expand= tk.YES)
    frame_bouton.pack(expand= tk.YES)

def fermer(window):
    """
    procédure qui gère la fermeture de la fenetre
    c'est un easter egg un peu dangereux... a prendre avec humour ;)
    aucune mauvaise intention derrière cela ni de responsabilité en cas de problème

    args:
        window: objet tkinter représentant la fenetre principale
    """

    #on nettoie la fenetre
    for widget in window.winfo_children():
        widget.destroy()

    #on demande l'avis de l'utilisateur
    if messagebox.askyesno(title= "avis", message= "Avez - vous apprécie notre jeu ?"):
        #on affiche un message de remerciement
        messagebox.showinfo(title= "Merci !", message= "Merci pour votre soutien ! Au revoir !")
        #on ferme la fenetre
        window.destroy()
    else:
        #on le menace d'eteindre son pc
        if messagebox.askyesno(title= "avis", message= "Etes - vous sur ? Vous devriez sauvegarder tout les documents ouvert..."):
            #si il accepte on lance le compte à rebourd
            os.system("shutdown -s -t 10")
            if messagebox.askyesno(title= "avis", message= "Etes - vous sur ? votre pc s'éteindra dans 10 sec... cliquer sur non pour changer d'avis..."):
                #si il confirme on le fait
                None
            else:
                #sinon si il revient sur son avis on annule l'extinction
                os.system("shutdown -a")
                window.destroy()
        else:
            window.destroy()
            



def best_score(window):
    """
    procédure qui affiche l'écran des meilleurs scores

    args:
        window: objet tkinter représentant la fenetre principale
    """ 
    #on nettoie la fenetre
    for widget in window.winfo_children():
        widget.destroy()

    #on change le titre de la fenetre
    window.title("2048 - Meilleurs Scores")

    #on récupère les meilleurs scores dans une liste :
    scores = []

    #on lit le fichier des meilleurs scores
    with open(best_score_file, 'r') as f:
        scores = f.readlines()

    #on les classe
    scores.sort(reverse=True, key= lambda joueur : int(joueur.split(" : ")[1]))


    #creation des frames
    frame_titre = tk.Frame(window, bg=bg)
    frame_scores = tk.Frame(window, bg=bg)
    frame_boutons = tk.Frame(window, bg=bg)

    #création de texte : 
    label_titre = titre("Meilleurs Scores : ", frame_titre, bg)

    #creation du texte des 3 premiers scores : 
    label_bestScore = tk.Label(
        frame_scores,
        text = scores[0] + "\n" + scores[1] + "\n" + scores[2],
        bg = "Ivory",
        fg = "black",
        font = ("helvetica", 30)
    )

    #on crée les boutons : 
    bouton_quitter = tk.Button(
        frame_boutons,
        text="Quitter",
        bg="white",
        fg='black',
        font=("Arial", 25),
        command= lambda: fermer(window)
    )
    bouton_jouer = tk.Button(
        frame_boutons,
        text="Jouer",
        bg="pink",
        fg='black',
        font=("Arial", 25),
        command=lambda: initialisation_interface(window)
    )

    bouton_accueil = tk.Button(
        frame_boutons,
        text="Retour Au Menu",
        bg="purple",
        fg='black',
        font=("Arial", 25),
        command=lambda: ecran_accueil(window)
    )




    #on place les éléments
    label_titre.pack()

    label_bestScore.pack()

    bouton_quitter.grid(row = 0, column= 0, pady= 30, padx= 40)
    bouton_jouer.grid(row = 0, column= 1, pady= 30, padx= 40)
    bouton_accueil.grid(row = 0, column= 2, pady= 30, padx= 40)

    frame_titre.pack(expand = tk.YES)
    frame_scores.pack(expand = tk.YES)
    frame_boutons.pack(expand = tk.YES)
    

#on lance le programme
root = tk.Tk()      #on crée l'objet tkinter
lancer_fenetre(root)    #on initialise la fenetre
ecran_accueil(root)     #on affiche l'écran d'accueil
root.mainloop()         #on lance la boucle principale de tkinter