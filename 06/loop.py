import numpy as np
from copy import copy

dirs = ['^', '>', 'V', '<']



def pstr(p):
    return f'{p[0],p[1]}'

def is_repeating(path):
    post_val = path[-1]
    for i in range(len(path)-2, 0, -1):
        if path[i] == post_val:
            end_str = path[i+1:]
            next_str = path[i-(len(end_str)-1):i+1]
            if np.array_equal(end_str, next_str):
                return True

    return False

def new_walk(room, origin):
    global dirs
    path = [pstr(origin)]
    start_pos = copy(origin)
    start_dir = room[start_pos[0], start_pos[1]]

    here = copy(start_pos)
    next = [-1, -1]
    while room[here[0], here[1]] != 'Q':
        facing = room[here[0], here[1]]
        if facing == '^':
            next = [here[0]-1, here[1]]
        elif facing == '>':
            next = [here[0], here[1]+1]
        elif facing == 'V':
            next = [here[0]+1, here[1]]
        elif facing == '<':
            next = [here[0], here[1]-1]

        next_info = room[next[0], next[1]]
        # if np.array_equal(next, start_pos) and facing == start_dir:
        #     return 'looped'
        if next_info == 'Q':
            return 'exited'
        elif next_info == '#':
            room[here[0], here[1]] = dirs[(dirs.index(room[here[0], here[1]])+1) % len(dirs)]
            continue

        room[next[0],next[1]] = room[here[0], here[1]]

        here[0] = next[0]
        here[1] = next[1]
        path.append(pstr(here))
        if len(path) % 10000 == 1:
            if is_repeating(path):
                return 'looped'

def main():
    src = 'buf_input.txt'
    # src = 'buf_sample.txt'
    with open(src, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    room = np.array([list(line) for line in lines])
    og_room = copy(room)

    start_pos = None
    with np.nditer(room, flags=['multi_index']) as it:
        for x in it:
            if x in ['^', '>', 'v', '<']:
                start_pos = np.array(it.multi_index)
                break

    num_loops = 0
    with np.nditer(room, flags=['multi_index']) as it:
        for x in it:
            room = copy(og_room)
            test_pos = np.array(it.multi_index)
            if room[test_pos[0], test_pos[1]] == 'Q':
                continue
            if np.array_equal(test_pos, start_pos):
                continue

            room[test_pos[0], test_pos[1]] = '#'

            # result = walk(room, start_pos)
            result = new_walk(room, start_pos)
            if test_pos[1] == 1:
                print(f'{test_pos}: {num_loops}')
            if result == 'looped':
                num_loops += 1

    print(f'num_loops {num_loops}')

main()
