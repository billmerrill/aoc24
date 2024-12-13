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
        self.notes[here]['root'] = root
        self.notes[here]['done'] = True
        for n in neighbors:
            look = (int(here[0]+n[0]), int(here[1]+n[1]))
            if 0 <= look[0] < self.garden.shape[0] and 0 <= look[1] < self.garden.shape[1] and not self.notes[look]['done']:
                if self.garden[here[0], here[1]].item() == self.garden[look[0], look[1]].item():
                    n_area, n_peri = self.walk_neighbors(look, root)
                    area += n_area
                    peri += n_peri
        return area, peri                

    def compute_areas(self):
        self.notes = {}
        self.areas = {}
        for i in range(self.garden.shape[0]):
            for j in range(self.garden.shape[1]):
                self.notes[(i,j)] = {'plant': self.garden[i,j].item(), 'root':None, 'done': False}
        
        for i in range(self.garden.shape[0]):
            for j in range(self.garden.shape[1]):
                if not self.notes[(i,j)]['done']:
                    here = (int(i), int(j))
                    self.areas[(i,j)] = self.walk_neighbors(here, here)

        # print(self.areas)

    def edge_filter(self, i,j,plant):
        filter = [[False]*3 for q in range(3)]
        for x_i, x in enumerate(range(i-1,i+2)):
            for y_i, y in enumerate(range(j-1,j+2)):
                if 0 <= x < self.garden.shape[0] and 0 <= y < self.garden.shape[1]:
                    filter[x_i][y_i] = (self.garden[x,y].item() == plant)
                else:
                    pass # it's not plant or oob.. false

        return filter

    def count_sides(self, i, j, f):
        # lhs
        sides = 0
        if (not f[0][1] and not f[1][0]) or \
            (f[0][0] and f[0][1] and not f[1][0]):
            sides += 1
            pass

        # top
        if (not (f[0][1] or f[1][0])) or \
            (f[0][0] and f[1][0] and not f[0][1]):
            sides += 1
            pass

        # rhs
        if (not(f[0][1] or f[1][2])) or \
            (f[0][2] and not f[1][2]):
            sides += 1
            pass

        # bottom
        if (not(f[1][0] or f[2][1])) or \
            (f[1][0] and f[2][0] and not f[2][1]):
            sides += 1
            pass
        return sides

    def compute_sides(self):
        for area_head in self.areas.keys():
            sides = 0
            print('computing sides for ', area_head, self.notes[area_head]['plant'])
            area_counter = self.areas[area_head][0]
            for i in range(self.garden.shape[0]):
                for j in range(self.garden.shape[1]):
                    it_root = self.notes[(i,j)]['root']
                    if it_root  == self.notes[area_head]['root']:
                        area_counter -= 1
                        filter = self.edge_filter(i,j,self.garden[i,j].item())
                        sides += self.count_sides(i,j,filter)
                        if area_counter < 0:
                            break

                if area_counter < 0:
                    break
            self.notes[area_head]['sides'] = sides
            print(area_head, sides)

    def compute_cost(self):
        cost = 0
        for p in self.areas:
            cost += self.areas[p][0] * self.areas[p][1]
        return cost

    def compute_bulk_cost(self):
        cost = 0
        for p in self.areas:
            cost += self.areas[p][0] * self.notes[p]['sides']
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
    n.compute_sides()
    print('cost: ', n.compute_cost())
    print('bulk cost: ', n.compute_bulk_cost())

main()