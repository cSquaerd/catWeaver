# Some frameworks for different kinds of cellular automata.

import copy
import math

# Elementary automata are 1-dimensional, and the next state of each cell
# depends on the state of the cells in their neighborhoods.
class ElementaryAutomaton:
    def __init__(self, size, rule, iterations, isDefaultStart = True):
        self.cells = [0 for i in range(size)]
        self.size = size
        self.ruleString = format(rule, '#010b')[2:]
        self.iterations = iterations
        if (isDefaultStart):
            self.cells[self.size // 2] = 1

    def reset_board(self, isDefaultStart = True):
        for i in range(self.size):
            self.cells[i] = 0

        if (isDefaultStart):
            self.cells[self.size // 2] = 1

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

    def toggle_cell(self, index):
        self.cells[index] = abs(self.cells[index] - 1)


    def iterate(self):
        prevCells = copy.copy(self.cells)
        stateNumber = 0
        for i in range(1, self.size-1):
            self.cells[i] = 0
            stateNumber = math.floor(prevCells[i+1] + 2*prevCells[i] + \
                                     4*prevCells[i-1])
            if (self.ruleString[7 - stateNumber] == '1'):
                self.cells[i] = 1


    def generate_grid(self):
        stateGrid = []
        stateGrid.append(copy.copy(self.cells))

        for i in range(self.iterations):
            self.iterate()
            stateGrid.append(copy.copy(self.cells))

        return stateGrid
