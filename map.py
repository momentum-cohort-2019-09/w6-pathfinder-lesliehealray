from PIL import Image, ImageDraw

# class Map:
#     image = 0
#     def __init__(self, file):
#         self.file = file



image = Image.new("RGBA", (600, 600), color=(0,0,0,255))
draw = ImageDraw.Draw(image)
image.save('image.png')

def elevation_data():
    with open("elevation_small.txt") as file_handler:
        elevation_data = file_handler.readlines()
    return elevation_data

def topo_data(elevation_data):
    # [[0, 0, 10], [1, 0,15]]
    matrix = []
    for row in elevation_data:
        row = [int(x) for x in row.strip("\n").split(" ")]
        matrix.append(row)
    return matrix

data = elevation_data()
matrix = topo_data(data)
print(matrix[0][0])


def build_gradient(matrix):
    flat_list = [item for sublist in matrix for item in sublist]
    unique_values = set(flat_list)
    unique_values.sort()
    
    return unique_values
