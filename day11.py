with open('./input11.txt') as f:
    data = f.read()


lines = data.split('\n')[:-1]

i_widen, j_widen = set(), set()

for i in range(len(lines)):
    if all(lines[i][j] == '.' for j in range(len(lines[0]))):
        i_widen.add(i)
for j in range(len(lines[0])):
    if all(lines[i][j] == '.' for i in range(len(lines))):
        j_widen.add(j)

# part 1 - actually widening the array
def taxicab(u, v):
    return abs(u[0] - v[0]) + abs(u[1] - v[1])


widened_lines = []

for i in range(len(lines)):
    new_line = ['..' if j in j_widen else lines[i][j] for j in range(len(lines[0]))]
    widened_lines.append(''.join(new_line))
    if i in i_widen:
        widened_lines.append('.'*(len(lines[0]) + len(j_widen)))

galaxy_coordinates = set(
    [
        (i, j) for i in range(len(widened_lines))
        for j in range(len(widened_lines[0]))
        if widened_lines[i][j] == '#'
    ]
)

result = sum(
    [
        taxicab(a, b) for a in galaxy_coordinates for b in galaxy_coordinates
        if a != b
    ]
)//2

print(result)


# part 2
def wide_taxicab(u, v, factor, i_widen, j_widen):
    return abs(u[0] - v[0]) + (factor - 1) * len([
        i for i in i_widen if min(u[0], v[0]) < i < max(u[0], v[0])
    ]) + abs(u[1] - v[1]) + (factor - 1) * len([
        j for j in j_widen if min(u[1], v[1]) < j < max(u[1], v[1])
    ])


galaxy_coordinates = set(
    [
        (i, j) for i in range(len(lines))
        for j in range(len(lines[0]))
        if lines[i][j] == '#'
    ]
)

result = sum(
    [
        wide_taxicab(a, b, 10**6, i_widen, j_widen) 
            for a in galaxy_coordinates 
            for b in galaxy_coordinates
            if a != b
    ]
)//2

print(result)
