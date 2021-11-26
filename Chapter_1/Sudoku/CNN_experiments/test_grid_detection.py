import pytest 
from grid_detector import puzzle_parser

@pytest.fixture
def sample_img_1():
    return 'test_imgs/test_1.png'

@pytest.fixture
def sample_img_2():
    return 'test_imgs/test_2.png'

def test_grid_recognition(sample_img_1, sample_img_2):
    #just to test that the grid parser is working 
    for path in [sample_img_1, sample_img_2]:
        cells = puzzle_parser(path)
        assert len(cells) == 81



