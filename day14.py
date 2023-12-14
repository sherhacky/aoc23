from collections import defaultdict

with open('./input14.txt') as f:
    data = f.read()

# data = '''O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....
# '''

lines = data.split('\n')[:-1]

grid = [[char for char in line] for line in lines]
result = 0

def tilt(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            k = i
            while grid[k][j] == 'O' and k > 0 and grid[k-1][j] == '.':
                grid[k-1][j] = 'O'
                grid[k][j] = '.'
                k -= 1
    return grid

def score(grid):
    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'O':
                result += (len(grid) - i)
    return result


def rotate_cw(grid):
    result = []
    for j in range(len(grid[0])):
        result.append([grid[i][j] for i in range(len(grid))][::-1])
    return result


def stringify(grid):
    return '\n'.join([''.join(row) for row in grid])


def cycle(grid):
    for i in range(4):
        grid = rotate_cw(tilt(grid))
    return grid


# Part 1
print(score(tilt(grid)))


# Part 2
seen = defaultdict(list)
i = 0

while True:
    grid = cycle(grid)
    i += 1
    seen[stringify(grid)].append(i)
    L = seen[stringify(grid)]
    if len(L) > 1:
        a, b = L[-1], L[-2]
        if (10**9 - b) % (b - a) == 0:
            break

print(score(grid))