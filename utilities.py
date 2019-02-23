# make sure you have Pillow installed - if not, install it with pip.
from PIL import Image

# this function "carves" part of a 2D array that we want.
def carve_array(arr, start_col, start_row, row_length, col_length):
    newArray = [[0 for col in range(col_length)] for row in range(row_length)]

    for row in range(row_length):
        for col in range(col_length):
            newArray[row][col] = arr[row + start_row][col + start_col]


    return newArray

# outputs a .png file, and takes two parameters:
# first, a list of RGB color tuples, and second, the actual array of cells. if
# arr[i][j] is n, the color used for that pixel at (i, j) will be colors[n].
# AFAIK it works for all common image types, including .bmp and .png.
# TODO: implement error-checking
def render_img(colors, arr, outputPath):
    img = Image.new("RGB", (len(arr), len(arr[0])))
    pixels = img.load()

    for row in range(len(arr)):
        for col in range(len(arr[0])):
            pixels[col, row] = colors[arr[row][col]]

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
