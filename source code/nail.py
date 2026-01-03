def fleche_gauche():
    for i in range(taille):
        ligne = grille[i]

        nvl_ligne = []
        for x in ligne:
            if x != 0:
                nvl_ligne.append(x)

# TEST TKINTER 1:
import tkinter as tk
from tkinter import messagebox

fenetre = tk.Tk()
fenetre.title("Test Tkinter")
fenetre.geometry("300x150")  

def bouton_clique():
    messagebox.showinfo("clique")

bouton = tk.Button(fenetre, text="Clique moi", command=bouton_clique)
bouton.pack(pady=50)  # pady = marge verticale

fenetre.mainloop()
