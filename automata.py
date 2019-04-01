# Some frameworks for different kinds of cellular automata.

import copy
import math
import random

import utilities

# Settings for the edges of the grid...
DEAD_EDGE = 0   # All cells outside the edges of the grid die.
WRAP_GRID = 1   # Attempting to write to cells outside the grid will write
                # to the opposite side of the grid.

# Settings for the default grid state. This will be implemented later...
CENTER_PIXEL      = 0        # The pixel in the center is on by default.
FULLY_RANDOM      = 1        # Every cell starts at a random state.
RANDOM_CENTER_5X5 = 2        # The cells in a 5x5 grid in the center start at random states. Not valid in 1D automata.

'''
This is the general layout of an automaton class.
I'll explain each one of these functions in great detail...
'''
class Automaton:
    # Returns a string with the automaton type.
    def get_aut_type(self):
        pass

    # Empties the board, and has a boolean for a default state - if it's
    # true, the states will reset to a default, and if false, they will
    # remain empty.
    def reset_board(self):
        pass

    # Returns a boolean stating whether or not all the cells are dead.
    def is_empty(self):
        pass

    # Changes the size of the board. Currently the render size also accounts
    # for the dead edges on the sides of the board - I'm planning on
    # implementing edge options (dead edge or grid wrap).
    def resize(self):
        pass

    # The number of iterations performed. For a 1D automaton the iteration
    # count should equal the vertical size of the image in pixels.
    def set_iteration_count(self):
        pass

    # Changes the state of the cell at the desired index.
    def set_cell_state(self):
        pass

    # Checks the state of the cell according to the edge-detection rule.
    def access_cell(self):
        pass

    # Runs the automaton through one iteration. In a 1D automaton this adds
    # a new row to the grid, whereas in a 2D automaton it just runs as normal.
    def iterate(self):
        pass

    # Runs an automaton through the number of iterations specified and returns
    # the array of grid states.
    def generate_grid(self):
        pass

