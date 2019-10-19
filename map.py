from PIL import Image

class Map:
    def __init__(self, file_path):
        self.file_path = file_path
        self.elevation_data = []
        self.matrix = []
        self.unique_elevations = []
        self.gradient = {}

    
    def get_elevation_data(self):
        with open(self.file_path) as file_handler:
           self.elevation_data = file_handler.readlines()

    def get_topo_data(self):
        # [y[elev1, elev2, elev3, evel4] 
        for row in self.elevation_data:
            row = [int(x) for x in row.strip("\n").split(" ")]
            self.matrix.append(row)


    def get_unique_elevations(self):
        flat_list = [item for sublist in self.matrix for item in sublist]
        flat_list.sort()
        self.unique_elevations = set(flat_list)

    def build_gradient(self):
        max_elev = max(self.unique_elevations)
        min_elev = min(self.unique_elevations)
        for elev in self.unique_elevations:
            brightness = (elev - min_elev) / (max_elev - min_elev)
            greyscale = int(255 * brightness)
            self.gradient[elev] = (greyscale, greyscale, greyscale, 255)


map = Map("elevation_small.txt")

map.get_elevation_data()
map.get_topo_data()
map.get_unique_elevations()
map.build_gradient()


image = Image.new("RGBA", (600, 600), color=(0,0,0,255))
for y, row in enumerate(map.matrix):
    for x, elev in enumerate(row):
        image.putpixel((x, y), map.gradient[elev])
    
image.save('image.png')

