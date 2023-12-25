import helpers
import itertools
from collections import defaultdict
import copy
import sys



input = helpers.get_input('input23.txt')
test_input = helpers.get_input('input23test.txt')

# max_depth = len([char for row in input for char in row if char == '.'])

# print(max_depth)
# sys.setrecursionlimit(max_depth + 10)


arrow_to_delta = helpers.arrow_to_delta_map()

def next_options(input, start, points_to_avoid):
    i, j = start
    result = set()
    for d_i, d_j in arrow_to_delta.values():
        if (
            0 < i + d_i < len(input)
         ) and (
            0 < j + d_j < len(input[0])
         ) and (
            (i + d_i, j + d_j) not in points_to_avoid
         ) and (
            input[i + d_i][j + d_j] in '.^v<>'
         ):
            result.add((i + d_i, j+ d_j))
    return result

# def find_next_branch_point(input, start, direction, points_to_avoid):
#     i,j = start
#     for d_i, d_j in arrow_to_delta.values():
#         if (d_i, d_j) != direction:
#             points_to_avoid.add((i + d_i, j + d_j))
#     path_length = 0
#     np = next_options(input, start, points_to_avoid)
#     while len(np) == 1:
#         current = np[0]
#         path_length += 1
#         np = next_options(input, current, {current})
#     if np

def dijkstra_ish(input):
    branch_points = {(i,j) for i in range(len(input)) for j in range(len(input[0])) if (
        len(next_options(input, (i,j), set())) > 2
    )}
    d = defaultdict(list)
    d[(len(input) - 1, len(input[0]) - 2)] = [(0, frozenset())]
    print(branch_points)
    print(max(branch_points))
    print(len(branch_points))

dijkstra_ish(input)

def print_path(input, path_points):
    for i in range(len(input)):
        row = [input[i][j] if (i,j) not in path_points else 'O' for j in range(len(input[i]))]
        print(''.join(row))
    print('')

def longest_walk_avoiding(dp, input, points_to_avoid, start):
    # print(start)
    if start == (len(input) - 1, len(input[0]) - 2):
        return 0
    if (points_to_avoid, start) in dp:
        return dp[(points_to_avoid, start)]
    else:
        next_points = set()
        i, j = start
        if False:
            pass
        # if input[i][j] in '^v<>':
        #     d_i, d_j = arrow_to_delta[input[i][j]]
        #     if (i + d_i, j + d_j) not in points_to_avoid:
        #         next_points.add((i+d_i, j+d_j))
        else:
            for d_i, d_j in arrow_to_delta.values():
                # print('  ', d_i, d_j)
                if input[i+d_i][j+d_j] in '.^v<>' and (i + d_i, j+ d_j) not in points_to_avoid:
                    next_points.add((i+d_i, j+d_j))
        if len(next_points) == 0:
            return -float('inf')
        next_points_to_avoid = frozenset(points_to_avoid | {(i,j),})
        best = -float('inf')
        for p in next_points:
            best = max(best, longest_walk_avoiding(dp, input, next_points_to_avoid, p))
        dp[(points_to_avoid, start)] = best + 1
        # print(best + 1)
        # if len(points_to_avoid) > 90:
        #     print_path(input, points_to_avoid)
        return best + 1

# dp = dict()
# print(longest_walk_avoiding(dp, input, frozenset(), (0,1)))



# traversal(input)