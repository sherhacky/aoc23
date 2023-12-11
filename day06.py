with open('./input06.txt') as f:
    data = f.read()

# data = '''Time:      7  15   30
# Distance:  9  40  200
# '''

lines = data.split('\n')[:-1]


def count_ways_to_win(time, distance):
    result = 1
    for i in range(len(time)):
        ways_to_win = 0
        for k in range(1, time[i]):
            if k * (time[i] - k) > distance[i]:
                ways_to_win += 1
        result *= ways_to_win
    return result


# or use quadratic fmla (faster):
def quadratic(time, distance):
    result = 1
    for i in range(len(time)):
        t, d = time[i], distance[i]
        root_a = (t - (t**2 - 4*d)**.5)/2
        root_b = (t + (t**2 - 4*d)**.5)/2
        left = int(root_a) + 1
        right = int(root_b) - int(root_b % 1 == 0)
        result *= (right - left + 1)
    return result


time = [int(i) for i in lines[0].split(' ')[1:] if i != '']
distance = [int(i) for i in lines[1].split(' ')[1:] if i != '']

print(quadratic(time, distance))
print(count_ways_to_win(time, distance))


time = [int(''.join([str(i) for i in time]))]
distance = [int(''.join([str(i) for i in distance]))]

print(quadratic(time, distance))
print(count_ways_to_win(time, distance))
