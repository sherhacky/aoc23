with open('./input04.txt') as f:
    data = f.read()

# data = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
# '''

lines = data.split('\n')[:-1]
match_counts = [0] * len(lines)
card_counts = [1] * len(lines)
total_points = 0
for i,card in enumerate(lines):
    left = card.replace('  ', ' ').split(': ')[1].split(' | ')[0].split(' ')
    right = card.replace('  ', ' ').split(': ')[1].split(' | ')[1].split(' ')

    matches = set(left) & set(right)
    if any(matches):
        point_value = 2**(len(set(left) & set(right)) - 1)
        total_points += point_value
        match_counts[i] = len(matches)

for i in range(len(card_counts)):
    for j in range(1, match_counts[i]+1):
        if i + j < len(card_counts):
            card_counts[i+j] += card_counts[i]

print(total_points)
print(sum(card_counts))