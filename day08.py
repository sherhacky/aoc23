from numpy import lcm


with open('./input08.txt') as f:
    data = f.read()


lines = data.split('\n')[:-1]

directions = lines[0]
links = lines[2:]

next_loc = dict()
for a in links:
    next_loc[a[:3]] = (a[7:10], a[12:15])

current = 'AAA'
steps = 0
i = 0
while current != 'ZZZ':
    current = next_loc[current]['LR'.index(directions[i])]
    i = (i + 1) % len(directions)
    steps += 1

print(steps)


z_lists = dict()

for loc in next_loc:
    if loc[-1] == 'A':
        steps, i = 0, 0
        z_list = []
        visited = [loc]
        done = False
        while not done:
            steps += 1
            visited.append(next_loc[visited[-1]]['LR'.index(directions[i])])
            i = (i + 1) % len(directions)
            if visited[-1][-1] == 'Z':
                z_list.append(steps)
            if len(visited) > len(directions) + 1 and any(
                visited[-1] == v for v in visited[-1-len(directions):0:-len(directions)]
            ):
                done = True
        z_lists[visited[0]] = z_list

# Just using the lcm only works here because the z_lists
# all had length 1.  More complicated "visiting Z" behavior would
# require a more complicated solution...
results = [l[0] for l in z_lists.values()]
print(lcm.reduce(results))
