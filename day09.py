with open('./input09.txt') as f:
    data = f.read()

# data = '''0 3 6 9 12 15
# 1 3 6 10 15 21
# 10 13 16 21 30 45
# '''

lines = data.split('\n')[:-1]

sequences = [[int(c) for c in line.split(' ')] for line in lines]

right_result = 0
left_result = 0

for s in sequences:
    rightmost = [s[-1]]
    leftmost = [s[0]]
    current = s
    while any(n != 0 for n in current):
        current = [current[i+1] - current[i] for i in range(len(current) -1)]
        rightmost.append(current[-1])
        leftmost.append(current[0])
    right_result += sum(rightmost)
    left_result += sum([n * (-1)**i for i, n in enumerate(leftmost)])

print(right_result)
print(left_result)