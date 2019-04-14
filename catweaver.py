import tkinter as tk
import tkinter.simpledialog as sdg
import tkinter.messagebox as mbx
import tkinter.font as tkf
import tkinter.filedialog as fdg
import tkinter.colorchooser as clc
import math
import random as rnd
import platform as pt
import time
import copy
import json

# For the utilities.py file
import utilities
import automata

if pt.system() == "Linux":
	id = "~"
elif pt.system() == "Windows":
	id = "C:\\"

stringCreateRules = "Create Rules (with dialog)"
stringLoadRules = "Load Rules (from .json)"
stringViewRules = "View Rules (from .json)"
stringModifyRules = "Modify Rules (from .json)"
tupleRuleNs = ("Rule 30", "Rule 110")
tupleFileTypes = ( \
	("Custom Automaton Rules", "*.json"), \
	("All Files", "*.*") \
)
dictCustomRules = {}

# Rule customization root dialog window
class dialogRootCustomizeRules(sdg.Dialog):
	def __init__(self, master, atmt):
		self.automaton = atmt
		super().__init__(master)
	def body(self, master):
		self.title("Customize Rules")
		self.resizable(False, False)

		if self.automaton in ("Toothpick Sequence", "Seeds", "Hodgepodge Machine"):
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
				stringViewRules, \
				stringModifyRules \
			)
			self.optionsCustomize.pack()

	def apply(self):
		self.result = self.varCustomizeChoice.get()

