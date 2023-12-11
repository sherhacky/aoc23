import networkx as nx

with open('./input10.txt') as f:
    data = f.read()

lines = data.split('\n')[:-1]

connections = {
    '|': {(-1, 0), (1, 0)},
    '-': {(0, -1), (0, 1)},
    'L': {(-1, 0), (0, 1)},
    'J': {(-1, 0), (0, -1)},
    '7': {(0, -1), (1, 0)},
    'F': {(0, 1), (1, 0)},
    'S': {(-1, 0), (1, 0), (0, -1), (0, 1)},
    '.': set()
}

dir_edges = set()
for i in range(len(lines)):
    for j in range(len(lines[0])):
        for a, b in connections[lines[i][j]]:
            dir_edges.add(((i, j), (i+a, j+b)))
        if lines[i][j] == 'S':
            start = (i, j)

edges = {E for E in dir_edges if (E[1], E[0]) in dir_edges}

G = nx.Graph()
for E in edges:
    G.add_edge(E[0], E[1])

shortest_paths = nx.shortest_path(G, source=start)
print(max(len(path) for path in shortest_paths.values()) - 1)

expanded_grid = [
    [
        '.' for j in range(2*len(lines[0]) - 1)
    ] for i in range(2*len(lines) - 1)
]

loop_nodes = set([u for path in shortest_paths.values() for u in path])

for u, v in edges:
    if u in loop_nodes and v in loop_nodes:
        d_i = v[0] - u[0]
        d_j = v[1] - u[1]
        for (i, j) in {
            (2*u[0], 2*u[1]),
            (2*u[0] + d_i, 2*u[1] + d_j),
            (2*v[0], 2*v[1]),
        }:
            expanded_grid[i][j] = 'X'

outside_current = set()

for i in range(len(expanded_grid)):
    for j in range(len(expanded_grid[0])):
        if expanded_grid[i][j] == '.' and (
            i in (0, len(expanded_grid) - 1) or
            j in (0, len(expanded_grid[0]) - 1)
        ):
            outside_current.add((i, j))

while any(outside_current):
    for (i, j) in outside_current:
        expanded_grid[i][j] = 'O'
    outside_next = {
        (i + a, j + b) for (i, j) in outside_current
        for (a, b) in [(0, 1), (-1, 0), (1, 0), (0, -1)]
        if 0 <= i+a < len(expanded_grid)
        and 0 <= j+b < len(expanded_grid[0])
        and expanded_grid[i+a][j+b] == '.'
    }
    outside_current = set(outside_next)

result = sum(
    [1
    for i in range(len(expanded_grid))
    for j in range(len(expanded_grid[0]))
    if i % 2 == 0 and j % 2 == 0 and expanded_grid[i][j] == '.']
)

print(result)
