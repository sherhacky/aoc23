from collections import defaultdict
with open('./input16.txt') as f:
    line = f.readline()
    grid = []
    while line:
        # print('a line')
        # print(line)
        # grid.append(repr(line)[1:-3])
        grid.append(r"{}".format(line[:-1]))
        # print(grid[-1])
        line = f.readline()

# grid.pop(-1)
# for l in grid:
#     print(l, len(l))
m, n = len(grid), len(grid[0])
print(m,n)
beam_map = {(i,j): set() for i in range(m) for j in range(n)}

beam_map[(0,0)].add('>')

direction = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}

paths = {
    '>': {
        '|': ['^', 'v'],
        '-': ['>'],
        '/': ['^'],
        '\\': ['v'],
        '.': ['>'],
    },
    '<': {
        '|': ['^', 'v'],
        '-': ['<'],
        '/': ['v'],
        '\\': ['^'],
        '.': ['<'],
    },
    'v': {
        '|': ['v'],
        '-': ['<', '>'],
        '/': ['<'],
        '\\': ['>'],
        '.': ['v'],
    },
    '^': {
        '|': ['^'],
        '-': ['<', '>'],
        '/': ['>'],
        '\\': ['<'],
        '.': ['^'],
    },
}

def pretty_print(grid, beam_map):
    for i, line in enumerate(grid):
        result = [char for char in line]
        for j in range(len(result)):
            if grid[i][j] == '.':
                # print(i,j, beam_map[(i,j)])

                if len(beam_map[(i,j)]) > 1:
                    result[j] = str(len(beam_map[(i,j)]))
                elif len(beam_map[(i,j)]) == 1:
                    result[j] = list(beam_map[(i,j)])[0]
        print(''.join(result))
            

def energize(grid, starting_configuration):
    beam_map = {(i, j): set() for i in range(m) for j in range(n)}
    for p, s in starting_configuration:
        beam_map[p].add(s)
    current_hash = ''
    while str(beam_map) != current_hash:
        current_hash = str(beam_map)
        for (i,j) in beam_map:
            for b in beam_map[(i,j)]:
                for nb in paths[b][grid[i][j]]:
                    d_i, d_j = direction[nb]
                    if 0 <= i + d_i < m and 0 <= j + d_j < n:
                        beam_map[(i + d_i, j + d_j)].add(nb)
    return len([p for p in beam_map if beam_map[p]])
    # print('now')
    # pretty_print(grid, beam_map)


# Part 1
# print(energize(grid, [((0,0), '>')]))




def better_energize(grid, starting_configuration):
    beam_map = {(i, j): set() for i in range(m) for j in range(n)}
    beam_head = defaultdict(set)
    for p, s in starting_configuration:
        beam_head[p].add(s)
    # current_hash = ''
    while any(dir not in beam_map[p] for p in beam_head for dir in beam_head[p]):
        # current_hash = str(beam_map)
        for p in beam_head:
            for s in beam_head[p]:
                beam_map[p].add(s)
        new_beam_head = defaultdict(set)
        for (i, j) in beam_head:
            for b in beam_head[(i, j)]:
                for nb in paths[b][grid[i][j]]:
                    d_i, d_j = direction[nb]
                    if 0 <= i + d_i < m and 0 <= j + d_j < n:
                        new_beam_head[(i + d_i, j + d_j)].add(nb)
        beam_head = defaultdict(set)
        for p in new_beam_head:
            for s in new_beam_head[p]:
                beam_head[p].add(s)
    return len([p for p in beam_map if beam_map[p]])


# Part 1
print('part 1')
print(better_energize(grid, [((0, 0), '>')]))


# Part 2
print('part 2')
best = 0
for i in range(m):
    a = better_energize(grid, [((i, 0), '>')])
    b = better_energize(grid, [((i, n-1), '<')])
    if max(a, b) > best:
        best = max(a, b)
        print('i:', i, best)
print('halfway there')
for j in range(n):
    a = better_energize(grid, [((0, j), 'v')])
    b = better_energize(grid, [((m-1, j), '^')])
    if max(a, b) > best:
        best = max(a, b)
        print('j:', j, best)
