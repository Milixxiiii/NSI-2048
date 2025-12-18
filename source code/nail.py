def fleche_gauche():
    for i in range(taille):
        ligne = grille[i]

        nvl_ligne = []
        for x in ligne:
            if x != 0:
                nvl_ligne.append(x)
