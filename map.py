from PIL import Image
from random import choice, randrange


class Map:
    def __init__(self, file_path, all_paths=False):
        self.file_path = file_path
        self.elevation_data = []
        self.matrix = []
        self.unique_elevations = []
        self.gradient = {}
        self.width = 0
        self.height = 0
        self.image = None
        self.all_paths = all_paths

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

    def draw_path(self, filename, all_paths):
        if all_paths:
            y_coordinates = range(0, self.height) 
        else:
            y_coordinates = [randrange(0, self.height)]
        for y in y_coordinates:
            x = 0 # set x coordinate to left side of the image
            self.image.putpixel((x, y), (0, 128, 128, 1)) # color the x, y starting coordinate
            elevation = self.matrix[y][x] # store the starting elevation
            for x in range(1, self.width-1): # iterate over the width of the image by x axis
                choices = [] # prepare an empty list hold information about potential path choices
                left = y-1 # defines y coordinate for the potential step to the left
                right = y+1 # defines the y coordinate for the potential step to the right
                forward = y # defines the y coordinate for the potential step forward
                for y in [left, forward, right]: # iterate through three possible steps
                    if (0 <= y < self.height): # ignore steps if above or below the height of the image
                        choices.append({
                            'x': x, 'y': y, 'delta': abs(elevation - self.matrix[y][x])
                        }) # add a dictionary of coordinate inforamtion to the choices list.
                min_delta = min([choice['delta'] for choice in choices]) # identify the minimum change of elevation from the last step to each of the potential steps
                # generate expression to look up the dictionary item in the list that matches the min_delta
                next_step = next((item for item in choices if item['delta'] == min_delta), None)
                # color the next_step
                self.image.putpixel((next_step["x"], next_step["y"]),(255, 153, 51, 255))
                # set the y coordinate for the next iteration
                y = next_step["y"]
        # save the map after interating and drawing all the path points.
        self.image.save(f'{filename}.png')

    
    def topo_map(self, filename):
        self.get_elevation_data()
        self.get_topo_data()
        self.get_unique_elevations()
        self.build_gradient()
        self.generate_image(filename)
        self.draw_path(filename, self.all_paths)

map = Map("elevation_large.txt")   
map.topo_map("map")

map = Map("elevation_large.txt", all_paths=True)   
map.topo_map("map_all_paths")






