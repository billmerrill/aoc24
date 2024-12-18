import networkx

settings = [
    {'limit':12, 'file': 'sample.txt', 'size':7},
    {'limit':1024, 'file': 'input.txt', 'size':71}]
s = settings[1]
with open(s['file'], 'r') as fh:
    data = fh.read().splitlines()

# data = [tuple(x.split('x')) for x in data_str]

dir = [(-1, 0), (0, -1), (1, 0), (0, 1)]
unsafe = []
for i in range(s['limit']):
    c = data[i].split(',')
    unsafe.append((int(c[1]), int(c[0])))

start = (0,0)
end = (s['size']-1, s['size']-1)
safe = (s['size'], s['size'])
graph = networkx.DiGraph()

for i in range(s['size']):
    for j in range(s['size']):
        if (i,j) not in unsafe:
            graph.add_node((i,j))

for x, y in list(graph.nodes):
    for d in dir:
        next_x, next_y = x+d[0], y+d[1]
        if (next_x, next_y) in graph.nodes and \
            (next_x, next_y) not in unsafe:
            graph.add_edge((x,y), (next_x, next_y), weight=1)

print(networkx.shortest_path_length(graph, start, end, weight=1))





