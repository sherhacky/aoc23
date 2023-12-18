import networkx as nx


with open('./input17.txt') as f:
    data = f.read()

# data = '''2413432311323
# 3215453535623
# 3255245654254
# 3446585845452
# 4546657867536
# 1438598798454
# 4457876987766
# 3637877979653
# 4654967986887
# 4564679986453
# 1224686865563
# 2546548887735
# 4322674655533
# '''

# data = '''111111111111
# 999999999991
# 999999999991
# 999999999991
# 999999999991
# '''

lines = data.split('\n')[:-1]

grid = [[int(char) for char in line] for line in lines]
m, n = len(grid), len(grid[0])
# idea:
# product of grid with possible configurations of steps 
# leading up to that point
# eg '>2', '>1', '>0'
# the weight of an edge is the number in the target node

direction = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}

def next_options(d, s):
    result = []
    nd = '^v' if d in '<>' else '<>'
    for c in nd:
        result.append((c, 2))
    if s > 0:
        result.append((d, s-1))
    return result

G = nx.DiGraph()

G.add_edge((0, 0), ((0, 1), '>', 2), weight=grid[0][1])
G.add_edge((0, 0), ((1, 0), 'v', 2), weight=grid[1][0])
for i in range(m):
    for j in range(n):
        for c in '^v<>':
            for s in range(3):
                for d, t in next_options(c, s):
                    d_i, d_j = direction[d]
                    if 0 <= i + d_i < m and 0 <= j + d_j < n:
                        G.add_edge(
                            ((i, j), c, s), 
                            ((i+d_i, j+d_j), d, t),
                             weight=grid[i+d_i][j+d_j]
                        )

for s in range(0, 3):
    for char in '>v':
        G.add_edge(((m-1, n-1), char, s), (m-1, n-1), weight=0)

path = nx.shortest_path(G, (0,0), (m-1,n-1), weight="weight")

# for p in path:
#     print(p)

print(sum(
    grid[u[0][0]][u[0][1]] for u in path[1:-1]
))


# part 2

def ultra_next_options(d, s):
    result = []
    nd = '^v' if (
        d in '<>' and s in range(7)
    ) else '<>' if (
        d in '^v' and s in range(7)
    ) else ''
    for c in nd:
        result.append((c, 9))
    if s > 0:
        result.append((d, s-1))
    return result


G = nx.DiGraph()


G.add_edge((0, 0), ((0, 1), '>', 9), weight=grid[0][1])
G.add_edge((0, 0), ((1, 0), 'v', 9), weight=grid[1][0])
for i in range(m):
    for j in range(n):
        for c in '^v<>':
            for s in range(10):
                for d, t in ultra_next_options(c, s):
                    d_i, d_j = direction[d]
                    if 0 <= i + d_i < m and 0 <= j + d_j < n:
                        G.add_edge(
                            ((i, j), c, s),
                            ((i+d_i, j+d_j), d, t),
                            weight=grid[i+d_i][j+d_j]
                        )

for s in range(7):
    for char in '>v':
        G.add_edge(((m-1, n-1), char, s), (m-1, n-1), weight=0)

ultra_path = nx.shortest_path(G, (0, 0), (m-1, n-1), weight="weight")

# for p in ultra_path:
#     print(p)

print(sum(
    grid[u[0][0]][u[0][1]] for u in ultra_path[1:-1]
))
