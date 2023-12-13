with open('./input13.txt') as f:
    data = f.read()

grids = [chunk.split('\n') for chunk in data.split('\n\n')]
grids[-1] = grids[-1][:-1]


def is_mirror_image(string, i):
    return all(string[i-k] == string[i+k+1] 
      for k in range(len(string)) if 0 <= i-k < i+k+1 < len(string))


def reflection_points(string):
    return set([i+1 for i in range(len(string) - 1) 
      if is_mirror_image(string, i)])


def find_reflection_points(lines):
    cols = [
        [lines[i][j] for i in range(len(lines))] 
            for j in range(len(lines[0]))
    ]
    verticals = set([i for i in range(len(lines[0]))])
    horizontals = set([i for i in range(len(cols[0]))])
    for line in lines:
        verticals &= reflection_points(line)
    for line in cols:
        horizontals &= reflection_points(line)
    return [sorted(list(verticals)), sorted(list(horizontals))]


# Part 1
result = 0
for grid in grids:
    points = find_reflection_points(grid)
    result += sum(points[0])
    result += 100 * sum(points[1])
print(result)


# Part 2
def toggle(grid, i, j):
    grid[i] = ''.join([char if k != j else (
        '.' if char == '#' else '#') for k, char in enumerate(grid[i])])


def value_after_fixed_smudge(grid):
    actual_reflection_points = find_reflection_points(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            toggle(grid, i, j)
            this_try = find_reflection_points(grid)
            if this_try != [[], []] and this_try != actual_reflection_points:
                for i in range(2):
                    this_try[i] = [el for el in this_try[i] 
                        if el not in actual_reflection_points[i]]
                result = sum(this_try[0]) + 100 * sum(this_try[1])
                return result
            toggle(grid, i, j)


unsmudged_sum = 0
for grid in grids:
    unsmudged_sum += value_after_fixed_smudge(grid)
print(unsmudged_sum)