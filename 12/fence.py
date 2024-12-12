import numpy as np 
from dataclasses import dataclass

@dataclass
class Neighbors:

    garden: np.array

    def __post_init__(self):
        pass


    def compute_edges(self):
        self.edges = np.zeros(self.garden.shape, dtype=int)
        neighbors = np.array([[-1,0],[0,1],[1,0],[0,-1]])
        with np.nditer(self.garden, flags=['multi_index']) as it:
            for x in it:
                edge_count = 0
                for n in neighbors:
                    look = it.multi_index + n
                    if 0 <= look[0] < self.garden.shape[0] and 0 <= look[1] < self.garden.shape[1]:
                        if self.garden[look[0],look[1]] != x.item():
                            self.edges[it.multi_index] += 1
                    else:
                        self.edges[it.multi_index] += 1

    def walk_neighbors(self, here, root):
        area = 1
        peri = int(self.edges[here[0], here[1]])
        neighbors = np.array([[-1,0],[0,1],[1,0],[0,-1]])
        here_key = f'{here[0],here[1]}' 
        self.notes[here_key]['root'] = root
        self.notes[here_key]['done'] = True
        for n in neighbors:
            look = (int(here[0]+n[0]), int(here[1]+n[1]))
            if 0 <= look[0] < self.garden.shape[0] and 0 <= look[1] < self.garden.shape[1] and not self.notes[f'{look[0],look[1]}']['done']:
                if self.garden[here[0], here[1]].item() == self.garden[look[0], look[1]].item():
                    n_area, n_peri = self.walk_neighbors(look, root)
                    area += n_area
                    peri += n_peri
        return area, peri                


    def walk_area(self, root):
        area = 1
        f
        area += walk_neigbors(root)


    def compute_areas(self):
        self.notes = {}
        self.areas = {}
        for i in range(self.garden.shape[0]):
            for j in range(self.garden.shape[1]):
                self.notes[f'{i,j}'] = {'plant': self.garden[i,j].item(), 'root':None, 'done': False}
        
        for i in range(self.garden.shape[0]):
            for j in range(self.garden.shape[1]):
                if not self.notes[f'{i,j}']['done']:
                    here = [int(i), int(j)]
                    self.areas[f'{i,j}'] = self.walk_neighbors(here, here)

        # print(self.areas)

    def compute_cost(self):
        cost = 0
        for p in self.areas:
            cost += self.areas[p][0] * self.areas[p][1]
        return cost


def main():
    src = 'sample3.txt'
    src = 'input.txt'
    with open(src, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    garden = np.array([list(line) for line in lines])
    n = Neighbors(garden)
    n.compute_edges()
    n.compute_areas()
    print('cost: ', n.compute_cost())

main()