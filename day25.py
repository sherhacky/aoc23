import helpers
import itertools
from collections import defaultdict
import copy
import sys
import networkx as nx


input = helpers.get_input('input25.txt')
# input = helpers.get_input('input25test.txt')


G = nx.Graph()

for row in input:
    l, r = row.split(': ')
    for e in r.split(' '):
        G.add_edge(l, e)
    
for u in nx.minimum_edge_cut(G):
    G.remove_edge(*u)

i = nx.connected_components(G)
print(len(set(next(i)))*len(set(next(i))))