# Rule customization "leaf" dialog window
class dialogNewCustomizeRules(sdg.Dialog):
	def __init__(self, master, atmt, r = None, v = False):
		self.automaton = atmt
		self.oldRules = r
		self.view = v
		super().__init__(master)
	def refreshLAFields(self):
		for w in self.frameLAColors.grid_slaves():
			w.destroy()
		for w in self.frameLARules.grid_slaves():
			w.destroy()

		tk.Label(self.frameLARules, text = "Read Color", font = fontNormal).grid(row = 0, column = 0)
		tk.Label(self.frameLARules, text = "Rotation", font = fontNormal).grid(row = 0, column = 1)
		tk.Label(self.frameLARules, text = "Write Color", font = fontNormal).grid(row = 0, column = 2)

		for i in range(0, self.varNumColors.get()):
			localField = {}

			tk.Label( \
				self.frameLAColors, text = "Color " + str(i) + ':', \
				font = fontNormal \
			).grid(row = i, column = 0)
			localField["varColor"] = tk.StringVar(self, '#' + \
				6 * hex(0xf * (i + 1) // self.varNumColors.get())[2] \
			)
			localField["btnColor"] = tk.Button( \
				self.frameLAColors, \
				textvariable = localField["varColor"], \
				background = localField["varColor"].get(), \
				foreground = '#' + "{:06x}".format( \
					int(localField["varColor"].get()[1:], base = 16) ^ 0xFFFFFF \
				), \
				font = fontNormal \
			)
			localField["btnColor"].grid(row = i, column = 1)

			localField["varRead"] = tk.IntVar(self, i)
			tk.OptionMenu( \
				self.frameLARules, localField["varRead"], \
				i \
			).grid(row = i + 1, column = 0)

			localField["varRotate"] = tk.StringVar(self, "0")
			tk.OptionMenu( \
				self.frameLARules, localField["varRotate"], \
				"0", "L90", "R90", "180" \
			).grid(row = i + 1, column = 1)

			localField["varWrite"] = tk.IntVar(self, 0)
			tk.OptionMenu( \
				self.frameLARules, localField["varWrite"], \
				*tuple(range(0, self.varNumColors.get())) \
			).grid(row = i + 1, column = 2)
			if self.loadLA:
				for k in localField.keys():
					if k != "btnColor":
						localField[k].set(self.oldRules[i][k])

			self.fields[i] = localField
		self.fields[0]["btnColor"].config(command = lambda : self.changeColor(0))
		self.fields[1]["btnColor"].config(command = lambda : self.changeColor(1))
		if self.varNumColors.get() > 2:
			self.fields[2]["btnColor"].config(command = lambda : self.changeColor(2))
		if self.varNumColors.get() > 3:
			self.fields[3]["btnColor"].config(command = lambda : self.changeColor(3))
		if self.varNumColors.get() > 4:
			self.fields[4]["btnColor"].config(command = lambda : self.changeColor(4))
		if self.varNumColors.get() > 5:
			self.fields[5]["btnColor"].config(command = lambda : self.changeColor(5))
		if self.varNumColors.get() > 6:
			self.fields[6]["btnColor"].config(command = lambda : self.changeColor(6))
		if self.varNumColors.get() > 7:
			self.fields[7]["btnColor"].config(command = lambda : self.changeColor(7))
		if self.varNumColors.get() > 8:
			self.fields[8]["btnColor"].config(command = lambda : self.changeColor(8))
		if self.varNumColors.get() > 9:
			self.fields[9]["btnColor"].config(command = lambda : self.changeColor(9))
		if self.varNumColors.get() > 10:
			self.fields[10]["btnColor"].config(command = lambda : self.changeColor(10))
		if self.varNumColors.get() > 11:
			self.fields[11]["btnColor"].config(command = lambda : self.changeColor(11))
		if self.varNumColors.get() > 12:
			self.fields[12]["btnColor"].config(command = lambda : self.changeColor(12))
		if self.varNumColors.get() > 13:
			self.fields[13]["btnColor"].config(command = lambda : self.changeColor(13))
		if self.varNumColors.get() > 14:
			self.fields[14]["btnColor"].config(command = lambda : self.changeColor(14))
		if self.varNumColors.get() > 15:
			self.fields[15]["btnColor"].config(command = lambda : self.changeColor(15))

	def refreshRuleID(self):
		k = 0
		for n in range(8):
			k += 2 ** (n) if self.fields[n].get() else 0
		self.ruleID.set(k)

	def changeColor(self, n):
		if self.automaton == "Rule N":
			self.fields[n].set( \
				clc.askcolor( \
					parent = self, \
					title = "Choose a color:", \
					initialcolor = self.fields[n].get() \
				)[1] \
			)
			self.fields[n - 2].config( \
				background = self.fields[n].get(), \
				foreground = '#' + "{:06x}".format( \
					int(self.fields[n].get()[1:], base = 16) ^ 0xFFFFFF \
				)
			)
		elif self.automaton == "Langton\'s Ant":
			self.fields[n]["varColor"].set( \
				clc.askcolor( \
					parent = self, \
					title = "Choose a color:", \
					initialcolor = self.fields[n]["varColor"].get() \
				)[1] \
			)
			self.fields[n]["btnColor"].config( \
				background = self.fields[n]["varColor"].get(), \
				foreground = '#' + "{:06x}".format( \
					int(self.fields[n]["varColor"].get()[1:], base = 16) ^ 0xFFFFFF \
				)
			)

	def body(self, master):
		if self.automaton in tupleRuleNs:
			self.automaton = "Rule N"
		self.title("Customize " + self.automaton + " Rules")
		self.resizable(False, False)
		if self.view:
			tk.Label( \
				master, text = "Read-Only Mode: Changes Will Not Be Saved", \
				font = fontNormal \
			).grid(row = 3, column = 0, columnspan = 8, pady = 2)
		self.fields = {}
		self.fields[-1] = self.automaton

		if self.automaton == "Rule N":
			tk.Label( \
				master, \
				text = "Each binary string corresponds to a pattern of cells. The value you set for each pattern is the value the center cell of the pattern will become in the next generation.", \
				justify = tk.LEFT, wraplength = 400, font = fontNormal \
			).grid(row = 0, column = 0, columnspan = 8)
			self.tempLF = tk.LabelFrame( \
				master, text = "Rule ID", font = fontNormal \
			)
			self.ruleID = tk.IntVar(self, 0)
			tk.Label(self.tempLF, textvariable = self.ruleID, font = fontNormal).pack()
			self.tempLF.grid(row = 2, column = 0, columnspan = 2, padx = 2)
			self.ruleNLabels = ("111", "110", "101", "100", "011", "010", "001", "000")

			for n in range(8):
				self.tempLF = tk.LabelFrame( \
					master, text = self.ruleNLabels[n], font = fontNormal \
				)
				self.fields[7 - n] = tk.BooleanVar(self, False)
				tk.OptionMenu( \
					self.tempLF, self.fields[7 - n], \
					False, True, \
					command = lambda n: self.refreshRuleID() \
				).pack()
				self.tempLF.grid(row = 1, column = n, padx = 2)
				if type(self.oldRules) is not type(None):
					self.fields[7 - n].set(self.oldRules[7 - n])

			self.fields[-2] = tk.StringVar(self, "#000000")
			self.fields[-3] = tk.StringVar(self, "#FFFFFF")
			ruleNColorLabels = ("Inactive Color", "Active Color")
			for n in range (2):
				if type(self.oldRules) is not type(None):
					self.fields[-2 - n].set(self.oldRules[-2 - n])
				self.tempLF = tk.LabelFrame( \
					master, text = ruleNColorLabels[n], font = fontNormal \
				)
				self.fields[-4 - n] = tk.Button( \
					self.tempLF, \
					textvariable = self.fields[-2 - n], \
					background = self.fields[-2 - n].get(), \
					foreground = '#' + "{:06x}".format( \
						int(self.fields[-2 - n].get()[1:], base = 16) ^ 0xFFFFFF \
					), \
					font = fontNormal \
				)
				self.fields[-4 - n].pack()
				self.tempLF.grid( \
					row = 2, column = 3 * (n + 1) - 1, columnspan = 3, \
					padx = 2, pady = 4 \
				)

			self.fields[-4].config( \
				command = lambda : self.changeColor(-2)
			)
			self.fields[-5].config( \
				command = lambda : self.changeColor(-3)
			)

		elif self.automaton == "Langton\'s Ant":
			self.loadLA = False
			self.varNumColors = tk.IntVar(self, 2)
			self.optionsNumColors = tk.OptionMenu( \
				master, self.varNumColors, \
				2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, \
				command = lambda n : self.refreshLAFields() \
			)
			self.frameLAColors = tk.LabelFrame( \
				master, text = "Colors", \
				relief = "ridge", bd = 2, font = fontNormal \
			)
			self.frameLARules = tk.LabelFrame( \
				master, text = "Rules", \
				relief = "ridge", bd = 2, font = fontNormal \
			)
			if type(self.oldRules) is not type(None):
				self.varNumColors.set(max(self.oldRules.keys()) + 1)
				self.loadLA = True

			tk.Label( \
				master, text = "Number of Colors:", \
				font = fontNormal \
			).grid(row = 0, column = 0)
			self.optionsNumColors.grid(row = 0, column = 1)
			self.frameLAColors.grid(row = 1, column = 0, columnspan = 2, padx = 2)
			self.frameLARules.grid(row = 1, column = 2, columnspan = 2, padx = 2)
			self.refreshLAFields()

		else:
			tk.Label(self, text = "Under construction!", font = fontBig).pack()
	def apply(self):
		if hasattr(self, "fields"):
			self.result = self.fields
	def validate(self):
		errorTitle = "Color Error"
		errorMessage = "The color fields must be six-digit hex values preceded by a # symbol."
		if self.automaton == "Langton\'s Ant":
			try:
				for i in range(self.varNumColors.get()):
					int(self.fields[i]["varColor"].get()[1:], base = 16)
					if len(self.fields[i]["varColor"].get()) != 7:
						int("foo")
				return 1
			except ValueError:
				mbx.showerror(errorTitle, errorMessage)
				return 0
		elif self.automaton == "Rule N":
			try:
				for i in range(-3, -1):
					int(self.fields[i].get()[1:], base = 16)
					if len(self.fields[i].get()) != 7:
						int("bar")
				return 1
			except ValueError:
				mbx.showerror(errorTitle, errorMessage)
				return 0
		else:
			return 1

# Rule customization function
def customizeRules():
	def saveRuleFile(result):
		if type(result) is dict:
			savefile = fdg.asksaveasfilename( \
				parent = base, \
				title = "Select a file to save to:", \
				initialdir = id, \
				filetypes = tupleFileTypes \
			)
			if type(savefile) is str and len(savefile) > 0:
				if optionVar.get() in ("Rule 30", "Rule 110"):
					del result[-5]
					del result[-4]
					for n in [-3, -2] + list(range(8)):
						result[n] = result[n].get()
				elif optionVar.get() == "Langton\'s Ant":
					for n in range(len(list(result.keys())) - 1):
						del result[n]["btnColor"]
						for k in result[n].keys():
							if type(result[n][k]) in [tk.StringVar, tk.IntVar]:
								result[n][k] = result[n][k].get()
				f = open(savefile, "w")
				f.write(json.dumps(result, sort_keys = True, indent = 2))
				f.close()
				#print("Main result:", result)
				#print("In JSON Format:", json.dumps(result, sort_keys = True, indent = 4))
				mbx.showinfo("Success!", "Your file was saved successfully.")

	choice = dialogRootCustomizeRules(base, optionVar.get()).result
	if choice == stringCreateRules:
		result = dialogNewCustomizeRules(base, optionVar.get()).result
		saveRuleFile(result)
	elif choice in (stringLoadRules, stringModifyRules) or \
		(choice == stringViewRules and labelCustomLoaded.config()["state"][4] != "normal"):
		global dictCustomRules
		loadfile = fdg.askopenfilename( \
			parent = base, \
			title = "Select a file to load from:", \
			initialdir = id, \
			filetypes = tupleFileTypes \
		)
		if type(loadfile) is str and len(loadfile) > 0:
			try:
				f = open(loadfile, "r")
				loaded = json.loads(f.read())
				originalKeys = list(loaded.keys())
				for s in originalKeys:
					loaded[int(s)] = loaded[s]
					del loaded[s]
			except:
				mbx.showinfo("File Load Error", "Unable to load the rules from " + loadfile + ".")
				return None
			if loaded[-1][:4] != optionVar.get()[:4]:
				optionVarTranslator = {"Rule N": "Rule 30", "Langton\'s Ant": "Langton\'s Ant"}
				if mbx.askyesno( \
					"Different Automaton Detected", \
					"This file contains rules for the automaton: \"" \
						+ loaded[-1] \
						+ "\". Do you wish to continue loading and switch to the automaton in the file?" \
					):
					optionVar.set(optionVarTranslator[loaded[-1]])
				else:
					return None
			dictCustomRules = loaded
			automatonAcronyms = {"Rule N": "ELMT", "Langton\'s Ant": "LANG"}
			labelCustomLoaded.config( \
				state = "normal", \
				text = "Custom Rules Loaded [" + automatonAcronyms[dictCustomRules[-1]] + ']' \
			)
			mbx.showinfo("Success!", "Your file was loaded successfully.")
		else:
			return None

		if choice == stringModifyRules:
			result = dialogNewCustomizeRules(base, optionVar.get(), dictCustomRules).result
			saveRuleFile(result)

	if choice == stringViewRules:
		dialogNewCustomizeRules(base, optionVar.get(), dictCustomRules, True)
	return None

def loadCheck(newOption):
	global dictCustomRules
	if len(dictCustomRules) > 0 and dictCustomRules[-1][:4] != newOption[:4]:
		if mbx.askyesno( \
			"Automaton Change Pending", \
			"Changing your automaton will unload the custom ruleset currently loaded. Do you wish to proceed?" \
		):
			dictCustomRules = {}
			labelCustomLoaded.config( \
				state = "disabled", \
				text = "Custom Rules Unloaded" \
			)
		else:
			optionVar.set("Rule 30" if dictCustomRules[-1] == "Rule N" else "Langton\'s Ant")

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

# A list of the automata that are loaded.
autList = [automata.ElementaryAutomaton(400, 30, 400, edgeRule=automata.WRAP_GRID),
		   automata.ElementaryAutomaton(400, 110, 400, edgeRule=automata.WRAP_GRID),
		   None,
		   None,
		   automata.LifelikeAutomaton(400, 400, "B2/S", 100, \
		   							  edgeRule=automata.WRAP_GRID, \
									  startConfig=automata.RANDOM_CENTER_5X5),
		   automata.HodgepodgeMachine(400, 400, 200, 200, 3, 3, 28, edgeRule=automata.WRAP_GRID)]

# A dropdown menu to pick the automaton the user wants.
autOptions = [ 'Rule 30', 'Rule 110', 'Toothpick Sequence', 'Langton\'s Ant', 'Seeds', \
 			   'Hodgepodge Machine' ]
optionVar = tk.StringVar(base)
optionVar.set('Rule 30') #default rule
autMenu = tk.OptionMenu(settings, optionVar, *autOptions, command = loadCheck)

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


def load_automaton():
	global dictCustomRules
	rule = None
	aut = None
	if dictCustomRules[-1] == "Rule N":
		rule = 0
		for i in range(8):
			rule += (2 ** i) * dictCustomRules[i]

		aut = automata.ElementaryAutomaton(400, rule, 400, edgeRule=automata.WRAP_GRID)

	elif dictCustomRules[-1] == "Langton's Ant":
		mbx.showerror("Error", "The implementation of Langton's ant is under construction.")
		aut = autList[autOptions.index(optionVar.get())]

	else:
		mbx.showerror("Wait, what?", "This shouldn't be happening!")
		aut = autList[autOptions.index(optionVar.get())]

	return aut


def output_img():
	global dictCustomRules
	grid = []
	colors = []
	autCurrent = None
	try:
		if not dictCustomRules:
			autCurrent = autList[autOptions.index(optionVar.get())]
		else:
			autCurrent = load_automaton()

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
				if (autCurrent.get_aut_type() == "Hodgepodge Machine"):
					colors = utilities.linear_gradient((255, 0, 0), (0, 0, 0), 201)
					utilities.render_img(colors, grid, filename)
				else:
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

btnCustomRules = tk.Button(settings, text = "Customize Automata Rules", command = customizeRules)
btnCustomRules.grid(row = 3, column = 0, columnspan = 2, pady = 5, sticky = tk.W + tk.E)
labelCustomLoaded = tk.Label(settings, text = "Custom Rules Unloaded", bd = 2, relief = "ridge", state = "disabled")
labelCustomLoaded.grid(row = 4, column = 0, columnspan = 2, pady = 5, sticky = tk.W + tk.E)

saveBMPButton = tk.Button(settings, text="Save image", command=output_img)
saveBMPButton.grid(row = 5, column = 0, columnspan = 2, pady = 5, sticky=tk.W + tk.E)
# Sean, I didn't know about the sticky option to get the buttons to
# Span the frame theyre in. A neat trick. - Charlie

base.mainloop()