'''
The classic elementary automaton that we all know and love. The rule for
the next state of each cell is defined by an 8-bit number (0-255), for which
each bit corresponds to a different arrangement of cell states in a cell's
neighborhood.

Rule definition: An 8-bit number, with each bit corresponding to a
configuration of different cell states.
'''
class ElementaryAutomaton(Automaton):
    def __init__(self, size, rule, iterations, edgeRule = DEAD_EDGE, \
                 startConfig = CENTER_PIXEL):
        self.cells = [0 for i in range(size)]
        self.size = size
        self.ruleString = format(rule, '#010b')[2:]
        self.iterations = iterations
        self.edgeRule = edgeRule

        if (startConfig == CENTER_PIXEL):
            self.cells[self.size // 2] = 1
        elif (startConfig == FULLY_RANDOM):
            for i in range(size):
                self.cells[i] = random.randint(0, 1)

        else:
            print("Start configuration not valid. Defaulting to CENTER_PIXEL.")
            self.cells[self.size // 2] = 1


    def get_aut_type(self):
        return "Elementary Automaton"


    def reset_board(self, startConfig = CENTER_PIXEL):
        for i in range(self.size):
            self.cells[i] = 0

        if (startConfig == CENTER_PIXEL):
            self.cells[self.size // 2] = 1
        elif (startConfig == FULLY_RANDOM):
            for i in range(size):
                self.cells[i] = random.randint(0, 1)


    def is_empty(self):
        isEmpty = True
        for i in self.cells:
            if i == 1:
                isEmpty = False

        return isEmpty


    def resize(self, size):
        self.cells = [0 for i in range(size)]
        self.size = size
        self.reset_board()


    def set_iteration_count(self, iterCount):
        self.iterations = iterCount
        self.reset_board()


    def access_cell(self, cellList, index):
        cell_state = 0
        if (index >= 0 and index < self.size):
            cell_state = cellList[index]
        else:
            if (self.edgeRule == WRAP_GRID):
                if (index < 0):
                    cell_state = self.access_cell(cellList, index + self.size)
                elif (index >= self.size):
                    cell_state = self.access_cell(cellList, index - self.size)

        return cell_state


    def set_cell_state(self, index, state):
        self.cells[index] = state


    def iterate(self):
        prevCells = copy.copy(self.cells)
        stateNumber = 0
        for i in range(self.size):
            self.cells[i] = 0
            stateNumber = math.floor(self.access_cell(prevCells, i+1) + 2*self.access_cell(prevCells, i) + \
                                     4*self.access_cell(prevCells, i-1))
            if (self.ruleString[7 - stateNumber] == '1'):
                self.cells[i] = 1


    def generate_grid(self):
        stateGrid = []
        stateGrid.append(copy.copy(self.cells))

        for i in range(self.iterations-1):
            self.iterate()
            stateGrid.append(copy.copy(self.cells))

        return stateGrid

'''
LIFELIKE AUTOMATON

A "Life-like" is any automaton that is similar in form to Conway's Game of
Life in the following pattern: the automaton is totalistic (meaning the
states of the cells within a cell's neighborhood are counted to determine
the next state of the cell) and each cell has two states - alive and dead.

A rulestring for a Life-like is defined in the following way: B[x]/S[y].
B denotes the number of cells required for a dead cell to come to life, and
S denotes the number of cells required for a live cell to remain alive.
[x] and [y] are lists of numbers that show the state counts, and they
contain numbers from 0 to 8.

Examples:
    - Conway's Game of Life: B3/S23
        - Produces highly complex behavior that I don't feel the need to explain.
    - Seeds: B2/S
        - Very simple rule. Things get chaotic very fast.
    - Diamoeba: B35678/S5678
        - Creates very large, fluctuating, almost organic patterns.
    - Day & Night: B3678/S34678
        - Symmetric automaton with very complex behavior.
'''
class LifelikeAutomaton:
    def __init__(self, rows, columns, rule, iterations, edgeRule = DEAD_EDGE, \
                 startConfig = RANDOM_CENTER_5X5):
        self.rows = rows
        self.cols = columns
        self.cells = [[0 for col in range(columns)] for row in range(rows)]
        # note: each cell is at self.cells[row][col]
        self.ruleString = rule
        self.iterations = iterations
        self.edgeRule = edgeRule
        self.bornCount = []
        self.aliveCount = []

        centerRow = rows // 2
        centerCol = columns // 2
        if (startConfig == CENTER_PIXEL):
            self.cells[centerRow][centerCol] = 1
        elif (startConfig == FULLY_RANDOM):
            for row in range(self.rows):
                for col in range(self.cols):
                    self.cells[row][col] = random.randint(0, 1)


        elif (startConfig == RANDOM_CENTER_5X5):
            for row in range(centerRow - 2, centerRow + 3):
                for col in range(centerCol - 2, centerCol + 3):
                    self.cells[row][col] = random.randint(0, 1)


        else:
            print("Start configuration not valid. Defaulting to RANDOM_CENTER_5X5...")
            for row in range(centerRow - 2, centerRow + 3):
                for col in range(centerCol - 2, centerCol + 3):
                    self.cells[row][col] = random.randint(0, 1)


        ruleSplit = rule.split("/")
        ruleSplit[0] = ruleSplit[0][1:]
        ruleSplit[1] = ruleSplit[1][1:]

        for i in ruleSplit[0]:
            self.bornCount.append(int(i))
        for i in ruleSplit[1]:
            self.aliveCount.append(int(i))


    def get_aut_type(self):
        return "Lifelike Automaton"


    def reset_board(self, startConfig = RANDOM_CENTER_5X5):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[0])):
                self.cells[i][j] = 0

        centerRow = self.rows // 2
        centerCol = self.cols // 2
        if startConfig == CENTER_PIXEL:
            self.cells[centerRow][centerCol] = 1

        elif startConfig == FULLY_RANDOM:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.cells[row][col] = random.randint(0, 1)


        elif startConfig == RANDOM_CENTER_5X5:
            for row in range(centerRow - 2, centerRow + 3):
                for col in range(centerCol - 2, centerCol + 3):
                    self.cells[row][col] = random.randint(0, 1)


    def is_empty(self):
        isEmpty = True
        for i in range(len(self.cells)):
            for j in range(len(self.cells[0])):
                if (self.cells[i][j] == 1):
                    isEmpty = False


        return isEmpty


    def resize(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [[0 for i in range(rows)] for i in range(cols)]
        self.reset_board()


    def set_iteration_count(self, iterCount):
        self.iterations = iterCount
        self.reset_board()


    def set_cell_state(self, row, col, state):
        self.cells[row][col] = state


    def access_cell(self, cellList, row, col):
        cellState = 0
        if (row >= 0 and row < self.rows):
            if (col >= 0 and col < self.cols):
                cellState = cellList[row][col]
            else:
                if (self.edgeRule == WRAP_GRID):
                    if (col < 0):
                        cellState = self.access_cell(cellList, row, col + self.cols)
                    elif (col >= self.cols):
                        cellState = self.access_cell(cellList, row, col - self.cols)


        else:
            if (self.edgeRule == WRAP_GRID):
                if (row < 0):
                    cell_state = self.access_cell(cellList, row + self.rows, col)
                else:
                    cell_state = self.access_cell(cellList, row - self.rows, col)

        return cellState


    def iterate(self):
        prevCells = copy.deepcopy(self.cells)
        stateNumber = 0
        for row in range(self.rows):
            for col in range(self.cols):
                stateNumber = \
                    self.access_cell(prevCells, row-1, col-1) + \
                    self.access_cell(prevCells, row-1, col) + \
                    self.access_cell(prevCells, row-1, col+1) + \
                    self.access_cell(prevCells, row, col-1) + \
                    self.access_cell(prevCells, row, col+1) + \
                    self.access_cell(prevCells, row+1, col-1) + \
                    self.access_cell(prevCells, row+1, col) + \
                    self.access_cell(prevCells, row+1, col+1)

                if prevCells[row][col] == 0:
                    if stateNumber in self.bornCount:
                        self.cells[row][col] = 1
                    else:
                        self.cells[row][col] = 0

                elif prevCells[row][col] == 1:
                    if stateNumber in self.aliveCount:
                        self.cells[row][col] = 1
                    else:
                        self.cells[row][col] = 0


    def generate_grid(self):
        stateGrid = []
        for i in range(self.iterations-1):
            self.iterate()

        stateGrid = copy.copy(self.cells)
        return stateGrid

'''
Below this divider is the automata that do not have rulestrings or aren't
part of the default automata (elementary, toothpick, ant, or Life-like).
These currently include:

    - Hodgepodge Machine
'''
# -----------------------------------------------------------------------------
'''
HODGEPODGE MACHINE

The idea behind this one is a bit more complex than the other ones. In essence,
each cell can be in one of N+1 states, or any state between 0 and N. If a cell
is in state 0, it is "healthy", and if it is in state N, it is "ill". If the
cell is any state in between 0 and N, it is "infected". Additionally, for the
automaton, we have two constants, k1, k2, and g - their use will make sense
later.

For each cell state, we do the following:
    - If the cell is healthy, we say that A is the number of infected cells and
      B is the number of ill cells within its neighborhood. The state of the
      cell is then given by the formula (A / k1) + (B / k2).
    - If a cell is infected, we say that S is the sum of the state numbers of
      the cell's neighbors and itself, and that A is the number of infected or
      ill cells in its neighborhood, not including itself. The cell's next state
      is given by (S / (A + 1)) + g.
    - If a cell is ill, it will miraculously become healthy.

The reason this is interesting is because it can mimic the kind of oscillating
chemical reactions that occur in a Petri dish. If you want to hear more about
that, look up the Belousov-Zhabotinsky reaction.
'''
class HodgepodgeMachine(Automaton):
    def __init__(self, rows, columns, stateCount, iterations, k1, k2, g, \
                 edgeRule=DEAD_EDGE):
        self.rows = rows
        self.cols = columns
        self.stateCount = stateCount
        self.iterCount = iterations

        self.k1 = k1
        self.k2 = k2
        self.g = g

        self.edgeRule = edgeRule

        self.cells = [[0 for col in range(self.cols)] for row in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col] = random.randint(0, self.stateCount)


    def get_aut_type(self):
        return "Hodgepodge Machine"


    def reset_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col] = random.randint(0, self.stateCount)


    def resize(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.reset_board()


    def set_iteration_count(self, iterations):
        self.iterCount = iterations


    def set_cell_state(self, row, col, state):
        self.cells[row][col] = state


    def access_cell(self, cellList, row, col):
        cellState = 0
        if (row >= 0 and row < self.rows):
            if (col >= 0 and col < self.cols):
                cellState = cellList[row][col]
            else:
                if (self.edgeRule == WRAP_GRID):
                    if (col < 0):
                        cellState = self.access_cell(cellList, row, col + self.cols)
                    elif (col >= self.cols):
                        cellState = self.access_cell(cellList, row, col - self.cols)



        else:
            if (self.edgeRule == WRAP_GRID):
                if (row < 0):
                    cellState = self.access_cell(cellList, row + self.rows, col)
                elif (row > self.rows):
                    cellState = self.access_cell(cellList, row - self.rows, col)

        return cellState


    def _state(self, cellList, row, col):
        stateString = ""
        if self.access_cell(cellList, row, col) == 0:
            stateString = "Healthy"
        elif self.access_cell(cellList, row, col) >= self.stateCount - 1:
            stateString = "Ill"
        else:
            stateString = "Infected"

        return stateString


    def iterate(self, iterNumber):
        prevCells = copy.deepcopy(self.cells)
        for row in range(self.rows):
            for col in range(self.cols):
                stateNumber = 0
                A = B = S = 0
                state = ""
                state = self._state(prevCells, row-1, col-1)
                if state == "Infected":
                    A += 1
                elif state == "Ill":
                    B += 1

                state = self._state(prevCells, row-1, col)
                if state == "Infected":
                    A += 1
                elif state == "Ill":
                    B += 1

                state = self._state(prevCells, row-1, col+1)
                if state == "Infected":
                    A += 1
                elif state == "Ill":
                    B += 1

                state = self._state(prevCells, row, col-1)
                if state == "Infected":
                    A += 1
                elif state == "Ill":
                    B += 1

                state = self._state(prevCells, row, col+1)
                if state == "Infected":
                    A += 1
                elif state == "Ill":
                    B += 1

                state = self._state(prevCells, row+1, col-1)
                if state == "Infected":
                    A += 1
                elif state == "Ill":
                    B += 1

                state = self._state(prevCells, row+1, col)
                if state == "Infected":
                    A += 1
                elif state == "Ill":
                    B += 1

                state = self._state(prevCells, row+1, col+1)
                if state == "Infected":
                    A += 1
                elif state == "Ill":
                    B += 1

                if self._state(prevCells, row, col) == "Healthy":
                    self.cells[row][col] = utilities.clamp(int(math.floor((A / float(self.k1)) + (B / float(self.k2)))), \
                                                           0, self.stateCount)

                elif self._state(prevCells, row, col) == "Ill":
                    self.cells[row][col] = 0

                else:
                    S = self.access_cell(prevCells, row-1, col-1) + \
                        self.access_cell(prevCells, row-1, col) + \
                        self.access_cell(prevCells, row-1, col+1) + \
                        self.access_cell(prevCells, row, col-1) + \
                        self.access_cell(prevCells, row, col) + \
                        self.access_cell(prevCells, row, col+1) + \
                        self.access_cell(prevCells, row+1, col-1) + \
                        self.access_cell(prevCells, row+1, col) + \
                        self.access_cell(prevCells, row+1, col+1)

                    self.cells[row][col] = utilities.clamp(int(math.floor(S / (A + B + 1) + self.g)), \
                                                           0, self.stateCount)


        print("Iteration #{0} completed.".format(iterNumber))


    def generate_grid(self):
        stateGrid = []
        for i in range(self.iterCount - 1):
            self.iterate(i + 1)

        stateGrid = copy.copy(self.cells)
        return stateGrid
