import numpy as np
import copy

from manimlib.mobject.mobject import Mobject


def axes_point(*line_space_array):
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
    return np.array(list(zip(*list(np.array_split(np.array(list(np.broadcast_arrays(*[each[(slice(None),)+(None,)*i] for i, each in enumerate(map(np.asarray, [x, y, z]))]))).flat, 3))))).tolist()


def to_get_point(mobject_or_point, default=[0, 0, 0]):
    if isinstance(mobject_or_point, (Mobject)):
        mobject_or_point = mobject_or_point.get_center()
    elif isinstance(mobject_or_point, (int,float)):
        mobject_or_point = default.point_from_proportion(mobject_or_point)
    elif isinstance(mobject_or_point, str) and mobject_or_point == "get_center()":
        mobject_or_point = default.get_center()
    return mobject_or_point


def to_expand_lists(lists, shape=None, fill=None):
    if shape == None:
        x, y = np.shape(lists)
        result = np.zeros((x, 3))
        result[:x, :y] = lists
        return result
    else:
        return (np.ones(np.shape(shape))*lists).tolist()


def to_get_offset_lists(mobject_or_point, offset):
    mobject_or_point = to_get_point(mobject_or_point)
    dim = len(mobject_or_point)
    mobject_or_point = np.repeat([mobject_or_point], dim, axis=0)
    point_array = to_expand_lists(mobject_or_point)
    for i, each in enumerate(offset):
        if isinstance(each, (int, float)):
            offset[i] = (
                point_array+to_expand_lists(np.identity(dim))*each).tolist()
        elif isinstance(each, (list)):
            offset[i] = (point_array+to_expand_lists(np.identity(
                dim))*(each+[0, 0, 0])[:dim]).tolist()
        elif isinstance(each, (tuple)):
            offset[i] = ((1-to_expand_lists(np.identity(
                dim)))*point_array + to_expand_lists(np.identity(
                    dim))*(list(each)+[0, 0, 0])[:dim]).tolist()
    return offset


def to_get_product(obj, n):
    if isinstance(obj, Mobject):
        return to_get_product(obj.get_center, n)
    if isinstance(obj, (int, float)):
        return obj*n
    if isinstance(obj, list):
        return list(each*n for each in obj)
    if isinstance(obj, tuple):
        return tuple(each*n for each in obj)


def to_get_offsets(obj, n=2):
    return [to_get_product(obj, (-1)**i/n) for i in range(1, -1, -1)]


def to_get_zlist(*lists, n=True):
    if isinstance(n, bool) and n == True:
        return list(np.array(lists, dtype=object).T.flat)
    elif isinstance(n, int):
        return to_get_zlist([lists]*n)
    elif isinstance(n, tuple):
        lists = list(lists)
        return [y for x in [copy.deepcopy(*lists) for i in range(n[0])] for y in x]
    else:
        return lists
