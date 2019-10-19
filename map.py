from PIL import Image

class Map:
    def __init__(self, file_path):
        self.file_path
    
    def elevation_data(self):
        with open(self.file_path) as file_handler:
            elevation_data = file_handler.readlines()
        return elevation_data

    def topo_data(self, elevation_data):
        # [y[elev1, elev2, elev3, evel4] 
        matrix = []
        for row in elevation_data:
            row = [int(x) for x in row.strip("\n").split(" ")]
            matrix.append(row)
        return matrix


    def unique_elevations(self, matrix):
        flat_list = [item for sublist in matrix for item in sublist]
        flat_list.sort()
        unique_values = set(flat_list)
        return unique_values

    def build_gradient(self, unique_values):
        gradient = {}
        max_elev = max(unique_values)
        min_elev = min(unique_values)
        for elev in unique_values:
            brightness = (elev - min_elev) / (max_elev - min_elev)
            greyscale = int(255 * brightness)
            gradient[elev] = (greyscale, greyscale, greyscale, 255)
        return gradient


data = elevation_data()
matrix = topo_data(data)
# print(matrix[0][0])
unique_values = unique_elevations(matrix)
gradient = build_gradient(unique_values)


image = Image.new("RGBA", (600, 600), color=(0,0,0,255))
for y, row in enumerate(matrix):
    for x, elev in enumerate(row):
        image.putpixel((x, y), gradient[elev])
    
image.save('image.png')

