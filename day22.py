import helpers
import itertools
from collections import defaultdict
import copy

input = helpers.get_input('input22.txt')


bricks = [tuple(eval('(' + r + ')') for r in row.split('~')) for row in input]


# print(bricks)

def interpolate(b):
    p, q = b
    m = [min(p[i], q[i]) for i in range(len(p))]
    M = [max(p[i], q[i]) for i in range(len(p))]
    return tuple(
        itertools.product(
            *[range(m[i], M[i] + 1) for i in range(len(p))]
        )
    )

bricks = [interpolate(b) for b in bricks]
# track = {bricks[i]: 'ABCDEFG'[i] for i in range(len(bricks))}

def shift_down_one(b):
    return tuple((p[0], p[1], p[2]-1) for p in b)


def settle(bricks):
    to_process = set(bricks)
    result = set()
    occupied = set()
    while any(to_process):
        b = min(to_process, key=lambda x: min(p[2] for p in x))
        to_process.discard(b)
        # start = tuple(b)
        while all(p[2] >= 1 and p not in occupied for p in shift_down_one(b)):
            b = shift_down_one(b)
        occupied |= set(b)
        result.add(b)
        # track[b] = track[start]
        # del(track[start])
    # occupied_2 = {p for b in result for p in b}
    # if occupied != occupied_2:
    #     print('failure')
    #     return None
    # if any(all(p[2] >= 1 and p not in occupied for p in shift_down_one(b)) for b in result):
        
    #     result = settle(result)
    # if len(result) != len(bricks):
    #     return 'Failure'
    return result

def supporters(bricks, t):
    result = set()
    occupied = {p: brick for brick in bricks for p in brick}
    for p in t:
        if (p[0], p[1], p[2] - 1) in occupied:
            result.add(occupied[(p[0], p[1], p[2] - 1)])
    result.discard(t)
    return result

# assumes bricks is settled
def safe_to_remove(settled_bricks, b):
    occupied = {p: brick for brick in settled_bricks for p in brick}
    for p in b:
        q = (p[0], p[1], p[2] + 1)
        if q in occupied and q not in b:
            t = occupied[q]
            if len(supporters(settled_bricks, t)) <= 1:
                return False
            
    return True


bricks = settle(bricks)

# blist = sorted(bricks, key=lambda x: x[::-1])
# for i,b in enumerate(blist):
#     print(i, b)
#     print(len(supporters(blist, b)), [blist.index(c) for c in supporters(blist, b)])

final_answer = 0
for b in bricks:
    tv = safe_to_remove(bricks, b)
    print(b, tv)
    if tv: 
        final_answer += 1

print(final_answer)

# def bricks_on_top_that_would_fall(bricks, b):
#     result = set()
#     occupied = {p: brick for brick in bricks for p in brick}
#     for p in b:
#         q = (p[0], p[1], p[2] + 1)
#         if q in occupied and q not in b:
#             t = occupied[q]
#             if len(supporters(bricks, t)) <= 1:
#                 result.add(t)
#     return result


# def fill_in_total_bricks_that_fall(dp, bricks, b):
#     if b in dp:
#         return dp[b]
#     result = bricks_on_top_that_would_fall(bricks, b)
#     for t in list(result):
#         result |= fill_in_total_bricks_that_fall(dp, bricks, t)
#     dp[b] = result
#     return result


# final_dp = dict()
# for b in bricks:
#     fill_in_total_bricks_that_fall(final_dp, bricks, b)

# print(sum(len(s) for s in final_dp.values()))

def count_fallen_bricks(settled_bricks, brick):
    return(len(
        settled_bricks - settle(bricks - {brick, })
    ))


def count_fallen_bricks_actually(settled_bricks, brick):
    to_process = settled_bricks - {brick,}
    occupied = {p for b in to_process for p in b}
    fallen = 0
    while any(to_process):
        b = min(to_process, key=lambda x: min(p[2] for p in x))
        to_process.discard(b)
        # start = tuple(b)
        if all(p[2] >= 1 and p not in (occupied - set(b)) for p in shift_down_one(b)):
            occupied -= set(b)
            fallen += 1
    return fallen

# Part 2 - this takes like 40 minutes to run lol
result = 0
for i, brick in enumerate(bricks):
    k = count_fallen_bricks_actually(bricks, brick)
    print(i, k)
    result += k

print(result)