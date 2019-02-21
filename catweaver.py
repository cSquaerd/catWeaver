import tkinter as tk
import tkinter.simpledialog as sdg
import tkinter.messagebox as mbx
import tkinter.font as tkf
import tkinter.filedialog as fdg
import random as rnd
import platform as pt
import time

# For the utilities.py file
import utilities

if pt.system() == "Linux":
	id = "~"
elif pt.system() == "Windows":
	id = "C:\\"

stringCreateRules = "Create Rules (with dialog)"
stringLoadRules = "Load Rules (from .json)"
stringModifyRules = "Modify Rules (from .json)"

# Rule customization root dialog window
class dialogRootCustomizeRules(sdg.Dialog):
	def __init__(self, master, atmt):
		self.automaton = atmt
		super().__init__(master)
	def body(self, master):
		self.title("Customize Rules")
		self.resizable(False, False)
		self.varCustomizeChoice = tk.StringVar(self, stringCreateRules)
		tk.Label(self, text = "Current Automaton:", font = fontNormal).pack()
		tk.Label(self, text = self.automaton, font = fontNormal).pack()
		self.optionsCustomize = tk.OptionMenu( \
			self, \
			self.varCustomizeChoice, \
			stringCreateRules, \
			stringLoadRules, \
			stringModifyRules \
		)
		self.optionsCustomize.pack()
	def apply(self):
		self.result = self.varCustomizeChoice.get()

# Rule customization "leaf" dialog window
class dialogNewCustomizeRules(sdg.Dialog):
	def __init__(self, master, atmt):
		self.automaton = atmt
		super().__init__(master)
	def refreshLAFields(self):
		for w in self.frameLAColors.grid_slaves():
			w.destroy()
		for w in self.frameLARules.grid_slaves():
			w.destroy()

		tk.Label(self.frameLARules, text = "Read Color", font = fontNormal).grid(row = 0, column = 0)
		tk.Label(self.frameLARules, text = "Rotation", font = fontNormal).grid(row = 0, column = 1)
		tk.Label(self.frameLARules, text = "Write Color", font = fontNormal).grid(row = 0, column = 2)

		self.fields = {}
		for i in range(0, self.varNumColors.get()):
			localField = {}


			tk.Label( \
				self.frameLAColors, text = "Color " + str(i), \
				font = fontNormal \
			).grid(row = i, column = 0)
			localField["varColor"] = tk.StringVar(self, "#000000")
			tk.Entry( \
				self.frameLAColors, \
				textvariable = localField["varColor"], \
				font = fontNormal \
			).grid(row = i, column = 1)

			localField["varRead"] = tk.IntVar(self, i)
			tk.OptionMenu( \
				self.frameLARules, localField["varRead"], \
				i \
			).grid(row = i + 1, column = 0)

			localField["varRotate"] = tk.StringVar(self, "L90")
			tk.OptionMenu( \
				self.frameLARules, localField["varRotate"], \
				"L90", "R90", "180" \
			).grid(row = i + 1, column = 1)

			localField["varWrite"] = tk.IntVar(self, 0)
			tk.OptionMenu( \
				self.frameLARules, localField["varWrite"], \
				*tuple(range(0, self.varNumColors.get())) \
			).grid(row = i + 1, column = 2)

			self.fields[i] = localField

	def body(self, master):
		self.title("Customize " + self.automaton + " Rules")
		self.resizable(False, False)
		if self.automaton == "Langton\'s Ant":
			self.varNumColors = tk.IntVar(self, 2)
			self.optionsNumColors = tk.OptionMenu( \
				master, self.varNumColors, \
				2, 3, 4, 5, 6, 7, 8, \
				command = lambda n : self.refreshLAFields() \
			)
			self.buttonRefresh = tk.Button( \
				master, text = "Refresh Fields", \
				command = self.refreshLAFields, \
				font = fontNormal \
			)
			self.frameLAColors = tk.LabelFrame( \
				master, text = "Colors", \
				relief = "ridge", bd = 2, font = fontNormal \
			)
			self.frameLARules = tk.LabelFrame( \
				master, text = "Rules", \
				relief = "ridge", bd = 2, font = fontNormal \
			)

			tk.Label( \
				master, text = "Number of Colors:", \
				font = fontNormal \
			).grid(row = 0, column = 0)
			self.optionsNumColors.grid(row = 0, column = 1)
			#self.buttonRefresh.grid(row = 0, column = 3)
			self.frameLAColors.grid(row = 1, column = 0, columnspan = 2)
			self.frameLARules.grid(row = 1, column = 2, columnspan = 2)
			self.refreshLAFields()
		else:
			tk.Label(self, text = "Under construction!", font = fontBig).pack()
	def apply(self):
		self.result = self.fields

# Rule customization function
def customizeRules():
	choice = dialogRootCustomizeRules(base, option_var.get()).result
	if choice == stringCreateRules:
		result = dialogNewCustomizeRules(base, option_var.get()).result
		print(result)
		if type(result) is dict:
			savefile = fdg.asksaveasfilename( \
				parent = base, \
				title = "Select a file to save to:", \
				initialdir = id, \
				filetypes = ( \
					("Custom Automaton Rules", "*.json"), \
					("All Files", "*.*") \
				) \
			)
			if type(savefile) is str and len(savefile) > 0:
				print(savefile)
				mbx.showinfo("Success!", "Your file was saved successfully.")
	return None

base = tk.Tk()
base.title("Cellular Automata Tiling Weaver")
base.resizable(False, False)

# Some fonts
fontNormal = tkf.Font(family = "Consolas", size = 10)
fontBig = tkf.Font(family = "Consolas", size = 20)

viewer = tk.LabelFrame(base, text="Image Render", bd = 4, font=fontNormal)
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

btnCustomRules = tk.Button(settings, text = "Customize Automata Rules", command = customizeRules)
btnCustomRules.grid(row = 3, column = 0, columnspan = 2, pady = 5, sticky = tk.W + tk.E)
# Sean, I didn't know about the sticky option to get the buttons to
# Span the frame theyre in. A neat trick. - Charlie

saveBMPButton = tk.Button(settings, text="Save .BMP")
saveBMPButton.grid(row = 4, column = 0, pady = 5, sticky=tk.W + tk.E)
savePNGButton = tk.Button(settings, text="Save .PNG")
savePNGButton.grid(row = 4, column = 1, pady = 5, sticky=tk.W + tk.E)

base.mainloop()
