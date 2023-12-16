from collections import defaultdict
from time import time


with open('./input16.txt') as f:
    line = f.readline()
    grid = []
    while line:
        grid.append(r"{}".format(line[:-1]))
        line = f.readline()

direction = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}


def pathing(arrow, cell):
    if cell == '.':
        return arrow
    elif cell == '|':
        return '^v' if arrow in '<>' else arrow
    elif cell == '-':
        return '<>' if arrow in '^v' else arrow
    elif cell == '/':
        return '^v><'['><^v'.index(arrow)]
    elif cell == '\\':
        return 'v^<>'['><^v'.index(arrow)]


def pretty_print(grid, beam_map):
    for i, line in enumerate(grid):
        result = [char for char in line]
        for j in range(len(result)):
            if grid[i][j] == '.':
                if len(beam_map[(i,j)]) > 1:
                    result[j] = str(len(beam_map[(i,j)]))
                elif len(beam_map[(i,j)]) == 1:
                    result[j] = list(beam_map[(i,j)])[0]
        print(''.join(result))
            

# First attempt - obsoleted by better_energize() below
def energize(grid, starting_configuration):
    m, n = len(grid), len(grid[0])
    beam_map = {(i, j): set() for i in range(m) for j in range(n)}
    for p, s in starting_configuration:
        beam_map[p].add(s)
    current_hash = ''
    while str(beam_map) != current_hash:
        current_hash = str(beam_map)
        for (i,j) in beam_map:
            for b in beam_map[(i,j)]:
                for nb in pathing(b, grid[i][j]):
                    d_i, d_j = direction[nb]
                    if 0 <= i + d_i < m and 0 <= j + d_j < n:
                        beam_map[(i + d_i, j + d_j)].add(nb)
    return len([p for p in beam_map if beam_map[p]])
    # print('\n')
    # pretty_print(grid, beam_map)


# Part 1
print('Part 1')
start_time = time()
print(energize(grid, [((0,0), '>')]))
print('Time taken: {}s\n'.format(str(time() - start_time)[:4]))


# Trying to save time by tracking just the 'frontier' of the beam (beam_head),
# rather than all 'energized' coordinates
def better_energize(grid, starting_configuration):
    m, n = len(grid), len(grid[0])
    beam_map = {(i, j): set() for i in range(m) for j in range(n)}
    beam_head = defaultdict(set)
    for p, s in starting_configuration:
        beam_head[p].add(s)
    while any(dir not in beam_map[p] for p in beam_head for dir in beam_head[p]):
        for p in beam_head:
            for s in beam_head[p]:
                beam_map[p].add(s)
        new_beam_head = defaultdict(set)
        for (i, j) in beam_head:
            for b in beam_head[(i, j)]:
                for nb in pathing(b, grid[i][j]):
                    d_i, d_j = direction[nb]
                    if 0 <= i + d_i < m and 0 <= j + d_j < n:
                        new_beam_head[(i + d_i, j + d_j)].add(nb)
        beam_head = defaultdict(set)
        for p in new_beam_head:
            for s in new_beam_head[p]:
                beam_head[p].add(s)
    return len([p for p in beam_map if beam_map[p]])


# Part 1
print('part 1 (with better algo)')
start_time = time()
print(better_energize(grid, [((0, 0), '>')]))
print('Time taken: {}s\n'.format(str(time() - start_time)[:4]))


# Part 2
print('part 2')
start_time = time()
m, n = len(grid), len(grid[0])
best = 0
for i in range(m):
    a = better_energize(grid, [((i, 0), '>')])
    b = better_energize(grid, [((i, n-1), '<')])
    if max(a, b) > best:
        best = max(a, b)
        print('i:', i, best, '(at {}s)'.format(str(time() - start_time)[:4]))
print('halfway there:')
print('{}s elapsed'.format(str(time() - start_time))[:5])
for j in range(n):
    a = better_energize(grid, [((0, j), 'v')])
    b = better_energize(grid, [((m-1, j), '^')])
    if max(a, b) > best:
        best = max(a, b)
        print('j:', j, best, '(at {}s)'.format(str(time() - start_time)[:5]))
print('Final answer: {}\n{}s to finish'.format(
    best,
    str(time() - start_time)[:5]
))
