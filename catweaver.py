import tkinter as tk
import tkinter.simpledialog as sdg
import tkinter.messagebox as mbx
import tkinter.font as tkf
import tkinter.filedialog as fdg
import random as rnd
import platform as pt
import time
import copy

import utilities
import automata

DEAD_EDGE = 0
WRAP_GRID = 1

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
autList = [automata.ElementaryAutomaton(400, 30, 400, edgeRule=WRAP_GRID),
		   automata.ElementaryAutomaton(400, 110, 400, edgeRule=WRAP_GRID),
		   None,
		   None,
		   automata.LifelikeAutomaton(400, 400, "B2/S", 100, edgeRule=WRAP_GRID)]

# A dropdown menu to pick the automaton the user wants.
autOptions = [ 'Rule 30', 'Rule 110', 'Toothpick Sequence', 'Langton\'s Ant', 'Seeds' ]
optionVar = tk.StringVar(base)
optionVar.set('Rule 30') #default rule
autMenu = tk.OptionMenu(settings, optionVar, *autOptions)

# A proxy class that does a number of things: store data pertinent to an
# automaton in immediate memory, convert between JSON data and automaton-
# specific rule strings, and alter configuration data.
# --- UNDER CONSTRUCTION ---
class AutomatonProxy:
	def __init__(self, colors=[(255, 255, 255), (0, 0, 0)]):
		self.aut = copy.deepcopy(autList[autOptions.index(optionVar.get())])
		self.autType = self.aut.get_aut_type()
		self.initCellStates = self.aut.cells
		self.colors = []
		self.width = 800
		self.height = 800

	# Sets the possible colors for the automaton. Note that colors[i] will
	# mark the color of the state of cells[i] in the automaton.
	def set_colors(self, colors):
		self.colors = colors

	# To know how a rule string might be constructed from the JSON data,
	# first we need to set the automaton type appropriately.
	def set_automaton(self, type):
		pass

	def set_dimensions(self, width, height):
		self.width = width
		self.height = height
		self.aut.resize(width, height)


	def set_dimensions(self, width):
		pass

	# Resets all values in the proxy to the default configuration for
	# each type of automaton.
	def reset_proxy(self):
		pass

	# Converts rules from JSON format to an automaton rule string and
	# loads the rules into the automaton object.
	def load_rule_string(self, jsonDictionary):
		pass

	# Sets the initial cell states based on an inputted array.
	def set_board_state(self):
		pass

	# Uses the current information to construct an image.
	def output_img(self):
		pass


class DialogSetInitial(sdg.Dialog):
	def __init__(self, master, aut):
		self.automaton = aut
		self.result = None
		super.__init__(master)

	def body(self, master):
		self.title("Set Initial Conditions")
		self.resizable(False, False)

		if self.automaton in ("Rule 30", "Rule 110"):
			tk.Button(self, text="Default").pack()
			tk.Button(self, text="Random").pack()


aut_proxy = AutomatonProxy()

def output_img():
	grid = []
	autCurrent = 0
	try:
		autCurrent = autList[autOptions.index(optionVar.get())]
		autCurrent.reset_board()
		if not (autCurrent.is_empty()):
			filename = fdg.asksaveasfilename( \
				parent = base, \
				title = "Save image to:", \
				initialdir = id, \
				filetypes = (("Portable Network Graphic", "*.png"), ("Bitmap", "*.bmp"), ("All files", "*.*")) \
				)

			if type(filename) is str and len(filename) > 0:
				grid = autCurrent.generate_grid()
				utilities.render_img([(0, 0, 0), (255, 255, 255)], grid, filename)
				mbx.showinfo("Success", "Image was rendered successfully at {0}".format(filename))

		else:
			mbx.showinfo("Error", "All cells in the starting configuration are empty.")
	except ValueError:
		mbx.showinfo("Error", "Invalid filename - please make sure you entered it correctly.")

	autCurrent.reset_board()


def set_init():
	pass


tk.Label(settings, text="Select an automaton: ").grid(row = 0, column = 0, sticky=tk.W + tk.E)
autMenu.grid(row = 0, column = 1, padx = 2, pady = 10, sticky=tk.W + tk.E)

startingCellsButton = tk.Button(settings, text="Set starting conditions", command=set_init)
startingCellsButton.grid(row = 1, column = 0, columnspan = 2, pady = 5, sticky=tk.W + tk.E)

previewImageButton = tk.Button(settings, text="Preview image")
previewImageButton.grid(row = 2, column = 0, columnspan = 2, pady = 5, sticky=tk.W + tk.E)

saveBMPButton = tk.Button(settings, text="Save image", command=output_img)
saveBMPButton.grid(row = 3, column = 0, columnspan = 2, pady = 5, sticky=tk.W + tk.E)

base.mainloop()
