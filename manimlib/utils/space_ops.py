from functools import reduce

import numpy as np
import math
from manimlib.constants import OUT
from manimlib.constants import PI
from manimlib.constants import RIGHT
from manimlib.constants import TAU
from manimlib.utils.iterables import adjacent_pairs
from manimlib.utils.simple_functions import fdiv


def get_norm(vect):
    return sum([x**2 for x in vect])**0.5


# Quaternions
# TODO, implement quaternion type


def quaternion_mult(*quats):
    if len(quats) == 0:
        return [1, 0, 0, 0]
    result = quats[0]
    for next_quat in quats[1:]:
        w1, x1, y1, z1 = result
        w2, x2, y2, z2 = next_quat
        result = [
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2,
            w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2,
        ]
    return result

def zquaternion_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2,
        w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2,
    ])


def quaternion_from_angle_axis(angle, axis, axis_normalized=False):
    if not axis_normalized:
        axis = normalize(axis)
    return [math.cos(angle / 2), *(math.sin(angle / 2) * axis)]

def zquaternion_from_angle_axis(angle, axis):
    return np.append(
        np.cos(angle / 2),
        np.sin(angle / 2) * normalize(axis)
    )


def angle_axis_from_quaternion(quaternion):
    axis = normalize(
        quaternion[1:],
        fall_back=np.array([1, 0, 0])
    )
    angle = 2 * np.arccos(quaternion[0])
    if angle > TAU / 2:
        angle = TAU - angle
    return angle, axis


def quaternion_conjugate(quaternion):
    result = np.array(quaternion)
    result[1:] *= -1
    return result


def rotate_vector(vector, angle, axis=OUT):
    if len(vector) == 2:
        # Use complex numbers...because why not
        z = complex(*vector) * np.exp(complex(0, angle))
        return np.array([z.real, z.imag])
    elif len(vector) == 3:
        # Use quaternions...because why not
        quat = quaternion_from_angle_axis(angle, axis)
        quat_inv = quaternion_conjugate(quat)
        product = reduce(
            quaternion_mult,
            [quat, np.append(0, vector), quat_inv]
        )
        return product[1:]
    else:
        raise Exception("vector must be of dimension 2 or 3")


def thick_diagonal(dim, thickness=2):
    row_indices = np.arange(dim).repeat(dim).reshape((dim, dim))
    col_indices = np.transpose(row_indices)
    return (np.abs(row_indices - col_indices) < thickness).astype('uint8')

def rotation_matrix_transpose_from_quaternion(quat):
    quat_inv = quaternion_conjugate(quat)
    return [
        quaternion_mult(quat, [0, *basis], quat_inv)[1:]
        for basis in [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ]
    ]

def rotation_matrix_transpose(angle, axis):
    if axis[0] == 0 and axis[1] == 0:
        # axis = [0, 0, z] case is common enough it's worth
        # having a shortcut
        sgn = 1 if axis[2] > 0 else -1
        cos_a = math.cos(angle)
        sin_a = math.sin(angle) * sgn
        return [
            [cos_a, sin_a, 0],
            [-sin_a, cos_a, 0],
            [0, 0, 1],
        ]
    quat = quaternion_from_angle_axis(angle, axis)
    return rotation_matrix_transpose_from_quaternion(quat)

def rotation_matrix(angle, axis):
    """
    Rotation in R^3 about a specified axis of rotation.
    """
    about_z = rotation_about_z(angle)
    z_to_axis = z_to_vector(axis)
    axis_to_z = np.linalg.inv(z_to_axis)
    return reduce(np.dot, [z_to_axis, about_z, axis_to_z])


def rotation_about_z(angle):
    c, s= np.cos(angle), np.sin(angle)
    return [[c, -s, 0],
            [s,  c, 0],
            [0,  0, 1]]


def z_to_vector(vector):
    """
    Returns some matrix in SO(3) which takes the z-axis to the
    (normalized) vector provided as an argument
    """
    norm = get_norm(vector)
    if norm == 0:
        return np.identity(3)
    v = np.array(vector) / norm
    phi = np.arccos(v[2])
    if any(v[:2]):
        # projection of vector to unit circle
        axis_proj = v[:2] / get_norm(v[:2])
        theta = np.arccos(axis_proj[0])
        if axis_proj[1] < 0:
            theta = -theta
    else:
        theta = 0
    phi_down = np.array([
        [np.cos(phi), 0, np.sin(phi)],
        [0, 1, 0],
        [-np.sin(phi), 0, np.cos(phi)]
    ])
    return np.dot(rotation_about_z(theta), phi_down)


def angle_between(v1, v2):
    return np.arccos(np.dot(
        v1 / get_norm(v1),
        v2 / get_norm(v2)
    ))


def angle_of_vector(vector):
    """
    Returns polar coordinate theta when vector is project on xy plane
    """
    z = complex(*vector[:2])
    if z == 0:
        return 0
    return np.angle(complex(*vector[:2]))


