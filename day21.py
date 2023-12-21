import helpers
import itertools
from collections import defaultdict
import copy

input = helpers.get_input('input21test.txt')



# current = set()
# for i in range(len(input)):
#     for j in range(len(input[0])):
#         if input[i][j] == 'S':
#             current.add((i, j))

# for _ in range(6):
#     reachable = set()
#     for i, j in current:
#         # print(i)
#         # print(j)
#         for u in [[0,1],[-1,0],[1,0],[0,-1]]:
#             if 0 <= i+u[0] < m and 0 <= j+u[1] < n and input[i+u[0]][j+u[1]] in 'S.':
#                 reachable.add((i+u[0], j+u[1]))
#     #print(reachable)
#     current = set(list(reachable))

# # print(reachable)
# print(len(reachable))

# old_reachable = set(reachable)

# seen = set()
# current = set()



# grid_counter = {(i,j): set() for i in range()

def fake_2x_input(grid):
    k = len(grid[0]) // 2
    widened = [
        row[k:].replace('S', '.') + row + row[:k].replace('S', '.') for row in grid
    ]
    l = len(grid) // 2
    widened_no_S = [row.replace('S', '.') for row in widened]
    result = widened_no_S[l:] + widened + widened_no_S[:l]
    return result

# input = fake_2x_input(input)

m = len(input)
n = len(input[0])


# right now only works on even x even grids,
# which is what fake_2x_input() is for
def translation_count(steps):
    tracker = defaultdict(lambda: defaultdict(lambda : [0, 0]))


    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == 'S':
                tracker[(i,j)][0] = [0, 0]


    for _ in range(steps):
        new_tracker = defaultdict(lambda: defaultdict(lambda: [float('inf'), -float('inf')]))
        for (i,j) in tracker:
            for u in [[0, 1], [-1, 0], [1, 0], [0, -1]]:
                if input[(i+u[0]) % m][(j+u[1]) % n] in 'S.':
                    i_new = (i+u[0]) % m
                    j_new = (j+u[1]) % n

                    v_shift = -1 if (
                        i+u[0] == -1
                    ) else 1 if (
                        i+u[0] == m
                    ) else 0
                    h_shift = -1 if (
                        j+u[1] == -1
                    ) else 1 if (
                        j+u[1] == n
                    ) else 0

                    for a in tracker[(i,j)]:
                        l, r = tracker[(i,j)][a]
                        new_tracker[(i_new, j_new)][a + v_shift] = [
                            min(l + h_shift, 
                                new_tracker[(i_new, j_new)][a + v_shift][0]),
                            max(r + h_shift,
                                new_tracker[(i_new, j_new)][a + v_shift][1])
                        ]

        tracker = copy.deepcopy(new_tracker)

    return tracker


def count_tracker(tracker):
    result = sum(
        tracker[(i, j)][x][1] - tracker[(i, j)][x][0] + 1
        for (i, j) in tracker for x in tracker[(i, j)]
    )

    return result

for p in (6, 10, 50, 100, 500, 1000, 5000, 26501365):
    print(p, count_tracker(translation_count(p)))

# print(t[(5, 5)])



quit()


def convert_tracker(tracker_dict):
    result_set = set()
    for (i,j) in tracker_dict:
        for v_shift in tracker_dict[(i,j)]:
            l, r = tracker_dict[(i,j)][v_shift]
            for h_shift in range(l, r+1):
                result_set.add((v_shift * m + i, h_shift * n + j))
    return result_set


def count_reachable(steps):
    current = set()
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == 'S':
                current.add((i,j))

    for _ in range(steps):
        reachable = set()
        for i, j in current:
            # print(i)
            # print(j)
            for u in [[0, 1], [-1, 0], [1, 0], [0, -1]]:
                if input[(i+u[0]) % m][(j+u[1]) % n] in 'S.':
                    reachable.add((i+u[0], j+u[1]))
        # print(reachable)
        current = set(list(reachable))

    print(len(reachable))

    return reachable


def pretty_print(point_set):
    def get_char(i, j, point_set):
        return 'O' if (
            input[i % m][j % n] in 'S.' and (i,j) in point_set
        ) else 'X' if (
            input[i % m][j % n] not in 'S.' and (i, j) in point_set
        ) else '.' if (
            input[i % m][j % n] in 'S.'
        ) else '#'

    i_m, i_M = min(u[0] for u in point_set), max(u[0] for u in point_set)
    j_m, j_M = min(u[1] for u in point_set), max(u[1] for u in point_set)

    for i in range(i_m, i_M + 1):
        row = [get_char(i, j, point_set) for j in range(j_m, j_M + 1)]
        print (''.join(row))


# pretty_print(reachable)
# pretty_print(convert_tracker(tracker))

i = 0
old_way, new_way = None, None
while old_way == new_way:
    i += 1
    old_way = count_reachable(i)
    new_way = convert_tracker(translation_count(i))

print(old_way)
print(new_way)
pretty_print(old_way)
pretty_print(new_way)
print(i)
print(len(new_way))
print(new_way - old_way)

# reachable_list = [1]
# for i in range(1, 501):
#     reachable_list.append(count_reachable(i))
#     print(i, reachable_list[-1], reachable_list[-1] - reachable_list[-2])

# for i, m in enumerate(reachable_list[1:]):
#     print(i+1, m, m - reachable_list[i])