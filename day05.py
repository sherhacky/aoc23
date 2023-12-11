import collections
from time import time

with open('./input05.txt') as f:
    data = f.read()

# data = '''seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4
# '''

mapping = dict()


chunks = data.split('\n\n')
chunks[-1] = chunks[-1][:-1]

seeds = [int(item) for item in chunks[0].split(': ')[1].split(' ')]

print(seeds)


def get_lowest_location(seeds):
    best = float('inf')
    for seed in seeds:
        current = seed
        for chunk in chunks[1:]:
            rows = chunk.split('\n')[1:]
            for row in rows:
                b, a, r = [int(num) for num in row.split(' ')]
                if a <= current <= a + r:
                    current = b + (current - a)
                    break
        best = min(best, current)
    return best


current = set()
for chunk in chunks[1:][::-1]:
    new = []
    rows = chunk.split('\n')[1:]
    added = False
    for row in rows:
        b, a, r = [int(num) for num in row.split(' ')]
        new += [a, b]
        for c in current:
            if b <= c <= b + r:
                c = a + (c - b)
            new.append(c)
    current = set([c for c in new])

print('lower endpoints:', len(current))
for s in seeds[::2]:
    print(s, get_lowest_location([s]))
print(get_lowest_location(current))

to_check = [c for c in current if any(seeds[2*i] <= c < seeds[2*i] + seeds[2*i+1] for i in range(len(seeds)//2 - 1))]

# print(sorted(to_check))

print(get_lowest_location(to_check))
