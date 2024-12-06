import numpy as np
from copy import copy

dirs = ['^', '>', 'V', '<']
src = 'buf_input.txt'
# src = 'buf_sample.txt'
with open(src, 'r') as f:
    lines = [line.strip() for line in f.readlines()]
room = np.array([list(line) for line in lines])

print(np.matrix(room))

cur = None
with np.nditer(room, flags=['multi_index']) as it:
    for x in it:
        if x in ['^', '>', 'v', '<']:
            cur = np.array(it.multi_index)
            break

next = cur
while room[cur[0], cur[1]] != "Q":
    print(cur)
    next = copy(cur)
    if room[cur[0],cur[1]] == '^':
        next[0] -= 1
    elif room[cur[0],cur[1]] == '>':
        next[1] += 1
    elif room[cur[0],cur[1]] == 'V':
        next[0] += 1
    elif room[cur[0],cur[1]] == '<':
        next[1] -= 1
    
    if room[next[0], next[1]] == 'Q':
        break
    
    if room[next[0], next[1]] == '#':
        room[cur[0], cur[1]] = dirs[(dirs.index(room[cur[0], cur[1]])+1) % len(dirs)]
        continue





    room[next[0],next[1]] = room[cur[0], cur[1]]
    room[cur[0],cur[1]] = 'B'
    cur = copy(next)


steps = 1
with np.nditer(room, flags=['multi_index']) as it:
    for x in it:
        # if x in ['^', '>', 'v', '<']:
        if x == 'B':
            steps += 1

print(np.matrix(room))
print(steps)

