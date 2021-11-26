import pytest 
import numpy as np
from solver import *
import time 

@pytest.fixture
def sample_puzzle_expert():
    return np.array([
[0, 0, 6, 0, 0, 0, 0, 0, 3],
[0, 0, 8, 0, 0, 0, 7, 5, 0],
[0, 5, 3, 4, 8, 0, 0, 0, 0],
[0, 0, 4, 0, 0, 9, 0, 0, 0],
[1, 0, 0, 0, 6, 7, 0, 0, 2],
[0, 6, 0, 0, 0, 0, 0, 8, 0],
[0, 3, 0, 2, 0, 0, 0, 4, 0],
[0, 4, 0, 1, 0, 0, 0, 0, 5],
[8, 0, 0, 0, 0, 5, 6, 0, 0]
])

@pytest.fixture
def sample_puzzle_medium():
    return np.array([
[6, 0, 0, 5, 0, 0, 9, 0, 0],
[8, 0, 1, 6, 0, 4, 2, 7, 0],
[0, 0, 0, 0, 7, 2, 6, 0, 0],
[0, 0, 0, 0, 8, 1, 7, 0, 4],
[0, 0, 4, 0, 3, 0, 1, 0, 0],
[0, 5, 0, 0, 0, 9, 0, 2, 3],
[4, 1, 5, 0, 0, 6, 0, 0, 0],
[7, 6, 3, 0, 0, 0, 4, 0, 0],
[0, 0, 0, 3, 4, 0, 5, 0, 6]
])

@pytest.fixture
def sample_puzzle_crooks():
    return np.array([
[2, 9, 5, 7, 0, 0, 8, 6, 0],
[0, 3, 1, 8, 6, 5, 0, 2, 0],
[8, 0, 6, 0, 0, 0, 0, 0, 0],
[0, 0, 7, 0, 5, 0, 0, 0, 6],
[0, 0, 0, 3, 8, 7, 0, 0, 0],
[5, 0, 0, 0, 1, 6, 7, 0, 0],
[0, 0, 0, 5, 0, 0, 1, 0, 9],
[0, 2, 0, 6, 0, 0, 3, 5, 0],
[0, 5, 4, 0, 0, 8, 6, 7, 2]
])


def check_complete(arr):
    """makes sure that answer is complete and valid"""
    assert len(np.argwhere(arr == 0)) == 0
    for i in range(9):
        for j in range(9):
            assert not rule_violation(arr, i, j)
    return True

def check_partial_complete(arr):
    """makes sure that puzzle is partially completed and is valid thus far"""
    non_empty = np.argwhere(arr > 0)
    assert len(non_empty) > 0
    for coord in non_empty:
        y,x = coord
        assert not rule_violation(arr, y, x)
    return True


def test_backtracking(sample_puzzle_expert, sample_puzzle_medium):
    expert = backtracking(sample_puzzle_expert)
    assert check_complete(expert)
    medium = backtracking(sample_puzzle_medium)
    assert check_complete(medium)

def test_cc_pf_hybrid_medium(sample_puzzle_medium):
    ans = cc_pf_hybrid(sample_puzzle_medium)
    assert check_complete(ans)

def test_cc_pf_hybrid_expert(sample_puzzle_expert):
    ans = cc_pf_hybrid(sample_puzzle_expert.copy())
    assert not np.array_equal(ans, sample_puzzle_expert)
    assert check_partial_complete(ans)
    ans = backtracking(ans.copy())
    assert check_complete(ans)


def test_solve_time_1(sample_puzzle_expert):
    #check that cc_pf_hybrid is faster than backtracking alone
    start = time.time()
    ans = cc_pf_hybrid(sample_puzzle_expert.copy())
    ans = backtracking(ans.copy())
    end = time.time()
    time_1 = end-start
    start = time.time()
    ans = backtracking(sample_puzzle_expert.copy())
    end = time.time()
    time_2 = end-start
    print(f'time 1: {time_1}')
    print(f'time_2: {time_2}')
    assert time_1 < time_2
    
#test to check mod crooks
def test_mod_crooks(sample_puzzle_expert):
    ans = mod_crooks_algorithm(sample_puzzle_expert.copy())
    assert check_complete(ans)

def test_solve_time_2(sample_puzzle_crooks):
    #check that cc_pf_hybrid is faster than backtracking alone
    start = time.time()
    ans = cc_pf_hybrid(sample_puzzle_crooks.copy())
    ans = backtracking(ans.copy())
    end = time.time()
    time_1 = end-start
    start = time.time()
    ans = mod_crooks_algorithm(sample_puzzle_crooks.copy())
    end = time.time()
    time_2 = end-start
    print(f'time 1: {time_1}')
    print(f'time_2: {time_2}')
    assert time_2 < time_1
