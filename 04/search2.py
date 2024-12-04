import numpy as np
from collections import defaultdict

xmas = ['X', 'M', 'A', 'S']
mas = ['M', 'A', 'S']
clock = defaultdict(int)
ex_mas = np.array([
    ['M', '.', 'S'],
    ['.', 'A', '.'],
    ['M', '.', 'S']])

def count_ex_mas(puzzle, oh):
    global ex_mas
    print(f'oh {oh}')
    ps1 = [puzzle[oh[0]-1, oh[1]-1], 
                puzzle[oh[0], oh[1]], 
                puzzle[oh[0]+1, oh[1]+1]]
    ps2 = [puzzle[oh[0]+1, oh[1]-1], 
                puzzle[oh[0], oh[1]], 
                puzzle[oh[0]-1, oh[1]+1]]
    # print(ps1, ps2)
    found = 0
    for t in range(0,4):
        f1 = [ex_mas[0,0], ex_mas[1,1], ex_mas[2,2]]
        f2 = [ex_mas[2,0], ex_mas[1,1], ex_mas[0,2]]

        if np.array_equal(ps1,f1) and np.array_equal(ps2, f2):
            found += 1
        ex_mas = np.rot90(ex_mas)

    return found

with open('buf_input.txt', 'r') as f:
# with open('buf_test_input.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
puzzle = np.array([list(line) for line in lines])
print(f'shape {puzzle.shape}')

exes = []
visits = 0
with np.nditer(puzzle, flags=['multi_index']) as it:
    for x in it:
        visits += 1
        if x == 'A':
            exes.append(it.multi_index)
found = 0
for ex in exes:
    found += count_ex_mas(puzzle, np.array(ex))

print(f'final found {found}')
print(clock)