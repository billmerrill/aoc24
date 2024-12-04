import numpy as np
from collections import defaultdict

xmas = ['X', 'M', 'A', 'S']
clock = defaultdict(int)

def count_xmas(puzzle, oh):
    r"""
        \ | /
        - x -
        / | \
    """
    found = 0
    print(oh)
    # 3
    try:
        if oh[1] < puzzle.shape[1]-3:
            if np.array_equal(puzzle[oh[0], oh[1]+1:oh[1]+4], xmas[1:]):
                found += 1
                clock['3'] += 1
                print('3')
    except IndexError:
        pass

    # 4:30
    try:
        if oh[0] < puzzle.shape[0]-3 and oh[1] < puzzle.shape[1]-3:
            test_str = [puzzle[oh[0]+1, oh[1]+1], 
                        puzzle[oh[0]+2, oh[1]+2], 
                        puzzle[oh[0]+3, oh[1]+3]]
            if np.array_equal(test_str, xmas[1:]):
                found += 1
                clock['4.5'] += 1
                print('4.5')
    except IndexError:
        pass

    # 6
    try:
        if oh[0] < puzzle.shape[0]-3:
            if np.array_equal(puzzle[oh[0]+1:oh[0]+4, oh[1]], xmas[1:]):
                found += 1
                clock['6'] += 1
                print('6')
    except IndexError:
        pass

    # 7:30
    try: 
        if oh[0] < puzzle.shape[0]-3 and oh[1] >= 3:
            test_str = [puzzle[oh[0]+1, oh[1]-1], 
                        puzzle[oh[0]+2, oh[1]-2], 
                        puzzle[oh[0]+3, oh[1]-3]]
            if np.array_equal(test_str, xmas[1:]):
                found += 1
                clock['7.5'] += 1
                print('7.5')
    except IndexError:
        pass

    # 9
    try:
        if oh[1] >= 3:
            test_str = np.flip(puzzle[oh[0], oh[1]-3:oh[1]])
            if np.array_equal(test_str, xmas[1:]):
                found += 1
                clock['9'] += 1
                print('9')
    except IndexError:
        pass

    # 10:30
    try:
        if oh[0] >= 3 and oh[1] >= 3:
            test_str = [puzzle[oh[0]-1, oh[1]-1], 
                        puzzle[oh[0]-2, oh[1]-2], 
                        puzzle[oh[0]-3, oh[1]-3]]
            if np.array_equal(test_str, xmas[1:]):
                found += 1
                clock['10.5'] += 1
                print('10.5')
    except IndexError:
        pass

    # 12
    try:
        if oh[1] >= 3:
            if np.array_equal(
                    np.flip(puzzle[oh[0]-3:oh[0], oh[1]]), 
                            xmas[1:]):
                found += 1
                clock['12'] += 1
                print('12')
    except IndexError:
        pass

    # 1:30
    try: 
        if oh[0] >= 3 and oh[1] < puzzle.shape[1] - 3:
            test_str = [puzzle[oh[0]-1, oh[1]+1], 
                        puzzle[oh[0]-2, oh[1]+2], 
                        puzzle[oh[0]-3, oh[1]+3]]
            if np.array_equal(test_str, xmas[1:]):
                found += 1
                clock['1.5'] += 1
                print('1.5')
    except IndexError:
        pass
   
    return found


with open('input.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
puzzle = np.array([list(line) for line in lines])

exes = []
with np.nditer(puzzle, flags=['multi_index']) as it:
    for x in it:
        if x == 'X':
            exes.append(it.multi_index)
found = 0
for ex in exes:
    found += count_xmas(puzzle, np.array(ex))

print(f'final found {found}')
print(clock)