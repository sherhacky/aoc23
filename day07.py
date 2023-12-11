with open('./input07.txt') as f:
    data = f.read()

from collections import Counter
from itertools import product

# data = '''32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483
# '''

lines = data.split('\n')[:-1]

cards = 'AKQJT98765432'

def rank(hand):
    counts = Counter(hand).values()
    if 5 in counts:
        strength = 7
    elif 4 in counts:
        strength = 6
    elif 3 in counts and 2 in counts:
        strength = 5
    elif 3 in counts:
        strength = 4
    elif Counter(counts)[2] > 1:
        strength = 3
    elif 2 in counts:
        strength = 2
    else:
        strength = 1 #- min(cards.index(char) for char in hand)
    return (strength, ) + tuple([-cards.index(c) for c in hand])

deals = [(line.split(' ')[0], int(line.split(' ')[1])) for line in lines]

ranked_deals = sorted(deals, key = lambda x: rank(x[0]))
# print(ranked_deals)
print(sum(wager * (i+1) for i, (hand, wager) in enumerate(ranked_deals)))

# for h, w in ranked_deals:
#     print(h, w, rank(h))

def rank_with_jokers_brute_force(hand):
    cards = 'AKQT98765432J'
    best_rank = 0
    non_jokers = tuple([c for c in hand if c != 'J'])
    joker_count = Counter(hand).get('J', 0)
    for comb in product('AKQT98765432', repeat=joker_count):
        best_rank = max(best_rank, rank(''.join(comb + non_jokers))[0])
    return (best_rank, ) + tuple([-cards.index(c) for c in hand])

joker_ranked_deals = sorted(deals, key = lambda x: rank_with_jokers_brute_force(x[0]))
print(sum(wager * (i+1) for i, (hand, wager) in enumerate(joker_ranked_deals)))

