import tkinter as tk
import tkinter.simpledialog as sdg
import tkinter.messagebox as mbx
import tkinter.font as tkf
import tkinter.filedialog as fdg
import random as rnd
import platform as pt
import time
import json

# For the utilities.py file
import utilities

if pt.system() == "Linux":
	id = "~"
elif pt.system() == "Windows":
	id = "C:\\"

stringCreateRules = "Create Rules (with dialog)"
stringLoadRules = "Load Rules (from .json)"
stringModifyRules = "Modify Rules (from .json)"
tupleRuleNs = ("Rule 30", "Rule 110")

# Rule customization root dialog window
class dialogRootCustomizeRules(sdg.Dialog):
	def __init__(self, master, atmt):
		self.automaton = atmt
		super().__init__(master)
	def body(self, master):
		self.title("Customize Rules")
		self.resizable(False, False)

		if self.automaton in ("Toothpick Sequence", "Seeds"):
			tk.Label(self, text = "Your selected automaton does not support customization.", font = fontNormal).pack()
			self.varCustomizeChoice = tk.StringVar(self, "")

		else:
			if self.automaton in tupleRuleNs:
				self.automaton = "Rule N"
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
		if self.automaton in tupleRuleNs:
			self.automaton = "Rule N"
		self.title("Customize " + self.automaton + " Rules")
		self.resizable(False, False)
		if self.automaton == "Rule N":
			tk.Label( \
				master, \
				text = "Each binary string corresponds to a pattern of cells. The value you set for each pattern is the value the center cell of the pattern will become in the next generation.", \
				justify = tk.LEFT, wraplength = 400, font = fontNormal \
			).grid(row = 0, column = 0, columnspan = 8)
			self.ruleNLabels = ("111", "110", "101", "100", "011", "010", "001", "000")
			self.fields = {}

			for n in range(8):
				self.tempLF = tk.LabelFrame( \
					master, text = self.ruleNLabels[n], font = fontNormal \
				)
				self.fields[7 - n] = tk.BooleanVar(self, False)
				tk.OptionMenu( \
					self.tempLF, self.fields[7 - n], \
					False, True \
				).pack()
				self.tempLF.grid(row = 1, column = n, padx = 2)

		elif self.automaton == "Langton\'s Ant":
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
			self.frameLAColors.grid(row = 1, column = 0, columnspan = 2, padx = 2)
			self.frameLARules.grid(row = 1, column = 2, columnspan = 2, padx = 2)
			self.refreshLAFields()
		else:
			tk.Label(self, text = "Under construction!", font = fontBig).pack()
	def apply(self):
		if hasattr(self, "fields"):
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
				if option_var.get() in ("Rule 30", "Rule 110"):
					for n in result.keys():
						result[n] = result[n].get()
				elif option_var.get() == "Langton\'s Ant":
					for n in result.keys():
						for k in result[n].keys():
							if type(result[n][k]) in [tk.StringVar, tk.IntVar]:
								result[n][k] = result[n][k].get()
				print("Main result:", result)
				print("In JSON Format:", json.dumps(result, sort_keys = True, indent = 4))
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
