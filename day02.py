with open('./input02.txt') as f:
    data = f.read()

# data = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
# '''

lines = data.split('\n')[:-1]

limit = {'red': 12, 'green': 13, 'blue': 14}
sum_of_vals = 0
sum_of_powers = 0

for game in lines:
    possible = True
    rounds = game.split(': ')[1].split('; ')
    maxes = {'red': 0, 'green': 0, 'blue': 0}
    for r in rounds:
        counts = dict()
        pulls = r.split(', ')
        for p in pulls:
            counts[p.split(' ')[1]] = int(p.split(' ')[0])
            maxes[p.split(' ')[1]] = max(maxes[p.split(' ')[1]], int(p.split(' ')[0]))
        if any(counts[color] > limit[color] for color in counts):
            possible = False
        
    if possible:
        sum_of_vals += int(game.split(': ')[0].split(' ')[-1])

    sum_of_powers += maxes['red'] * maxes['green'] * maxes['blue']

print(sum_of_vals)
print(sum_of_powers)