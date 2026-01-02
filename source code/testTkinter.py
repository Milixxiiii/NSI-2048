from tkinter import *
from pathlib import Path

icon_path = Path(__file__).parent.parent / "ressources" / "icone.ico"

root = Tk()

root.title("2048")
root.iconbitmap(icon_path)


root.mainloop()

