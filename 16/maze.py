from collections import namedtuple
import networkx

# Node = namedtyple('Node', ['x', 'y', ])



class MazeSolver():

    def __init__(self):
        self.dir = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    def load(self, data):
        self.graph = networkx.DiGraph()
        self.start = -1
        self.end = -1

        # load nodes
        for i, row in enumerate(data):
            for j, tile in enumerate(row):
                if tile != '#':
                    if tile == 'S':
                        self.start = (i, j, 3) # start facing East
                    elif tile == 'E':
                        self.end = (i, j, 3)

                    for k in range(4):
                        self.graph.add_node((i,j,k))
        print(self.start, self.end)

        for x, y, facing in list(self.graph.nodes):
            dir_x, dir_y = self.dir[facing]
            next_x, next_y = x + dir_x, y + dir_y
            if (next_x, next_y, facing) in self.graph.nodes:
                self.graph.add_edge((x,y,facing), (next_x, next_y, facing), weight=1)
            for new_facing in range(4):
                facing_edge_weight = 1000
                # we don't need to count the last turn
                if (x,y) == (self.end[0], self.end[1]):
                    facing_edge_weight = 0
                self.graph.add_edge((x, y, facing), (x, y, new_facing), weight=facing_edge_weight)
    
    def part_one(self):
        cost = networkx.shortest_path_length(self.graph, self.start, self.end, weight='weight')
        print('cheapest solutoin', cost)

    def part_two(self):
        good_spots = set()
        for run in networkx.all_shortest_paths(self.graph, self.start, self.end, weight='weight'):
            for tile in run:
                good_spots.add((tile[0], tile[1]))
        print('num good seats', len(good_spots))

        

def main():
    src = "sample_2.txt"
    src = "input.txt"
    with open(src, 'r') as fh:
        data = fh.read().splitlines()

    m = MazeSolver()
    m.load(data)
    m.part_one()
    m.part_two()

main()
