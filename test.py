import pytest
from map.py import Map


@pytest.fixture()
def map():
    return Map('test_data.txt')

class testMap(self):

    def test_get_topo_data(self, map):
        for row in self.elevation_data:
            assert len(row) == len(matrix[0])
                



# https://stackoverflow.com/questions/50132703/pytest-fixture-for-a-class-through-self-not-as-method-argument
            

    

