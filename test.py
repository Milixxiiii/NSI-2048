def mouvement_ligne(ligne):

    """Fonction qui déplace tout les cubes d'une liste et fusionne certains à la mannière d'un 2048
    
    args:
        ligne: la ligne à laquelle on veut faire effectuer le déplacement
    returns:
        nvl_ligne: la ligne avec les modifications effectués
    """

    #nouvelle variables : une temporaire sans les 0(cases vides) et la nouvelle
    ligne_temp = [x for x in ligne if x != 0]
    nvl_ligne = []

    #boucles qui gère l'addition des termes ou non
    i = 0    
    while i < len(ligne_temp):
        valeur = ligne_temp[i]
        if i == len(ligne_temp)-1:              #si c'est la dernière itération on ajoute tout simplement 
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
            
lst = [2, 2, 2, 0]
print(mouvement_ligne(lst))
