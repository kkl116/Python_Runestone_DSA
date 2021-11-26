#Sudoku solver
"""
Module that contains implementations of different methods to solve a sudoku puzzle
"""
import numpy as np 

def get_n_subgrid_starting_coords(n):
    start_y = (n // 3) * 3
    start_x = (n % 3) * 3
    return start_y, start_x

def get_coord_subgrid_starting_point(y, x):
    x_q, y_q = max(0, x//3)*3, max(0, y//3)*3
    return y_q, x_q

def axis_check(arr, y, x, axis='x'):
    assert axis in ['x', 'y']
    current_val = arr[(y,x)]
    assert current_val != 0
    if axis == 'x':
        ax = arr[y, :].copy()
        ax[x] = -1
    elif axis == 'y':
        ax = arr[:, x].copy()
        ax[y] = -1
    assert len(ax) == 9
    return current_val in ax

def subgrid_check(arr, y, x):
    current_val = arr[(y,x)]
    #identify which quadrant current chords is in 
    y_q, x_q = get_coord_subgrid_starting_point(y, x)
    local = arr[y_q:y_q+3, x_q:x_q+3].copy()
    assert local.shape == (3,3)
    local[y%3, x%3] = -1
    return current_val in local

def rule_violation(arr, y, x):
    row = axis_check(arr, y, x, axis='x')
    col = axis_check(arr, y, x, axis='y')
    subgrid = subgrid_check(arr, y, x)
    if any([row, col, subgrid]):
        return True
    else:
        return False

def backtracking(arr, markings=None):
    empty_coords = np.argwhere(arr == 0)
    i = 0        
    while i < len(empty_coords):
        #run down the list of coords
        y,x = empty_coords[i, :]

        #normal brute force when no markings are provided
        if markings is None:
            if arr[y,x] == 9:
                #this deals with situation where after rolling back the val is 9 so should reset and roll back another val
                arr[y,x] = 0 
                i -= 1
                continue
            else:
                arr[y,x] += 1
        
        if markings is not None:
        #if have markings then use them! - cycle through the markings list instead of +1 everytime
            cell_markings = markings[(y,x)]
            curr_val = arr[y,x]
            if curr_val == cell_markings[-1]:
                arr[y,x] = 0
                i -= 1
                continue
            else:
                if arr[y,x] == 0:
                    curr_idx = 0
                else:
                    curr_idx = cell_markings.index(curr_val) + 1
                arr[y,x] = cell_markings[curr_idx]


        assert arr[y,x] <= 9
        #add one to current value
        if rule_violation(arr, y, x):
            #if current number violates a rule 
            if arr[y,x] == 0:
                if i == 0:
                    print('This sudoku does not have a valid solution.')
                    return
            #if current == 9
            #return to the previos cell and reset number -
                arr[y,x] = 0
                i -= 1
        else:
            i += 1
    return arr

def candidate_checking(arr):
    empty_coords = np.argwhere(arr == 0)
    while True:
        n_empty = len(empty_coords)
        del_idx = []
        for idx, coords in enumerate(empty_coords):
            #for each spot, check to see if a particular number satisfies conditions
            y,x = coords
            cands = []
            for n in range(1, 10):
                arr[y,x] = n
                if not rule_violation(arr, y, x):
                    cands.append(n)

            if len(cands) == 1:
                #if only one valid candidate
                arr[y,x] = cands[0]
                del_idx.append(idx)
            else:
                arr[y,x] = 0
        
        empty_coords = np.delete(empty_coords, del_idx, axis=0)
        if len(empty_coords) == n_empty:
            #if no coords have been removed this cycle 
            return arr

def axis_find(arr, n=None, val=None, axis='x'):
    empty_coords = np.argwhere(arr == 0)
    assert n in range(9)
    assert axis in ['x', 'y']
    cands = []
    if axis == 'x':
        ax_idx = 0
    elif axis == 'y':
        ax_idx = 1
    #in empty coords find empty cells in this row/col
    coords = [(idx,c) for idx,c in enumerate(empty_coords) if c[ax_idx] == n]
    if len(coords) == 0:
        #no empty cells in corresponding row or col - return empty cands
        return cands
    for c in coords:
        y,x = c[1]
        arr[y,x] = val 
        if not rule_violation(arr, y, x):
            cands.append(c)
        #reset val back to original
        arr[y,x] = 0
    return cands

def subgrid_find(arr, n=None, val=None):
    empty_coords = np.argwhere(arr == 0)
    assert n in range(9)
    #identify which subgrid we're working with 
    cands = []
    start_y, start_x = get_n_subgrid_starting_coords(n)
    subgrid_y_range = range(start_y, start_y+3)
    subgrid_x_range = range(start_x, start_x+3)

    coords = [(idx,c) for idx,c in enumerate(empty_coords) 
            if c[0] in subgrid_y_range
            and c[1] in subgrid_x_range]

    if len(coords) == 0:
        return cands

    for c in coords:
        y,x = c[1]
        arr[y,x] = val
        if not rule_violation(arr, y, x):
            cands.append(c)
        arr[y,x] = 0
    return cands

def process_cands(cands, arr, del_idx, val):
    if len(cands) == 1:
        y,x = cands[0][1]
        arr[y,x] = val
        del_idx.append(cands[0][0])
    else:
        pass

def place_finding(arr):
    empty_coords = np.argwhere(arr == 0)
    while True:
        n_empty = len(empty_coords)
        del_idx = []
        #loops have to be in order - elimination cannot happen concurrently
        for n in range(9):
            for val in range(1, 10):
                row_cands = axis_find(arr, n=n, val=val, axis='x')
                process_cands(row_cands, arr, del_idx, val)
        
        for n in range(9):
            for val in range(1, 10):
                col_cands = axis_find(arr, n=n, val=val, axis='y')
                process_cands(col_cands, arr, del_idx, val)

        for n in range(9):
            for val in range(1, 10):
                subgrid_cands = subgrid_find(arr, n=n, val=val)
                process_cands(subgrid_cands, arr, del_idx, val)

        empty_coords = np.delete(empty_coords, del_idx, axis=0)
        if n_empty == len(empty_coords):
            return arr


def cc_pf_hybrid(arr):
    assert arr.shape == (9,9)
    it = 0
    while len(np.argwhere(arr == 0)) > 0:
        starting_arr = arr.copy()
        arr = place_finding(arr)
        arr = candidate_checking(arr)
        if np.array_equal(starting_arr, arr):
            return arr
    return arr


#Crooks algorithm
def generate_markings(arr):
    markings = {}
    empty_coords = np.argwhere(arr == 0)
    for coord in empty_coords:
        y, x = coord
        curr_markings = []
        for val in range(1, 10):
            arr[y, x] = val
            if not rule_violation(arr, y, x):
                curr_markings.append(val)
            arr[y, x] = 0
        if curr_markings:
            markings.update({(y,x): curr_markings})
    return markings

def get_set_string(current_set):
    return ''.join(list([str(i) for i in current_set]))

def get_n_preemptive_sets(n_markings):
    preemptive_sets = {}
    for marking in n_markings:
        #len(m) should be bigger than 1 always b/c those should be completed by cc_pf
        #but also cannot exceed 9!
        marks = marking[1]
        for n in range(2, len(marks)+1):
            current_set = set(marks[:n])
            #check if current set is exists in other cells 
            if get_set_string(current_set) in preemptive_sets:
                continue

            supersets = [marking[0] for marking in n_markings if set(marking[1]) == current_set]
            if len(supersets) == n:
                #if supersets i.e. cells that contain this subset of markings == length of current_markings
                #turn current_set into a string 
                curr_set_string = get_set_string(current_set)
                preemptive_sets.update({curr_set_string: supersets})
    return preemptive_sets

def find_preemptive_sets(markings, n=None, mode=None):
    #try to create a recursive function so that preemptive sets can keep getting narrowed down?
    assert mode in ['row', 'col', 'subgrid']
    #first identify cells that are within nth row, col or subgrid 
    if mode == 'row':
        n_markings = [(key, val) for key, val in markings.items() if key[0] == n]
    elif mode == 'col':
        n_markings = [(key, val) for key, val in markings.items() if key[1] == n]
    elif mode == 'subgrid':
        start_y, start_x = get_n_subgrid_starting_coords(n)
        subgrid_y_range = range(start_y, start_y+3) 
        subgrid_x_range = range(start_x, start_x+3)
        n_markings = [(key, val) for key, val in markings.items() if 
        key[0] in subgrid_y_range
        and key[1] in subgrid_x_range]
    #find preemptive sets within n_markings
    #find all numbers that has freq > 1, then 
    #check all sets to see if it's preemptive?
    preemptive_sets = get_n_preemptive_sets(n_markings)
    #return markings - if any markings contain single num, return that as separate list
    return preemptive_sets

def process_preemptive_sets(markings, preemptive_sets, mode=None):
    assert mode in ['row', 'col', 'subgrid']
    """changes markings given preemptive sets that have been found"""
    for set_string, cells in preemptive_sets.items():
        set_ = [int(char) for char in set_string]
        for cell in cells:
            #find corresponding row, col, subgrid, and remove set_ vals from those markings
            p_y, p_x = cell

            for coords, m in markings.items():
                y, x = coords
                if mode == 'row':
                    change = y == p_y
                elif mode == 'col':
                    change = x == p_x
                elif mode == 'subgrid':
                    subgrid_start_y, subgrid_start_x = get_coord_subgrid_starting_point(p_y, p_x)
                    subgrid_y_range = range(subgrid_start_y, subgrid_start_y+3)
                    subgrid_x_range = range(subgrid_start_x, subgrid_start_x+3)
                    change = (y in subgrid_y_range and x in subgrid_x_range)

                if change:
                    new_m = [val for val in m if val not in set_]
                    #make sure 
                    if len(new_m) > 0:
                        #if new_m == 0 it means those are the cells in the preemptive set
                        markings.update({coords: new_m})
    return markings

def update_array_singletons(arr, markings):
    del_coords = []
    for coord, marks in markings.items():
        if len(marks) == 1:
            y, x = coord
            arr[y,x] = marks[0]
            assert not rule_violation(arr, y, x)
            #delete from markings
            del_coords.append(coord)
    for coord in del_coords:
        markings.pop(coord)
    return arr, markings


def check_partial_complete(arr):
    """makes sure that puzzle is partially completed and is valid thus far"""
    non_empty = np.argwhere(arr > 0)
    violations = []
    assert len(non_empty) > 0
    for coord in non_empty:
        y,x = coord
        if rule_violation(arr, y, x):
            violations.append(coord)
    return not violations

def mod_crooks_algorithm(arr):
    """general idea - 
    1. generate markings for the array
    2. complete empty cells where single candidates can be filled in 
    3. use occupancy theorem to eliminate possible candidates
    4. provide possible candidates for backtracking algorithm for solving"""
    markings = generate_markings(arr)
    arr, markings = update_array_singletons(arr, markings)
    assert check_partial_complete(arr)
    i = 0
    while True:
        init_markings = markings.copy()
        #generate markings for the array
        for mode in ['row', 'col', 'subgrid']:
            for n in range(9):
                preemptive_sets = find_preemptive_sets(markings, n=n, mode=mode)
                #when processing preemptive set it also depends on the mode!
                markings = process_preemptive_sets(markings, preemptive_sets, mode=mode)
                arr, markings = update_array_singletons(arr, markings)
        i += 1
        if markings == init_markings:
            #if there are no further changes to markings then break
            break
    ans = backtracking(arr, markings=markings)
    return ans


def solve_sudoku(arr, method=None):
    arr = arr.copy()
    assert method in [1, 2, 3]
    #expect np array
    assert arr.shape == (9,9)
    if method == 1:
        #Brute force - backtracking method - https://pi.math.cornell.edu/~mec/Summer2009/meerkamp/Site/Solving_any_Sudoku_I.html
        ans = backtracking(arr)
    elif method == 2:
        #hybrid method using simple strategies - place finding and candidate checking - https://pi.math.cornell.edu/~mec/Summer2009/meerkamp/Site/Solving_any_Sudoku_I.html
        #if puzzle cannot be finished then uses backtracking to finish the rest
        ans = cc_pf_hybrid(arr)
        if len(np.argwhere(ans == 0)) > 0:
            ans = backtracking(arr)
    elif method == 3:
        #crook's algorithm
        ans = mod_crooks_algorithm(arr)
    return ans



