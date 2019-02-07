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
tk.Label(base, text = "Under construction, please stand by...", font = tkf.Font(family = "Consolas", size = 24)).pack()

base.mainloop()
