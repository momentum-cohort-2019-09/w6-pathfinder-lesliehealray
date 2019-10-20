import pytest
from PIL import Image, ImageChops
from map import Map


@pytest.fixture()
def map():
    map = Map('test_data.txt')
    map.topo_map('test_image')
    return map

class TestMap:

    def test_get_topo_data(self, map):
        """
        map.get_topo_data returns a list of list that 
        contain elevations for which we can impute x, y coordinates
        """
        assert map.matrix[0][0] == 1000
        assert map.matrix[2][4] == 5002
                
    def test_get_unique_elevation(self, map):
        assert len(map.unique_elevations) == 13

    def test_build_gradient(self, map):
        brightness = (2000 - 1000) / (5002 - 1000)
        greyscale = int(255 * brightness)
        color = (greyscale, greyscale, greyscale, 255)
        assert map.gradient[2000] == color
    
    def test_generate_image(self):  
        map = Map('test_data.txt')
        map.topo_map('test_image2')
        fixture_image = Image.open('test_image.png')
        generated_image = Image.open('test_image2.png')
        diff = ImageChops.difference(fixture_image, generated_image)
        assert diff.getbbox() is None



# SOME RESOURCES USED:
# https://stackoverflow.com/questions/50132703/pytest-fixture-for-a-class-through-self-not-as-method-argument
# effbot.org/zone/pil-comparing-images.htm
# https://pytest-cov.readthedocs.io/en/latest/readme.html#installation
# pip3 install pytest-cov and run pytest --cov=map test.py           
# dbader.org/blog/python-generator
    

