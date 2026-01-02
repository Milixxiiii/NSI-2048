from tkinter import *

def fonctionA(event):
    print("a")
def fonctionB(event):
    print("b")

root = Tk()

root.bind("<Up>", fonctionA)
root.bind("<Down>", fonctionB)

bouton=Button(root, text="Fermer", command=root.quit)
bouton.pack()

root.mainloop()

