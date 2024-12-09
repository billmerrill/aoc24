import numpy as np
from collections import defaultdict

def possible_antinodes(ant_map):
    ants, counts = np.unique(ant_map, return_counts=True)
    ant_total = 0
    for i, ant in enumerate(ants):
        if ant != '.':
            ant_total += counts[i] * 2

    print(f'unbounded total {ant_total}')

def bounded_antinodes(ant_map):
    ants = defaultdict(list)
    with np.nditer(ant_map, flags=['multi_index']) as it:
        for x in it:
            if x.item() != '.':
                ants[x.item].append(it.multi_index)
    print(ants)

def main():
    src = 'sample.txt'
    src = 'input.txt'
    with open(src, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    ant_map = np.array([list(line) for line in lines])

    ants = defaultdict(list)
    with np.nditer(ant_map, flags=['multi_index']) as it:
        for x in it:
            if x.item() != '.':
                ants[x.item()].append(np.array(it.multi_index))

    #p1
    print(ants)
    antinodes = []
    for freq in ants:
        for i in ants[freq]:
            for j in ants[freq]:
                dist = i-j
                if not np.array_equal(i,j):
                    a = i+dist
                    if all(a >= 0) and all(a < ant_map.shape[0]) and (list(a) not in antinodes):
                        antinodes.append(list(a))

    print('p1')
    print(f'antinodes {antinodes}')
    print(len(antinodes))

    #p2
    print(ants)
    antinodes = []
    for freq in ants:
        if len(ants[freq]) > 1:
            for a in ants[freq]:
                antinodes.append(tuple(a))
    for freq in ants:
        for i in ants[freq]:
            for j in ants[freq]:
                if not np.array_equal(i,j):
                    dist = i-j
                    t = 1
                    while all(i+(dist*t) >=0) and all(i+(dist*t) < ant_map.shape[0]):
                        an = tuple(i+(dist*t))
                        if an not in antinodes:
                            antinodes.append(an)
                        t += 1
                    t = 1
                    while all(i-(dist*t) >=0) and all(i-(dist*t) < ant_map.shape[0]):
                        an = tuple(i-(dist*t))
                        if an not in antinodes:
                            antinodes.append(an)
                        t += 1
                            
    print('p2')
    print(f'anitnodes {antinodes}')
    print(len(antinodes))

    # possible_antinodes(ant_map)
    # bounded_antinodes(ant_map)


main()