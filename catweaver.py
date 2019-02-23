import tkinter as tk
import tkinter.simpledialog as sdg
import tkinter.messagebox as mbx
import tkinter.font as tkf
import tkinter.filedialog as fdg
import random as rnd
import platform as pt
import time

import utilities
import automata

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

# A list of the automata that are loaded.
# Note that the automaton doesn't continue past the left and right edges of the
# image - cells that do so die.
autList = [automata.ElementaryAutomaton(802, 30, 800),
		   automata.ElementaryAutomaton(802, 110, 800)]
autCurrent = autList[0]

def change_automaton(*args):
	try:
		autCurrent = autList[autList.index(optionVar.get())]
	except ValueError:
		autCurrent = autList[0]

	autCurrent.reset_board()


def output_img():
	grid = []
	try:
		if not (autCurrent.is_empty()):
			filename = fdg.asksaveasfilename( \
				parent = base, \
				title = "Save image to:", \
				initialdir = id, \
				filetypes = (("Portable Network Graphic", "*.png"), ("Bitmap", "*.bmp"), ("All files", "*.*")) \
				)

			if type(filename) is str and len(filename) > 0:
				grid = utilities.carve_array(autCurrent.generate_grid(), 1, 0, 800, 800)
				utilities.render_img([(0, 0, 0), (255, 255, 255)], grid, filename)
				mbx.showinfo("Success", "Image was rendered successfully at {0}".format(filename))

		else:
			mbx.showinfo("Error", "All cells in the starting configuration are empty.")
	except ValueError:
		mbx.showinfo("Error", "Invalid filename - please make sure you entered it correctly.")

	autCurrent.reset_board()

# A dropdown menu to pick the automaton the user wants.
autOptions = [ 'Rule 30', 'Rule 110', 'Toothpick Sequence', 'Langton\'s Ant', 'Seeds' ]
optionVar = tk.StringVar(base)
optionVar.set('Rule 30') #default rule
optionVar.trace('w', change_automaton)
autMenu = tk.OptionMenu(settings, optionVar, *autOptions)

tk.Label(settings, text="Select an automaton: ").grid(row = 0, column = 0, sticky=tk.W + tk.E)
autMenu.grid(row = 0, column = 1, padx = 2, pady = 10, sticky=tk.W + tk.E)

startingCellsButton = tk.Button(settings, text="Set starting conditions")
startingCellsButton.grid(row = 1, column = 0, columnspan = 2, pady = 5, sticky=tk.W + tk.E)

previewImageButton = tk.Button(settings, text="Preview image")
previewImageButton.grid(row = 2, column = 0, columnspan = 2, pady = 5, sticky=tk.W + tk.E)

saveBMPButton = tk.Button(settings, text="Save image", command=output_img)
saveBMPButton.grid(row = 3, column = 0, columnspan = 2, pady = 5, sticky=tk.W + tk.E)

base.mainloop()
