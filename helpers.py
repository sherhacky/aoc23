def get_input(filename, raw_input=False):
    if raw_input:
        with open('./' + filename) as f:
            line = f.readline()
            grid = []
            while line:
                grid.append(r"{}".format(line[:-1]))
                line = f.readline()
            return grid
    
    else:
        with open('./' + filename) as f:
            data = f.read()
            return data.split('\n')[:-1]


def generate_blank_grid(m, n, default_value=''):
    return [
        [
            default_value for _ in range(n)
        ] for _ in range(m)
    ]


def arrow_to_delta_map():
    return {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }


def shift_to_delta_map():
    return {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }


def cardinal_to_delta_map():
    return {
        'N': (-1, 0),
        'S': (1, 0),
        'W': (0, -1),
        'E': (0, 1)
    }


def fill_tool(grid, coordinate):
    pass


def euclidean_algorithm(a, b):
    r = [a, b]
    s = [1, 0]
    t = [0 ,1]
    while r[-1] != 0:
        q = r[-2] // r[-1]
        r.append(r[-2] - q*r[-1])
        s.append(s[-2] - q*s[-1])
        t.append(t[-2] - q*t[-1])
    return r[-2], s[-2], t[-2]


# input args of form 
# (x_1, a_1, n_1), (x_2, a_2, n_2), ...
# where the simultaneous system is 
# x_i cong a_i mod n_i
def crt(seq):
    a_1, n_1 = seq[0]
    a_2, n_2 = seq[1]
    g, m_1, m_2 = euclidean_algorithm(n_1, n_2)
    result = (
        a_1 * m_2 * n_2 + a_2 * m_1 * n_1
    ) % (n_1 * n_2)
    if len(seq) == 2:
        return result
    else:
        return crt([(result, n_1 * n_2)] + seq[2:])


def gcd(seq):
    g, m_1, m_2 = euclidean_algorithm(abs(seq[0]), abs(seq[1]))
    if len(seq) == 2:
        return g
    else:
        return gcd([g] + seq[2:])


def lcm(seq):
    n = gcd(seq[:2])
    p = abs(seq[0] * seq[1]) // n
    if len(seq) == 2:
        return p
    else:
        return lcm([p] + seq[2:])
