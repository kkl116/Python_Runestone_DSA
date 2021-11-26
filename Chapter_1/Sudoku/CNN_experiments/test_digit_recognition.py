import pytest 
import numpy as np
from digit_recognition import predict
from grid_detector import puzzle_parser

@pytest.fixture
def sample_img_1():
    path = 'test_imgs/test_1.png'
    cells = puzzle_parser(path)
    ans = np.array([
        [0, 0, 0, 0, 0, 4, 8, 0, 0],
        [0, 0, 3, 2, 8, 0, 0, 0, 5],
        [0, 2, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 0, 7, 0],
        [0, 3, 0, 9, 1, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 9, 0, 8, 3, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 4, 0, 0, 0, 0]
    ])
    return cells, ans

@pytest.fixture
def sample_img_2():
    path = 'test_imgs/test_2.png'
    cells = puzzle_parser(path)
    ans = np.array([
        [0, 1, 3, 5, 2, 0, 4, 2, 0],
        [0, 8, 7, 0, 0, 4, 0, 0, 0],
        [0, 0, 4, 0, 7, 9, 6, 0, 3],
        [0, 6, 2, 0, 4, 0, 5, 0, 8],
        [0, 0, 0, 0, 5, 0, 1, 0, 2],
        [0, 3, 8, 0, 9, 1, 0, 0, 0],
        [0, 0, 0, 9, 0, 0, 8, 0, 0],
        [7, 0, 0, 8, 1, 5, 0, 0, 9],
        [8, 9, 1, 0, 0, 7, 2, 5, 0]
    ])
    return cells, ans

def test_1(sample_img_1):
    cells, ans = sample_img_1
    digits = predict(cells)
    assert np.array_equal(digits, ans)
    return True

def test_2(sample_img_2):
    cells, ans = sample_img_2
    digits = predict(cells)
    print(digits)
    assert np.array_equal(digits, ans)
    return True


if __name__ == '__main__':
    pytest.main()