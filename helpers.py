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
