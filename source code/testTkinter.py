from tkinter import *
from pathlib import Path



icon_path = Path(__file__).parent.parent / "ressources" / "icone.ico"

#on crée l'objet tkinter
root = Tk()

#on fixe des paramètres pour notre objet root
root.title("2048")
root.iconbitmap(icon_path)
root.geometry("720x480")

#on crée les frames

frame = Frame(root)

#creation du texte 1



root.mainloop()

