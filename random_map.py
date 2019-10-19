import random
from PIL import Image

# class Map:
#     image = 0
#     def __init__(self, file):
#         self.file = file


def topo_generator(min_e, max_e, width, height):
    matrix = []
    for y in range(0, height):
        matrix.append([])
        for x in range(0, width):
            if y == 0 and x == 0:
                matrix[y].append(random.randrange(min_e, max_e)) 
            elif x == 0:
                min_delta = int(matrix[y-1][x] * .70)
                max_delta = int(matrix[y-1][x] * 1.30)
                if min_delta == 0 or max_delta == 0:
                    min_delta = min_e
                    max_delta = max_e
                matrix[y].append(random.randrange(min_delta, max_delta))            
            else:
                min_delta = int(matrix[y][x-1] * .70)
                max_delta = int(matrix[y][x-1] * 1.30)
                if min_delta == 0 or max_delta == 0:
                    min_delta = min_e
                    max_delta = max_e
                matrix[y].append(random.randrange(min_delta, max_delta))
    return matrix    

def unique_elevations(matrix):
    flat_list = [item for sublist in matrix for item in sublist]
    flat_list.sort()
    unique_values = set(flat_list)
    return unique_values

def build_gradient(unique_values):
    gradient = {}
    max_elev = max(unique_values)
    min_elev = min(unique_values)
    for elev in unique_values:
        brightness = (elev - min_elev) / (max_elev - min_elev)
        greyscale = int(255 * brightness)
        gradient[elev] = (greyscale, greyscale, greyscale, 255)
    return gradient


HEIGHT = 500
WIDTH = 500
matrix = topo_generator(100, 5280, HEIGHT, WIDTH)
# print(matrix[0][0])
unique_values = unique_elevations(matrix)
gradient = build_gradient(unique_values)


image = Image.new("RGBA", (HEIGHT, WIDTH), color=(0,0,0,255))
for y, row in enumerate(matrix):
    for x, elev in enumerate(row):
        image.putpixel((x, y), gradient[elev])
    
image.save('random.png')

