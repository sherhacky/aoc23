with open('./input18.txt') as f:
    data = f.read()

# data = '''R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)
# '''

lines = data.split('\n')[:-1]

delta = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

def do_the_problem(lines):



    visited = set()

    current = (0, 0)
    for line in lines:
        visited.add(current)
        [direction, distance, color] = line.split(' ')
        distance = int(distance)
        for k in range(distance):
            current = tuple([current[i] + delta[direction][i] for i in range(2)])
            visited.add(current)

    # print(visited)

    m = min([min(u) - 1 for u in visited])
    M = max([max(u) + 1 for u in visited])
    dimensions = M - m 
    grid = [['.' for _ in range(dimensions)] for _ in range(dimensions)]

    for i, j in visited:
        grid[i-m][j-m] = '#'

    # for row in grid:
    #     print(''.join(row))

    print(' I made the dang grid: length {}'.format(len(grid)))

    def mark_exterior(grid):
        outside_current = set()

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '.' and (
                    i in (0, len(grid) - 1) or
                    j in (0, len(grid[0]) - 1)
                ):
                    outside_current.add((i, j))

        while any(outside_current):
            for (i, j) in outside_current:
                grid[i][j] = 'O'
            outside_next = {
                (i + a, j + b) for (i, j) in outside_current
                for (a, b) in [(0, 1), (-1, 0), (1, 0), (0, -1)]
                if 0 <= i+a < len(grid)
                and 0 <= j+b < len(grid[0])
                and grid[i+a][j+b] == '.'
            }
            outside_current = set(outside_next)
        
        return grid

    grid = mark_exterior(grid)

    # for row in mark_exterior(grid):
    #     print(''.join(row))

    return sum(
            [
                1 if grid[i][j] in '#.' else 0
                for i in range(len(grid))
                for j in range(len(grid[0]))
            ]
        )

print(do_the_problem(lines))

mapping = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}

newlines = []
for line in lines:
    hexa_d = line.split('#')[1].split(')')[0]
    newlines.append(' '.join(
        [
            mapping[int(hexa_d[-1])],
            str(int(hexa_d[:-1], 16)),
            '.'
        ]
    ))

for line in newlines:
    print(line)


def create_segments(lines):
    segments = []
    current = (0, 0)
    for line in lines:
        [direction, distance, color] = line.split(' ')
        subsequent = tuple([current[i] + delta[direction][i]*int(distance)
                           for i in range(2)])
        segments.append((current, subsequent))
        current = tuple(subsequent)
    return segments


def mark_exterior(grid):
    outside_current = set()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '.' and (
                i in (0, len(grid) - 1) or
                j in (0, len(grid[0]) - 1)
            ):
                outside_current.add((i, j))

    while any(outside_current):
        for (i, j) in outside_current:
            grid[i][j] = 'O'
        outside_next = {
            (i + a, j + b) for (i, j) in outside_current
            for (a, b) in [(0, 1), (-1, 0), (1, 0), (0, -1)]
            if 0 <= i+a < len(grid)
            and 0 <= j+b < len(grid[0])
            and grid[i+a][j+b] == '.'
        }
        outside_current = set(outside_next)

    return grid


def measure_interior(lines):
    segments = create_segments(lines)
    m, M = 0, 0
    for s in segments:
        for t in s:
            m = min(m, t[0])
            M = max(M, t[0])

    I = sorted(set([p[0] for s in segments for p in s]))
    J = sorted(set([p[1] for s in segments for p in s]))

    weights = [[0 for _ in range(len(J)*2 - 1)] for _ in range(len(I)*2 - 1)]

    for i in range(len(I)):
        for j in range(len(J)):
            weights[2*i][2*j] = 1
            if i + 1 < len(I):
                weights[2*i + 1][2*j] = I[i+1] - I[i] - 1
            if j + 1 < len(J):
                weights[2*i][2*j + 1] = J[j+1] - J[j] - 1
            if i + 1 < len(I) and j + 1 < len(J):
                weights[2*i + 1][2*j + 1] = weights[2 *
                                                    i + 1][2*j] * weights[2*i][2*j + 1]
        
    grid = [['.' for _ in range(len(weights[0]))] for _ in range(len(weights))]

    for s in segments:
        i_a = min(I.index(t[0]) for t in s)
        i_b = max(I.index(t[0]) for t in s)
        j_a = min(J.index(t[1]) for t in s)
        j_b = max(J.index(t[1]) for t in s)
        for i in range(2*i_a, 2*i_b+1):
            for j in range(2*j_a, 2*j_b+1):
                grid[i][j] = '#'

    for g in grid:
        print(''.join(g))

    grid = mark_exterior(grid)

    result = sum(
        [
            weights[i][j] for i in range(len(grid)) for j in range(len(grid[0]))
            if grid[i][j] in '#.'
        ]
    )

    return result


    for l in weights:
        print(l)
    

print(
    measure_interior(lines)
)

print(
    measure_interior(newlines)
)

# print('\n')

# for s in create_segments(lines):
#     print(s)

# print('\n')

# for s in create_segments(newlines):
#     print(s)

