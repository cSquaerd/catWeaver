# make sure you have Pillow installed - if not, install it with pip.
from PIL import Image

import math

# this function "carves" part of a 2D array that we want.
def carve_array(arr, start_col, start_row, row_length, col_length):
    newArray = [[0 for col in range(col_length)] for row in range(row_length)]

    for row in range(row_length):
        for col in range(col_length):
            newArray[row][col] = arr[row + start_row][col + start_col]


    return newArray

# outputs an image file, and takes two parameters:
# first, a list of RGB color tuples, and second, the actual array of cells. if
# arr[i][j] is n, the color used for that pixel at (i, j) will be colors[n].
# AFAIK it works for all common image types, including .bmp and .png.
# TODO: implement error-checking
def render_img(colors, arr, outputPath):
    img = Image.new("RGB", (len(arr), len(arr[0])))

    for row in range(len(arr)):
        for col in range(len(arr[0])):
            img.putpixel((col, row), (colors[arr[row][col]]))


    img.save(outputPath)
    return img

'''
Note: here's an example of how it's called.

cols = [(0, 0, 0), (255, 255, 255)]

a = [[0, 0, 1, 0, 0],
     [0, 1, 0, 1, 0],
     [1, 0, 0, 0, 1],
     [0, 1, 0, 1, 0],
     [0, 0, 1, 0, 0]]

render_img(cols, a, "path/to/file/location.png")
'''
# Pretty self-explanatory - converts color hex string (#RRGGBB)
# to an RGB tuple (0xRR, 0xGG, 0xBB).
def hex_string_to_RGB(hexString):
    rStr = "0x" + hexString[1:3]
    gStr = "0x" + hexString[3:5]
    bStr = "0x" + hexString[5:]

    rgb = (int(rStr, 0), int(gStr, 0), int(bStr, 0))
    return rgb

# Clamp a value so it never goes out of a range between two
# numbers.
def clamp(number, lowBound, highBound):
    n = number
    if n < lowBound:
        n = lowBound
    elif n > highBound:
        n = highBound

    return n

# Get a list of color tuples comprising a linear gradient.
def linear_gradient(color1, color2, amount):
    rInc = (color2[0] - color1[0]) / float(amount)
    gInc = (color2[1] - color1[1]) / float(amount)
    bInc = (color2[2] - color1[2]) / float(amount)

    index = 0

    gradient = []
    currentColor = list(color1)
    while index < amount:
        gradient.append((int(math.floor(currentColor[0])), int(math.floor(currentColor[1])), int(math.floor(currentColor[2]))))
        currentColor = (currentColor[0] + rInc, currentColor[1] + gInc, currentColor[2] + bInc)
        index += 1

    return gradient

# Render the current states of the automaton to the canvas.
# Warning: I REALLY should not have used a Tkinter canvas
# for this, since it's infuriatingly slow. Hence, it is
# disabled by default on all automata aside from 1-dimensional
# ones.
def render_to_ctx(cells, colors, img):
    for row in range(len(cells)):
        for col in range(len(cells[0])):
            cellState = cells[row][col]
            img.put("#{:02x}{:02x}{:02x}".format(colors[cellState][0], colors[cellState][1], colors[cellState][2]), (col, row))
