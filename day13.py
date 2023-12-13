with open('./input13.txt') as f:
    data = f.read()

# data = '''.##.##.##....##
# #.##..##.####.#
# ####...########
# #.#....#.####.#
# ##.#..#.##..##.
# #.#.##.#.#..#.#
# #.##..##.####.#
# #.##..##.#..#.#
# ##########..###
# .#.#..#.#.##.#.
# #.#.##.#.#..#.#
# '''

# lines = data.split('\n')[:-1]

grids = [chunk.split('\n') for chunk in data.split('\n\n')]
grids[-1] = grids[-1][:-1]

# print(grids)


def is_mirror_image(string, i):
    return all(string[i-k] == string[i+k+1] 
      for k in range(len(string)) if 0 <= i-k < i+k+1 < len(string))


def reflection_points(string):
    return set([i+1 for i in range(len(string) - 1) 
      if is_mirror_image(string, i)])


def fine_reflection_points(lines):
    cols = [[lines[i][j] for i in range(len(lines))] for j in range(len(lines[0]))]

    verticals = set([i for i in range(len(lines[0]))])
    horizontals = set([i for i in range(len(cols[0]))])
    for line in lines:
        verticals &= reflection_points(line)

    for line in cols:
        horizontals &= reflection_points(line)

    return [sorted(list(verticals)), sorted(list(horizontals))]




def toggle(grid, i, j):
    grid[i] = ''.join([char if k != j else (
        '.' if char == '#' else '#') for k, char in enumerate(grid[i])])

def value_after_fixed_smudge(grid):
    real_line_value = fine_reflection_points(grid)
    # for g in grid:
    #     print(g)
    # print('truth: ', real_line_value)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # print(i,j)
            toggle(grid, i, j)
            # for g in grid:
            #     print(g)
            this_try = fine_reflection_points(grid)
            if this_try != [[], []] and this_try != real_line_value:
                # print(i, j, this_try)
                for i in range(2):
                    this_try[i] = [el for el in this_try[i] if el not in real_line_value[i]]
                result = sum(this_try[0]) + 100*sum(this_try[1])
                # print(result)
                return result
            toggle(grid, i, j)
    return None

smudged = 0
for grid in grids:
    # print(value_after_fixed_smudge(grid))
    smudged += value_after_fixed_smudge(grid)
print(smudged)