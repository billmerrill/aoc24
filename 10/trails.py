import numpy as np
import copy


def find_trailheads(dem):
    ths = []
    with np.nditer(dem, flags=['multi_index']) as it:
        for x in it:
            if x == 0:
                ths.append(it.multi_index)
    
    return ths

def wander(p, past, dem, nines):
    cur = dem[p[0], p[1]]
    if cur == 9:
        if p not in nines:
            nines.append(p)
        return nines

    score = 0
    children = [(p[0]+1,p[1]),(p[0],p[1]-1),(p[0]-1,p[1]),(p[0],p[1]+1)]
    for c in children:
        # if c[0] == past[0] and c[1] == past[1]:
        #     continue
        if 0 <= c[0] < dem.shape[0] and 0 <= c[1] < dem.shape[1]:
            if dem[c[0], c[1]] == (cur + 1):
                nines = wander(c, p, dem, nines)
            else:
                pass
    return nines

def wrating(p,dem):
    cur = dem[p[0], p[1]]
    if cur == 9:
        return 1
    
    score = 0
    children = [(p[0]+1,p[1]),(p[0],p[1]-1),(p[0]-1,p[1]),(p[0],p[1]+1)]
    for c in children:
        if 0 <= c[0] < dem.shape[0] and 0 <= c[1] < dem.shape[1]:
            if dem[c[0], c[1]] == (cur + 1):
                score += wrating(c, dem)
    return score


def score_trailheads(ths, dem):
    scores = []
    ratings = []
    nines = []
    for th in ths:
        nines = []
        scores.append(len(wander(th, (-1, -1), dem, nines)))
        ratings.append(wrating(th, dem))
    return scores, ratings

def main():
    src = 'sample.txt'
    src = 'input.txt'
    with open(src, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    dem = np.array([list(map(int,list(line))) for line in lines])
    print(f'shape {dem.shape}')
    print(dem)
    trailheads = find_trailheads(dem)
    scores, ratings = score_trailheads(trailheads, dem)
    print(f'scores {scores}')
    print(sum(scores))
    print(f'ratings {ratings}')
    print(sum(ratings))

main()