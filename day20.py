import helpers
from collections import defaultdict
from math import log2
import itertools

input = helpers.get_input('input20.txt')


destination =  dict()
flip_flops = dict()
conj = dict()


for line in input:
    m, d = line.split(' -> ')
    if m[0] == '%':
        flip_flops[m[1:]] = 0
    elif m[0] == '&':
        conj[m[1:]] = dict()
    m = m[1:] if m[0] in '%&' else m
    destination[m] = d.split(', ')

for key in destination:
    for d in destination[key]:
        if d in conj:
            conj[d][key] = 0


print(destination)
print(flip_flops)
print(conj)

track_state = defaultdict(int)

def press_button():
    current_pulses = [('broadcaster', 'button', 0)]
    next_pulses = []
    result = [1, 0]
    # print('button -low-> broadcaster')
    while any(current_pulses):
        # print(current_pulses)
        for p in current_pulses:
            module, source, pulse = p
            if module == 'broadcaster':
                for dest in destination['broadcaster']:
                    # print('broadcasting to {}'.format(dest))
                    if dest in conj:
                        conj[dest]['broadcaster'] = pulse
                    next_pulses.append((dest, 'broadcaster', pulse))
                    result[pulse] += 1
                    # print('broadcaster -{}-> {}'.format(
                    #     'high' if pulse else 0,
                    #     dest
                    # ))
            elif module in flip_flops:
                # print('flipping at {}: {}'.format(module, pulse))
                if pulse == 0:
                    flip_flops[module] = 1 - flip_flops[module]
                    track_state[module] = flip_flops[module]
                    for q in destination[module]:
                        if q in conj:
                            conj[q][module] = flip_flops[module]
                        next_pulses.append((q, module, flip_flops[module]))
                        # print('{} -{}-> {}'.format(
                        #     module,
                        #     'high' if flip_flops[module] else 'low',
                        #     q
                        # ))
                        result[flip_flops[module]] += 1
            elif module in conj:
                # print('conjing at {} with {}, {}'.format(module, pulse, conj))
                # conj[module][source] = pulse
                new_pulse = 0 if all(
                    conj[module][s] == 1 for s in conj[module]
                ) else 1
                track_state[module] = new_pulse
                for q in destination[module]:
                    if q in conj:
                        conj[q][module] = new_pulse
                    next_pulses.append((q, module, new_pulse))
                    # print('{} -{}-> {}'.format(
                    #     module,
                    #     'high' if new_pulse else 'low',
                    #     q
                    # ))
                    result[new_pulse] += 1
            elif module == 'output':
                pass
                # result[pulse] += 1
                # print('{} -{}-> output'.format(
                #     source,
                #     'high' if pulse else 'low'
                # ))
            else:
                # print('oh no. a pulse to nowhere')
                # print(module)
                if pulse == 0:
                    return 'done'
        current_pulses = list(next_pulses)
        next_pulses = []

    return result 


sources = dict()

for key, val_list in destination.items():
    for d in val_list:
        if d not in sources:
            sources[d] = set()
        sources[d].add(key)

from collections import defaultdict
seen = set()
pulses = [0,0]
presses = 0
previous = dict()
record = defaultdict(list)
# for _ in range(10):
#     for module in ['ft', 'qr', 'lk', 'lz']:
#         for t in sources[module]:
#             record[t].append(track_state[t])
#     press_button()
#     presses += 1

# for module in ['ft', 'qr', 'lk', 'lz']:
#     print('--{}--'.format(module))
#     for k in sources[module]:
#         value = record[k]
#         print('   ',
#               k,
#               value
#               )

for _ in range(30000):
# while True:
    presses += 1
    pulses = press_button()
    for module in ['ft', 'qr', 'lk', 'lz']:
        for t in sources[module]:
            if not record[t]:
                record[t].append(0)
            # if (
            #     t not in seen
            #     # t == 'mv'
            #  ) and 
            if (
                (t in track_state)
                    # and track_state[t]==1
                ) and (
                        (
                        t in previous and previous[t] != track_state[t]
                    ) or (
                        t not in previous and track_state[t]==1
                    )
                ):
                record[t].append(presses)
                # previous[t] = track_state[t]
                # seen.add(t)
            if t in track_state:
                previous[t] = track_state[t]

# for key, value in record.items():
#    print(key, value[:16])
# print(presses)



def compress(sequence):
    if not sequence:
        return sequence
    current = sequence[0]  
    result = []  
    counter = 1
    i = 1
    while i < len(sequence):
        if sequence[i] == current:
            counter += 1
        else:
            result.append(
                (current, counter)
            )
            counter = 1
            current = sequence[i]
        i += 1
    result.append(
        (current, counter)
    )
    return result

restrictions = dict()

for module in ['ft', 'qr', 'lk', 'lz']:
    chunklist = []
    print('--{}--'.format(module))
    for k in sorted(sources[module],
    key = lambda x: record[x][1]):
        value = record[k]
        chunks = compress(
            [value[i+1] - value[i] for i in range(len(value)-1)]
        )[:4]
        chunklist.append(chunks)
        print('   ',
            k,
            # value[0],
            chunks[0][0]*chunks[0][1] + chunks[1][0],
            chunks,
        )
    chunks = chunklist[1]
    modulus = chunks[0][0]*chunks[0][1] + chunks[1][0]
    restrictions[modulus] = dict()
    for s in chunklist:
        restrictions[modulus][int(log2(s[0][0]))] = 1
    print(restrictions[modulus])


def find_minimal_solution(restrictions):
    best = float('inf')
    count_missing = 12 * len(restrictions) - sum(
        [len(v) for v in restrictions.values()]
    )
    for f in itertools.product([0, 1], repeat=count_missing):
        i = 0
        seq = []
        for modulus in restrictions:
            target = 0
            for d in range(12):
                if d in restrictions[modulus]:
                    target += 2**d
                else:
                    target += 2**f[i]
                    i += 1
            if target <= modulus:
                seq.append((target, 2**12))
        if len(seq) == len(restrictions):
            this_try = helpers.crt(seq)
            if this_try < best:
                best = this_try
                print('new best, ', best, seq)
    return best

print(find_minimal_solution(restrictions))

for k in restrictions:
    print(sum([2**i for i in restrictions[k]]))

# print(len(seen))

# total = [0, 0]
# for _ in range(1000):
#     pulses = press_button()
#     for i in range(2):
#         total[i] += pulses[i]

# print(total)

# print(total[0]*total[1])


# least_positive_signal = {
#     line.split(' -> ')[0]: 0 for line in input
# }



# while least_positive_signal['rx'] == 0:
#     for target in sources:
#         if target[least_positive_signal] 


