import tkinter as tk
import tkinter.simpledialog as sdg
import tkinter.messagebox as mbx
import tkinter.font as tkf
import tkinter.filedialog as fdg
import random as rnd
import platform as pt
import time

if pt.system() == "Linux":
	id = "~"
elif pt.system() == "Windows":
	id = "C:\\"

base = tk.Tk()
base.title("Cellular Automata Tiling Weaver")
base.resizable(False, False)

viewer = tk.LabelFrame(base, text="Image Render", bd = 4, font=tkf.Font(family="Consolas", size = 10))
viewer.grid(row = 0, column = 0, padx = 2, pady = 2)
settings = tk.Frame(base, bd=4)
settings.grid(row = 0, column = 1, padx = 2, pady = 2)

ctx = tk.Canvas(viewer, width=600, height=600)
ctx.pack()

#A dropdown menu to pick the automaton the user wants.
aut_options = [ 'Rule 30', 'Rule 110', 'Toothpick Sequence', 'Langton\'s Ant', 'Seeds' ]
option_var = tk.StringVar(base)
option_var.set('Rule 30') #default rule
aut_menu = tk.OptionMenu(settings, option_var, *aut_options)

tk.Label(settings, text="Select an automaton: ").grid(row = 0, column = 0, sticky=tk.W + tk.E)
aut_menu.grid(row = 0, column = 1, padx = 2, pady = 10, sticky=tk.W + tk.E)

startingCellsButton = tk.Button(settings, text="Set starting conditions")
startingCellsButton.grid(row = 1, column = 0, columnspan = 2, pady = 5, sticky=tk.W + tk.E)

previewImageButton = tk.Button(settings, text="Preview image")
previewImageButton.grid(row = 2, column = 0, columnspan = 2, pady = 5, sticky=tk.W + tk.E)

saveBMPButton = tk.Button(settings, text="Save .BMP")
saveBMPButton.grid(row = 3, column = 0, pady = 5, sticky=tk.W + tk.E)
savePNGButton = tk.Button(settings, text="Save .PNG")
savePNGButton.grid(row = 3, column = 1, pady = 5, sticky=tk.W + tk.E)

base.mainloop()
