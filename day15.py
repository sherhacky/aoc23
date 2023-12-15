with open('./input15.txt') as f:
    data = f.read()

# data = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
# '''

asciis = [chr(i) for i in range(128)]


def hash_algorithm(string):
    cv = 0
    for char in string:
        cv += asciis.index(char)
        cv *= 17
        cv %= 256
    return cv


result = 0
for item in data[:-1].split(','):
    result += (hash_algorithm(item))

print(result)

lenses = [[] for _ in range(256)]
labels = [[] for _ in range(256)]

for instruction in data[:-1].split(','):
    label = instruction.split('=')[0].split('-')[0]
    op = instruction[len(label)]
    index = hash_algorithm(label)
    if op == '-':
        if label in labels[index]:
            lens_position = labels[index].index(label)
            lenses[index].pop(lens_position)
            labels[index].pop(lens_position)
    elif op == '=':
        focal_length = int(instruction.split('=')[1])
        if label in labels[index]:
            lens_position = labels[index].index(label)
            lenses[index][lens_position] = focal_length
        else:
            labels[index].append(label)
            lenses[index].append(focal_length)


print(
    sum(
        (index + 1) * (slot + 1) * (lenses[index][slot])
        for index in range(len(lenses))
        for slot in range(len(lenses[index]))
    )
)
