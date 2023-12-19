import helpers


input = helpers.get_input('input19.txt')


workflows = input[:input.index('')]
workflow = dict()
for line in workflows:
    name = line.split('{')[0]
    workflow[name] = line.split('{')[1][:-1].split(',')

parts = input[input.index('')+1:]


# Part 1
result = 0

for part in parts:
    val = dict()
    for eq in part[1:-1].split(','):
        val[eq[0]] = int(eq[2:])
    current = 'in'
    while current not in 'RA':
        for term in workflow[current]:
            if ':' in term:
                expr, dest = term.split(':')
                if eval(expr, val):
                    current = dest
                    break
            else:
                current = term
                break
    if current == 'A':
        result += sum(val[char] for char in 'xmas')

print(result)    
    

# Part 2
def count_acceptable(conditions_list):
    result = 1
    for char in 'xmas':
        result *= len(
            [
                n for n in range(1, 4001) if all(
                    eval(condition, {char: n})
                    for condition in conditions_list if char in condition)
            ]
        )
    return result


def traverse(node, conditions_stack=[]):    
    if node == 'A':
        return count_acceptable(conditions_stack)

    elif node == 'R':
        return 0

    result = 0
    this_node_conditions = []
    for instruction in workflow[node]:
        if ':' in instruction:
            condition = instruction.split(':')[0]
            dest = instruction.split(':')[1]
            this_node_conditions.append(condition)
            result += traverse(dest, conditions_stack + this_node_conditions)
            this_node_conditions.pop()
            this_node_conditions.append(
                condition.replace('<', '>=') if '<' in condition else
                condition.replace('>', '<='))

        else:
            result += traverse(
                instruction,
                conditions_stack + this_node_conditions
            )
    return result


print(traverse('in'))
