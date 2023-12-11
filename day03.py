with open('./input03.txt') as f:
    data = f.read()

# data = '''467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
# '''

lines = data.split('\n')[:-1]

result = 0
i = 0

number_start_location = dict()
number_at = dict()

while i < len(lines):
    j = 0
    in_group = False
    while j <= len(lines[i]):
        if not in_group and j < len(lines[i]) and lines[i][j] in '0123456789':
            in_group = True
            group_start = j
        elif in_group and (j == len(lines[i]) or lines[i][j] not in '0123456789'):
            candidate = int(lines[i][group_start:j])
            counts = False
            for a in range(max(0, i-1), min(len(lines), i+2)):
                for b in range(max(0, group_start-1), min(len(lines[i]), j+1)):
                    if lines[a][b] not in '0123456789.':
                        counts = True
            if counts:
                result += candidate
            in_group = False
            # track starting locations of numbers
            for b in range(group_start, j):
                number_start_location[(i,b)] = (i, group_start)
                number_at[(i, group_start)] = candidate
        j += 1
    i += 1

print(result)

gears = 0
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] == '*':
            neighbor_nums = set()
            for a in range(i-1, i+2):
                for b in range(j-1, j+2):
                    if (a,b) in number_start_location:
                        neighbor_nums.add(number_start_location[(a,b)])
            if len(neighbor_nums) == 2:
                nn_list = list(neighbor_nums)
                gears += number_at[(nn_list[0])] * number_at[(nn_list[1])]

print(gears)