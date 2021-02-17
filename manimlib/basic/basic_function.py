import numpy as np


def axes_point(*line_space_array):
    # items=line
    return [axis_point(each) for each in line_space_array]


def axis_point(line_space):
    for i in range(3, 5):
        try:
            if isinstance(line_space[i][0], (int, float)):
                pass
        except:
            try:
                isinstance(line_space[i], (int, float))
                line_space[i] = [line_space[i]]
            except:
                line_space.append([])
    return line_space[3]+[line_space[0]+line_space[1]*i for i in range(line_space[2])]+line_space[4]


def coord_grid(x, y, z=[0]):
    return list(zip(*list(np.array_split(np.array((np.broadcast_arrays(*[each[(slice(None),)+(None,)*i] for i, each in enumerate(map(np.asarray, [x, y, z]))]))).flat, 3))))
