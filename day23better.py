import helpers
import itertools
from collections import defaultdict
import copy
import sys
import networkx as nx

input = helpers.get_input('input23.txt')
# input = helpers.get_input('input23test.txt')


arrow_to_delta = helpers.arrow_to_delta_map()


def print_path(input, path_points):
    for i in range(len(input)):
        row = [input[i][j] if (
            i, j) not in path_points else 'O' for j in range(len(input[i]))]
        print(''.join(row))
    print('')


G = nx.Graph()

for i in range(len(input)):
    for j in range(len(input[0])):
        if input[i][j] in '.^v<>':
            for d_i, d_j in arrow_to_delta.values():
                if (
                    0 < i + d_i < len(input)
                ) and (
                    0 < j + d_j < len(input[0])
                ) and (
                    input[i + d_i][j + d_j] in '.^v<>'
                ):
                    G.add_edge((i, j), (i + d_i, j + d_j))


H = nx.Graph()

vertices = {
    (0, 1),
    (len(input)-1, len(input[0])-2)
}

for i in range(len(input)):
    for j in range(len(input[0])):
        if (i,j) in G and len(G[(i,j)]) > 2:
            vertices.add((i,j))
print(len(vertices))

all_paths = set()

for u in vertices:
    for p in G[u]:
        seen = [u]
        dist = 1
        while p not in vertices:
            dist += 1
            seen.append(p)
            next_vertices = set(G[p]) - set(seen)
            # print(u, p, next_vertices)
            if len(next_vertices) > 1:
                print('uh oh', u, p, dist, next_vertices, seen)
                quit()
            p = next(iter(next_vertices))
        # print(u, p)
        # print(dist)
        # print(len(seen), seen)
        if u not in H or p not in H[u]:
            H.add_edge(u, p, weight=dist)
        else:
            if H[p][u]['weight'] != dist:
                print('fake branching at ', u, p)
            H[p][u]['weight'] = max(H[p][u]['weight'], dist)

        all_paths |= set(seen)

print_path(input, all_paths)

# print(G[(1,1)])

print('H', len(H))
for v in H:
    print(v, H[v])

G_paths = nx.all_simple_paths(
        G,
        (0, 1),
        (len(input)-1, len(input[0])-2))
p = next(G_paths)


H_path = [u for u in p if u in H]

for i in range(len(H_path) - 1):
    u, v = H_path[i], H_path[i+1]
    print(u, v, v in H[u])

# quit()

best = 0
for path in nx.all_simple_paths(
    H, 
    (0, 1), 
    (len(input)-1, len(input[0])-2)):
    total_distance = sum(
        H[path[i]][path[i+1]]["weight"] for i in range(len(path)-1)
    )
    if total_distance > best:
        print(total_distance)
        # print(path)
        best = total_distance

# print('done:', best-1)



