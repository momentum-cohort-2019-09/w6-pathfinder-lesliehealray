from PIL import Image
from random import choice, randrange

class Map:
    def __init__(self, file_path):
        self.file_path = file_path
        self.elevation_data = []
        self.matrix = []
        self.unique_elevations = []
        self.gradient = {}
        self.width = 0
        self.height = 0
        self.image = None

    
    def get_elevation_data(self):
        with open(self.file_path) as file_handler:
           self.elevation_data = file_handler.readlines()

    def get_topo_data(self):
        # [[elev1, elev2], [elev3, evel4]] 
        for row in self.elevation_data:
            row = [int(x) for x in row.lstrip().rstrip("\n").split(" ")]
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
    
    def generate_image(self, filename):
        self.height = len(self.matrix)
        self.width =  len(self.matrix[0])
        self.image = Image.new("RGBA", (self.width, self.height), color=(0,0,0,255))
        for y, row in enumerate(self.matrix):
            for x, elev in enumerate(row):
                self.image.putpixel((x, y), self.gradient[elev])
        self.image.save(f'{filename}.png')

    def draw_path(self, filename):
        y = randrange(0, self.height)
        x = 0
        self.image.putpixel((x, y), (0, 128, 128, 1))
        elevation = self.matrix[y][x]
        for x in range(1, self.width-1):
            choices = []
            left = y-1
            right = y+1
            forward = y
            for y in [left, forward, right]:
                if (0 <= y < self.height):
                    choices.append({
                        'x': x, 'y': y, 'delta': abs(elevation - self.matrix[y][x])
                    })
            print([choice['delta'] for choice in choices])
            min_delta = min([choice['delta'] for choice in choices])
            print(min_delta)
            next_step = next((item for item in choices if item['delta'] == min_delta), None)
            print(next_step)
            self.image.putpixel((next_step["x"], next_step["y"]),(0, 128, 128, 1))
            y = next_step["y"]
        self.image.save(f'{filename}.png')




    def topo_map(self, filename):
        self.get_elevation_data()
        self.get_topo_data()
        self.get_unique_elevations()
        self.build_gradient()
        self.generate_image(filename)
        self.draw_path(filename)

   


map = Map("elevation_small.txt")
map.topo_map('foo')