def angle_between_vectors(v1, v2):
    """
    Returns the angle between two 3D vectors.
    This angle will always be btw 0 and pi
    """
    return np.arccos(fdiv(
        np.dot(v1, v2),
        get_norm(v1) * get_norm(v2)
    ))

def spaceangle_between(v1, v2, d=1):
    [x1, y1, z1], [x2, y2, z2] = v1, v2
    #[n1,n2,n3]=get_unit_normal(v1, v2)
    if d:
     [n1,n2,n3] = [0,0,1]
    else:
        [n1,n2,n3] = [0,0,-1]
    radangle= np.arctan2(np.dot([n1,n2,n3],np.cross([x1,y1,z1],[x2,y2,z2])),np.dot([x1,y1,z1],[x2,y2,z2]))
    if radangle<0:
        radangle=TAU+radangle
    return radangle
    '''
    [x1, y1, z1], [x2, y2, z2] = v1, v2
    dot = np.dot(v1,v2)#x1*x2 + y1*y2 + z1*z2    #between [x1, y1, z1] and [x2, y2, z2]
    lenSq1 = x1*x1 + y1*y1 + z1*z1
    lenSq2 = x2*x2 + y2*y2 + z2*z2
    return np.arccos(dot/np.sqrt(lenSq1 * lenSq2))
    '''


def project_along_vector(point, vector):
    matrix = np.identity(3) - np.outer(vector, vector)
    return np.dot(point, matrix.T)


def normalize(vect, fall_back=None):
    norm = get_norm(vect)
    if norm > 0:
        return np.array(vect) / norm
    else:
        if fall_back is not None:
            return fall_back
        else:
            return np.zeros(len(vect))


def cross(v1, v2):
    return np.array([
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ])


def get_unit_normal(v1, v2):
    return normalize(cross(v1, v2))


###


def compass_directions(n=4, start_vect=RIGHT):
    angle = TAU / n
    return np.array([
        rotate_vector(start_vect, k * angle)
        for k in range(n)
    ])


def complex_to_R3(complex_num):
    return np.array((complex_num.real, complex_num.imag, 0))


def R3_to_complex(point):
    return complex(*point[:2])


def complex_func_to_R3_func(complex_func):
    return lambda p: complex_to_R3(complex_func(R3_to_complex(p)))


def center_of_mass(points):
    points = [np.array(point).astype("float") for point in points]
    return sum(points) / len(points)


def midpoint(point1, point2):
    return center_of_mass([point1, point2])


def line_intersection(line1, line2):
    """
    return intersection point of two lines,
    each defined with a pair of vectors determining
    the end points
    """
    if not isinstance(line1,(list,tuple)):
        line1=line1.pts()
    if not isinstance(line2,(list,tuple)):
        line2=line2.pts()
    x_diff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    y_diff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(x_diff, y_diff)
    if div == 0:
        raise Exception("Lines do not intersect")
    d = (det(*line1), det(*line2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div
    return np.array([x, y, 0])


def get_winding_number(points):
    total_angle = 0
    for p1, p2 in adjacent_pairs(points):
        d_angle = angle_of_vector(p2) - angle_of_vector(p1)
        d_angle = ((d_angle + PI) % TAU) - PI
        total_angle += d_angle
    return total_angle / TAU


# Linear interpolation variants from bezier.py

def interpolate(start, end, alpha):
    return (1 - alpha) * start + alpha * end
    #(end-stat)*alpha+start

def interslice(start, end, count, first=0,last=1):
    '''(n)'''
    return np.multiply(end-start,np.transpose([np.linspace(first, last,count)]))+start
    #[interpolate(points[:-1], points[1:], a) for a in np.linspace(0, 1, nppcc)]
    #np.multiply.outer(np.transpose([3,2,4]),np.linspace(3, 1,3)).transpose()
    #np.multiply.outer(np.transpose(a),np.linspace(3, 1,3)).transpose()+a
def integer_interpolate(start, end, alpha):
    """
    alpha is a float between 0 and 1.  This returns
    an integer between start and end (inclusive) representing
    appropriate interpolation between them, along with a
    "residue" representing a new proportion between the
    returned integer and the next one of the
    list.

    For example, if start=0, end=10, alpha=0.46, This
    would return (4, 0.6).
    """
    if alpha >= 1:
        return (end - 1, 1.0)
    if alpha <= 0:
        return (start, 0)
    value = int(interpolate(start, end, alpha))
    residue = ((end - start) * alpha) % 1
    return (value, residue)


def mid(start, end):
    return (start + end) / 2.0


def inverse_interpolate(start, end, value):
    return np.true_divide(value - start, end - start)


def match_interpolate(new_start, new_end, old_start, old_end, old_value):
    return interpolate(
        new_start, new_end,
        inverse_interpolate(old_start, old_end, old_value)
    )

