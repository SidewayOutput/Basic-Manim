import numpy as np
from manimlib.basic.basic_function import to_get_offset_lists, to_get_offsets
from manimlib.constants import BLUE, DEGREES, DL, DR, LEFT,  ORIGIN, OUT, RIGHT, UL, UR, WHITE
from manimlib.mobject.geometry import Line, Polygon
from manimlib.mobject.mobject import Mobject, Location
from manimlib.mobject.types.vectorized_mobject import VGroup, VMobject
from manimlib.utils.config_ops import digest_config, generate_args, generate_args_kwargs, merge_config_kwargs
from manimlib.utils.space_ops import compass_directions, rotate_vector


class GeomPoint(VGroup):
    '''
    [mobject_or_point], {from_offset},      {to_offset} -->default
    {length},           [mobject_or_point]
    '''
    CONFIG = {
        "color": BLUE,
        "stroke_width": 2,
    }

    def __init__(self, *args, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.add_element(*args, **kwargs)

    def add_element(self, *args, **kwargs):
        if not args or isinstance(args[0], (Mobject, list)):
            self.mobject_or_point, self.from_offset, self.to_offset, kwargs = \
                generate_args_kwargs(self, args, kwargs,
                                     ["mobject_or_point", "from_offset", "to_offset"],
                                     [ORIGIN, -0.1, 0.1]
                                     )
        elif isinstance(args[0], (int, float, tuple)):
            self.length, self.mobject_or_point = \
                generate_args(self, args,
                              [0.2, ORIGIN])
            if isinstance(self.length, tuple):
                self.length = list(self.length)
            self.from_offset, self.to_offset = to_get_offsets(self.length, 2)
            kwargs = merge_config_kwargs(self, kwargs,
                                         ["length", "mobject_or_point"]
                                         )
        else:
            self.mobject_or_point, self.from_offset, self.to_offset, kwargs = \
                generate_args_kwargs(self, (), kwargs,
                                     ["mobject_or_point", "from_offset", "to_offset"],
                                     [ORIGIN, -0.5, 0.5]
                                     )

        return [self.add(GeomLine(
            *list(zip(*to_get_offset_lists(
                self.mobject_or_point,
                [self.from_offset, self.to_offset])))[i],
            **kwargs))
            for i in range(len(Location(self.mobject_or_point)))]


class GeomPosition(GeomPoint):
    def __init__(self, mobject_or_point, **kwargs):
        GeomPoint.__init__(self, mobject_or_point, 1e-8, 1e-8, **kwargs)


class GeomLine(Line):
    '''
    xx length,     [point]
    [point],    [point] -->default
    [point],    (displacement)
    [point],    slope,              length
    [point],    [directioncosine],  length
    [point],    (directionvector),  length
    '''
    CONFIG = {
        "buff": 0,
        "path_arc": None,
    }

    def __init__(self, *args, **kwargs):
        self.normal_vector = OUT
        digest_config(self, kwargs)
        self.start = LEFT
        self.end = RIGHT

        if len(args) == 2:
            try:
                isinstance(args[0], (list))
            except:
                try:
                    isinstance(args[0], (int, float))
                except:
                    raise Exception("Not Supported")

            else:
                try:
                    isinstance(args[1], (list, tuple))
                except:
                    raise Exception(
                        "not form of two points or point displacement")
                else:
                    if isinstance(args[1], (list)):
                        self.start, self.end = args
                    if isinstance(args[1], (tuple)):
                        self.start, self.end = args[0], np.sum(
                            args, 0)
        if len(args) == 3:
            try:
                isinstance(args[0], (list))
            except:
                raise Exception("args[0]!=point")
            else:
                try:
                    isinstance(args[1], (int, float, list, tuple)) and isinstance(
                        args[2], (int, float))
                except:
                    raise Exception(
                        "not form of point slope length or point direction length")
                else:
                    if (isinstance(args[1], (int, float)) and isinstance(args[2], (int, float))):
                        hypotenuse = (1.+args[1]**2.)**0.5

                        self.start, self.end = args[0], args[0]+args[2]*np.array(
                            [1/hypotenuse, args[1]/hypotenuse, 0])

                    if isinstance(args[1], (list)):
                        direction = 1
                        for each in args[1]:
                            direction -= each**2
                        direction = args[1]+[0, direction, 0][len(args[1]):]
                        self.start, self.end = args[0], args[0] + \
                            args[2]*np.array(direction)
                    if isinstance(args[1], (tuple)):
                        self.start, self.end = args[0], args[0] + \
                            np.multiply(args[1], args[2]/get_norm(args[1]))
        Line.__init__(self, self.start, self.end, **kwargs)


class GeomPolyline(Polygon):
    CONFIG = {
        "color": WHITE,
        "mark_paths_closed": False,
        "close_new_points": False,
    }

    def __init__(self, *vertices, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.set_points_as_corners(
            [*vertices]
        )


class GeomPolygon(Polygon):
    CONFIG = {
        "color": BLUE,
    }

    def __init__(self, *vertices, **kwargs):

        self.mobject_or_point = None
        VMobject.__init__(self, **kwargs)
        self.set_points_as_corners(
            [*vertices, vertices[0]]
        )
        if self.mobject_or_point != None:
            self.move_to(Location(self.mobject_or_point))


class GeomRegularPolygon(GeomPolygon):
    '''
    {number},start_angle,radius,[center],"point/edge",[normal_vector]
    '''
    CONFIG = {
        "start_angle": None,
    }

    def __init__(self, n=6, *args, **kwargs):
        self.args_name = \
            ["mobject_or_point", "radius", "start_angle", "element", "normal_vector"]
        self.args = \
            [ORIGIN, 1, None, "point", "OUT"]
        self.mobject_or_point, self.radius, self.start_angle, self.element, self.normal_vector = \
            generate_args(self, args, self.args)
        kwargs = merge_config_kwargs(self, kwargs, self.args_name)

        self.mobject_or_point = Location(self.mobject_or_point)
        if self.element == "point":
            if self.start_angle is None:
                if n % 2 == 0:
                    self.start_angle = 0
                else:
                    self.start_angle = 90 * DEGREES
            start_vect = rotate_vector(self.radius*RIGHT, self.start_angle)
        vertices = np.add(compass_directions(n, start_vect),
                          np.repeat([self.mobject_or_point], n, axis=0))
        GeomPolygon.__init__(self, *vertices, **kwargs)


class GeomRectangle(GeomPolygon):
    '''
    {height,width},[center],start_angle,"edge/point",[normal_vector]
    '''
    CONFIG = {
        "color": WHITE,
        "mark_paths_closed": True,
        "close_new_points": True,
    }

    def __init__(self, *args, **kwargs):
        self.args_name = \
            ["height", "width", "mobject_or_point",
                "start_angle", "element", "normal_vector"]
        self.args = \
            [2, 4, ORIGIN, None, "edge", "IN"]
        [self.height, self.width, self.mobject_or_point, self.start_angle, self.element, self.normal_vector] = \
            generate_args(self, args, self.args)
        kwargs = merge_config_kwargs(self, kwargs, self.args_name)
        self.mobject_or_point = Location(self.mobject_or_point)
        ul, ur, dr, dl = np.add(np.multiply(
            (UL, UR, DR, DL), [self.width/2, self.height/2, 0]), self.mobject_or_point)
        GeomPolygon.__init__(self, ul, ur, dr, dl, **kwargs)


class GeomSquare(GeomRectangle):
    '''
    {side_length},[center],start_angle,"edge/point",[normal_vector]
    '''

    def __init__(self, *args, **kwargs):
        self.args_name = \
            ["side_length", "mobject_or_point",
                "start_angle", "element", "normal_vector"]
        self.args = \
            [2, ORIGIN,  None, "edge", "IN"]
        [self.side_length, self.mobject_or_point, self.start_angle, self.element, self.normal_vector] = \
            generate_args(self, args, self.args)
        kwargs = merge_config_kwargs(self, kwargs, self.args_name)

        GeomRectangle.__init__(
            self,
            self.side_length,
            self.side_length,
            *args[1:],
            **kwargs
        )


class GeomArrow(GeomLine):
    CONFIG = {
        "stroke_width": 6,
        "buff": 0,
        "max_tip_length_to_length_ratio": 0.25,
        "max_stroke_width_to_length_ratio": 5,
        "preserve_tip_size_when_scaling": True,
    }

    def __init__(self, *args, **kwargs):
        GeomLine.__init__(self, *args, **kwargs)
        # TODO, should this be affected when
        # Arrow.set_stroke is called?
        self.initial_stroke_width = self.stroke_width
        self.add_tip(**kwargs)
        self.set_stroke_width_from_length()

    def scale(self, factor, **kwargs):
        if self.get_length() == 0:
            return self

        has_tip = self.has_tip()
        has_start_tip = self.has_start_tip()
        if has_tip or has_start_tip:
            old_tips = self.pop_tips()

        VMobject.scale(self, factor, **kwargs)
        self.set_stroke_width_from_length()

        # So horribly confusing, must redo
        if has_tip:
            self.add_tip()
            old_tips[0].points[:, :] = self.tip.points
            self.remove(self.tip)
            self.tip = old_tips[0]
            self.add(self.tip)
        if has_start_tip:
            self.add_tip(at_start=True)
            old_tips[1].points[:, :] = self.start_tip.points
            self.remove(self.start_tip)
            self.start_tip = old_tips[1]
            self.add(self.start_tip)
        return self

    def get_normal_vector(self):
        p0, p1, p2 = self.tip.get_start_anchors()[:3]
        return normalize(np.cross(p2 - p1, p1 - p0))

    def reset_normal_vector(self):
        self.normal_vector = self.get_normal_vector()
        return self

    def get_default_tip_length(self):
        max_ratio = self.max_tip_length_to_length_ratio
        return min(
            self.tip_length,
            max_ratio * self.get_length(),
        )

    def set_stroke_width_from_length(self):
        max_ratio = self.max_stroke_width_to_length_ratio
        self.set_stroke(
            width=min(
                self.initial_stroke_width,
                max_ratio * self.get_length(),
            ),
            family=False,
        )
        return self

    # TODO, should this be the default for everything?
    def copy(self):
        return self.deepcopy()

class GeomElbow(VMobject):
    CONFIG = {
        "width": 0.2,
        "angle": 0,
        "side":1,
        "position":ORIGIN
    }

    def __init__(self, **kwargs):
        VMobject.__init__(self, **kwargs)
        side=[self.side,0,0]
        self.set_points_as_corners([UP, UP + side, side])
        self.set_width(self.width, about_point=ORIGIN)
        self.rotate(self.angle, about_point=ORIGIN)
