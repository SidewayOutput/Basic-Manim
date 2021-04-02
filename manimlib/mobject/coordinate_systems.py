import numpy as np
import numbers

from manimlib.constants import *
from manimlib.mobject.functions import ParametricCurve, ParametricFunction
from manimlib.mobject.geometry import Arrow
from manimlib.mobject.geometry import Line
from manimlib.mobject.geometry import DashedLine
from manimlib.mobject.geometry import Rectangle
from manimlib.mobject.number_line import NumberLine
from manimlib.mobject.svg.tex_mobject import TexMobject
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.utils.config_ops import digest_config
from manimlib.utils.config_ops import merge_dicts_recursively
from manimlib.utils.simple_functions import binary_search
from manimlib.utils.space_ops import angle_of_vector

from manimlib.utils.space_ops import get_norm
from manimlib.utils.space_ops import rotate_vector

EPSILON = 1e-8
# TODO: There should be much more code reuse between Axes, NumberPlane and GraphScene


class CoordinateSystem():
    """
    Abstract class for Axes and NumberPlane
    """
    CONFIG = {
        "dimension": 2,
        "x_range": np.array([-FRAME_X_RADIUS, FRAME_X_RADIUS, 1.0]),
        "y_range": np.array([-4, 4, 1.0]),
        # "x_min": -FRAME_X_RADIUS,
        # "x_max": FRAME_X_RADIUS,
        # "y_min": -FRAME_Y_RADIUS,
        # "y_max": FRAME_Y_RADIUS,
        "width": None,
        "height": None,
        "num_sampled_graph_points_per_tick": 5,
    }

    def __zzinit__(self):
        x_range = self.minmax_to_range("x_min", "x_max", CoordinateSystem.x_range, kwargs)
        y_range = self.minmax_to_range("y_min", "y_max", y_range, kwargs)

    def minmax_to_range(self, min, max, step, range, kwargs):
        #kwargs=dict(kwargs)
        if range is None and min in kwargs and max in kwargs:
            range = [kwargs.pop(min,CoordinateSystem.CONFIG['x_range'][0]), kwargs.pop(max,CoordinateSystem.CONFIG['x_range'][1]),kwargs.pop(step,CoordinateSystem.CONFIG['x_range'][2]), ]
        return range

    def coords_to_point(self, *coords):
        raise Exception("Not implemented")

    def point_to_coords(self, point):
        raise Exception("Not implemented")

    def c2p(self, *coords):
        """Abbreviation for coords_to_point"""
        return self.coords_to_point(*coords)

    def p2c(self, point):
        """Abbreviation for point_to_coords"""
        return self.point_to_coords(point)

    def get_origin(self):
        return self.c2p(*[0] * self.dimension)

    def get_axes(self):
        raise Exception("Not implemented")

    def get_all_ranges(self):
        raise Exception("Not implemented")

    def get_axis(self, index):
        return self.get_axes()[index]

    def get_x_axis(self):
        return self.get_axis(0)

    def get_y_axis(self):
        return self.get_axis(1)

    def get_z_axis(self):
        return self.get_axis(2)

    def get_x_axis_label(self, label_tex, edge=RIGHT, direction=DL, **kwargs):
        return self.get_axis_label(
            label_tex, self.get_x_axis(),
            edge, direction, **kwargs
        )

    def get_y_axis_label(self, label_tex, edge=UP, direction=DR, **kwargs):
        return self.get_axis_label(
            label_tex, self.get_y_axis(),
            edge, direction, **kwargs
        )

    def get_axis_label(self, label_tex, axis, edge, direction, buff=MED_SMALL_BUFF):
        label = TexMobject(label_tex)
        label.next_to(
            axis.get_edge_center(edge), direction,
            buff=buff
        )
        label.shift_onto_screen(buff=MED_SMALL_BUFF)
        return label

    def get_axis_labels(self, x_label_tex="x", y_label_tex="y"):
        self.axis_labels = VGroup(
            self.get_x_axis_label(x_label_tex),
            self.get_y_axis_label(y_label_tex),
        )
        return self.axis_labels

    def get_line_from_axis_to_point(self, index, point,
                                    line_func=DashedLine,
                                    color=GREY_A,
                                    stroke_width=2):
        axis = self.get_axis(index)
        line = line_func(axis.get_projection(point), point)
        line.set_stroke(color, stroke_width)
        return line

    def get_v_line(self, point, **kwargs):
        return self.get_line_from_axis_to_point(0, point, **kwargs)

    def get_h_line(self, point, **kwargs):
        return self.get_line_from_axis_to_point(1, point, **kwargs)

    # Useful for graphing
    def get_graph(self, function, x_range=None, **kwargs):
        t_range = np.array(self.x_range, dtype=float)
        if x_range is not None:
            t_range[:len(x_range)] = x_range
        # For axes, the third coordinate of x_range indicates
        # tick frequency.  But for functions, it indicates a
        # sample frequency
        if x_range is None or len(x_range) < 3:
            t_range[2] /= self.num_sampled_graph_points_per_tick
        t_range[0] = kwargs.pop("x_min", t_range[0])
        t_range[1] = kwargs.pop("x_max", t_range[1])
        '''    
        x_min = kwargs.pop("x_min", self.x_min)
        x_max = kwargs.pop("x_max", self.x_max)
        '''
        graph = ParametricCurve(
            lambda t: self.c2p(t, function(t)),
            t_range=t_range,
            **kwargs
        )
        '''
        graph = ParametricFunction(
            lambda t: self.coords_to_point(t, function(t)),
            t_min=x_min,
            t_max=x_max,
            **kwargs
        )
        '''
        graph.underlying_function = function
        return graph

    def get_parametric_curve(self, function, **kwargs):
        dim = self.dimension
        graph = ParametricCurve(
            lambda t: self.coords_to_point(
                *function(t)[:dim]
            ),
            **kwargs
        )
        graph.underlying_function = function
        return graph

    def input_to_graph_point(self, x, graph):
        if hasattr(graph, "underlying_function"):
            return self.coords_to_point(x, graph.underlying_function(x))
        else:
            try:
                lower_bound = self.x_range[0],
                upper_bound = self.x_range[1],
            except:
                lower_bound = self.x_min,
                upper_bound = self.x_max,
            alpha = binary_search(
                function=lambda a: self.point_to_coords(
                    graph.point_from_proportion(a)
                )[0],
                target=x,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
            )
            if alpha is not None:
                return graph.point_from_proportion(alpha)
            else:
                return None

    def i2gp(self, x, graph):
        """
        Alias for input_to_graph_point
        """
        return self.input_to_graph_point(x, graph)

    def get_graph_label(self,
                        graph,
                        label="f(x)",
                        x=None,
                        direction=RIGHT,
                        buff=MED_SMALL_BUFF,
                        color=None):
        if isinstance(label, str):
            label = Tex(label)
        if color is None:
            label.match_color(graph)
        if x is None:
            # Searching from the right, find a point
            # whose y value is in bounds
            max_y = FRAME_Y_RADIUS - label.get_height()
            max_x = FRAME_X_RADIUS - label.get_width()
            for x0 in np.arange(*self.x_range)[::-1]:
                pt = self.i2gp(x0, graph)
                if abs(pt[0]) < max_x and abs(pt[1]) < max_y:
                    x = x0
                    break
            if x is None:
                x = self.x_range[1]

        point = self.input_to_graph_point(x, graph)
        angle = self.angle_of_tangent(x, graph)
        normal = rotate_vector(RIGHT, angle + 90 * DEGREES)
        if normal[1] < 0:
            normal *= -1
        label.next_to(point, normal, buff=buff)
        label.shift_onto_screen()
        return label

    def get_v_line_to_graph(self, x, graph, **kwargs):
        return self.get_v_line(self.i2gp(x, graph), **kwargs)

    def get_h_line_to_graph(self, x, graph, **kwargs):
        return self.get_h_line(self.i2gp(x, graph), **kwargs)

    # For calculus
    def angle_of_tangent(self, x, graph, dx=EPSILON):
        p0 = self.input_to_graph_point(x, graph)
        p1 = self.input_to_graph_point(x + dx, graph)
        return angle_of_vector(p1 - p0)

    def slope_of_tangent(self, x, graph, **kwargs):
        return np.tan(self.angle_of_tangent(x, graph, **kwargs))

    def get_tangent_line(self, x, graph, length=5, line_func=Line):
        line = line_func(LEFT, RIGHT)
        line.set_width(length)
        line.rotate(self.angle_of_tangent(x, graph))
        line.move_to(self.input_to_graph_point(x, graph))
        return line

    def get_riemann_rectangles(self,
                               graph,
                               x_range=None,
                               dx=None,
                               input_sample_type="left",
                               stroke_width=1,
                               stroke_color=BLACK,
                               fill_opacity=1,
                               colors=(BLUE, GREEN),
                               show_signed_area=True):
        if x_range is None:
            x_range = self.x_range[:2]
        if dx is None:
            dx = self.x_range[2]
        if len(x_range) < 3:
            x_range = [*x_range, dx]

        rects = []
        xs = np.arange(*x_range)
        for x0, x1 in zip(xs, xs[1:]):
            if input_sample_type == "left":
                sample = x0
            elif input_sample_type == "right":
                sample = x1
            elif input_sample_type == "center":
                sample = 0.5 * x0 + 0.5 * x1
            else:
                raise Exception("Invalid input sample type")
            height = get_norm(
                self.i2gp(sample, graph) - self.c2p(sample, 0)
            )
            rect = Rectangle(width=x1 - x0, height=height)
            rect.move_to(self.c2p(x0, 0), DL)
            rects.append(rect)
        result = VGroup(*rects)
        result.set_submobject_colors_by_gradient(*colors)
        result.set_style(
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            fill_opacity=fill_opacity,
        )
        return result

    def get_area_under_graph(self, graph, x_range, fill_color=BLUE, fill_opacity=1):
        # TODO
        pass


class Axes(VGroup, CoordinateSystem):
    CONFIG = {
        "axis_config": {
            "include_tip": True,
            "numbers_to_exclude": [0],
        },
        "number_line_config": {
            "color": LIGHT_GREY,
            "include_tip": True,
            "exclude_zero_from_default_numbers": True,
        },
        "x_axis_config": {},
        "y_axis_config": {
            "line_to_number_direction": LEFT,
            "label_direction": LEFT,
        },
        "center_point": ORIGIN,
        "height": None,  # FRAME_HEIGHT - 2,
        "width": None,  # FRAME_WIDTH - 2,
    }

    def __init__(self,
                 x_range=None,
                 y_range=None,
                 **kwargs):
        # super().__init__(**kwargs)
        x_range = self.minmax_to_range("x_min", "x_max","x_step", x_range, kwargs)
        y_range = self.minmax_to_range("y_min", "y_max","y_step", y_range, kwargs)
        VGroup.__init__(self, **kwargs)
        digest_config(self, kwargs)
        if x_range is not None:
            self.x_range[:len(x_range)] = x_range
        if y_range is not None:
            self.y_range[:len(y_range)] = y_range
        self.x_axis = self.create_axis(
            self.x_range, self.x_axis_config, self.width,
        )
        self.y_axis = self.create_axis(
            self.y_range, self.y_axis_config, self.height
        )
        '''
        self.x_axis = self.create_axis(
            self.x_min, self.x_max, self.x_axis_config
        )
        self.y_axis = self.create_axis(
            self.y_min, self.y_max, self.y_axis_config
        )
        '''
        self.y_axis.rotate(90 * DEGREES, about_point=ORIGIN)
        # Add as a separate group in case various other
        # mobjects are added to self, as for example in
        # NumberPlane below
        self.axes = VGroup(self.x_axis, self.y_axis)
        self.add(*self.axes)
        self.center()
        # self.shift(self.center_point)

    def create_axis(self, *args):
        if args[2] is not None and not isinstance(args[2], (int, float)):
            min_val, max_val, axis_config = args
            new_config = merge_dicts_recursively(
                self.number_line_config,
                {"x_min": min_val, "x_max": max_val},
                axis_config,
            )
            return NumberLine(**new_config)
        else:
            range_terms, axis_config, length = args
            new_config = merge_dicts_recursively(self.axis_config, axis_config)
            new_config["width"] = length
            axis = NumberLine(range_terms, **new_config)
            axis.shift(-axis.n2p(0))
            return axis

    def coords_to_point(self, *coords):
        origin = self.x_axis.number_to_point(0)
        result = origin.copy()  # np.array(origin)
        for axis, coord in zip(self.get_axes(), coords):
            result += (axis.number_to_point(coord) - origin)
        return result

    def c2p(self, *coords):
        return self.coords_to_point(*coords)

    def point_to_coords(self, point):
        return tuple([
            axis.point_to_number(point)
            for axis in self.get_axes()
        ])

    def p2c(self, point):
        return self.point_to_coords(point)

    def get_axes(self):
        return self.axes

    def get_all_ranges(self):
        return [self.x_range, self.y_range]

    def add_coordinate_labels(self,
                              x_values=None,
                              y_values=None,
                              **kwargs):
        axes = self.get_axes()
        self.coordinate_labels = VGroup()
        for axis, values in zip(axes, [x_values, y_values]):
            labels = axis.add_numbers(values, **kwargs)
            self.coordinate_labels.add(labels)
        return self.coordinate_labels

    def get_coordinate_labels(self, x_vals=None, y_vals=None):
        if x_vals is None:
            x_vals = []
        if y_vals is None:
            y_vals = []
        x_mobs = self.get_x_axis().get_number_mobjects(*x_vals)
        y_mobs = self.get_y_axis().get_number_mobjects(*y_vals)

        self.coordinate_labels = VGroup(x_mobs, y_mobs)
        return self.coordinate_labels

    def add_coordinates(self, x_vals=None, y_vals=None):
        self.add(self.get_coordinate_labels(x_vals, y_vals))
        return self


class ThreeDAxes(Axes):
    CONFIG = {
        "dimension": 3,
        "x_range": np.array([-5.0, 5.0, 1]),
        "y_range": np.array([-5.0, 5.0, 1]),
        # "x_min": -5.5,
        # "x_max": 5.5,
        # "y_min": -5.5,
        # "y_max": 5.5,
        "z_range": np.array([-4.0, 4.0, 1]),
        "z_axis_config": {},
        # "z_min": -3.5,
        # "z_max": 3.5,
        "z_normal": DOWN,
        "depth": None,
        "num_axis_pieces": 20,
        "light_source": 9 * DOWN + 7 * LEFT + 10 * OUT,
        "gloss": 0.5,
    }

    def __init__(self, x_range=None, y_range=None, z_range=None, **kwargs):
        x_range = self.minmax_to_range("x_min", "x_max", "x_step", x_range, kwargs)
        y_range = self.minmax_to_range("y_min", "y_max", "y_step", y_range, kwargs)
        z_range = self.minmax_to_range("z_min", "z_max", "z_step", z_range, kwargs)
        Axes.__init__(self, x_range, y_range, **kwargs)
        if z_range is not None:
            self.z_range[:len(z_range)] = z_range

        z_axis = self.create_axis(
            self.z_range,
            self.z_axis_config,
            self.depth,
        )
        z_axis.rotate(-PI / 2, UP, about_point=ORIGIN)
        #z_axis = self.z_axis = self.create_axis(self.z_min, self.z_max, self.z_axis_config)

        #z_axis.rotate(-np.pi / 2, UP, about_point=ORIGIN)
        z_axis.rotate(
            angle_of_vector(self.z_normal), OUT,
            about_point=ORIGIN
        )
        z_axis.shift(self.x_axis.n2p(0))
        self.axes.add(z_axis)
        self.add(z_axis)
        self.z_axis = z_axis

        for axis in self.axes:
            axis.insert_n_curves(self.num_axis_pieces - 1)

        self.add_3d_pieces()
        self.set_axis_shading()

    def add_3d_pieces(self):
        for axis in self.axes:
            axis.pieces = VGroup(
                *axis.get_pieces(self.num_axis_pieces)
            )
            axis.add(axis.pieces)
            axis.set_stroke(width=0, family=False)
            axis.set_shade_in_3d(True)

    def get_all_ranges(self):
        return [self.x_range, self.y_range, self.z_range]

    def set_axis_shading(self):
        def make_func(axis):
            vect = self.light_source
            return lambda: (
                axis.get_edge_center(-vect),
                axis.get_edge_center(vect),
            )
        for axis in self:
            for submob in axis.family_members_with_points():
                submob.get_gradient_start_and_end_points = make_func(axis)
                submob.get_unit_normal = lambda a: np.ones(3)
                submob.set_sheen(0.2)


class NumberPlane(Axes):
    CONFIG = {
        "axis_config": {
            "stroke_color": WHITE,
            "stroke_width": 2,
            "include_ticks": False,
            "include_tip": False,
            "line_to_number_buff": SMALL_BUFF,
            "line_to_number_direction": DL,
            "label_direction": DR,
            "number_scale_val": 0.5,
        },
        "y_axis_config": {
            "line_to_number_direction": DL,
            "label_direction": DR,
        },
        "background_line_style": {
            "stroke_color": BLUE_D,
            "stroke_width": 2,
            "stroke_opacity": 1,
        },
        "height": None,
        "width": None,
        # Defaults to a faded version of line_config
        "faded_line_style": None,
        "x_line_frequency": 1,
        "y_line_frequency": 1,
        "faded_line_ratio": 1,
        "make_smooth_after_applying_functions": True,
    }

    def __init__(self, x_range=None, y_range=None, **kwargs):
        digest_config(self, kwargs)
        kwargs["number_line_config"] = self.axis_config
        Axes.__init__(self,x_range, y_range, **kwargs)
        self.init_background_lines()

    def init_background_lines(self):
        if self.faded_line_style is None:
            style = dict(self.background_line_style)
            # For anything numerical, like stroke_width
            # and stroke_opacity, chop it in half
            for key in style:
                if isinstance(style[key], numbers.Number):
                    style[key] *= 0.5
            self.faded_line_style = style

        self.background_lines, self.faded_lines = self.get_lines()
        self.background_lines.set_style(**self.background_line_style)
        self.faded_lines.set_style(**self.faded_line_style)
        self.add_to_back(
            self.faded_lines,
            self.background_lines,
        )

    def get_lines(self):
        x_axis = self.get_x_axis()
        y_axis = self.get_y_axis()
        x_freq = self.x_line_frequency
        y_freq = self.y_line_frequency

        x_lines1, x_lines2 = self.get_lines_parallel_to_axis(
            x_axis, y_axis, x_freq,
            self.faded_line_ratio,
        )
        y_lines1, y_lines2 = self.get_lines_parallel_to_axis(
            y_axis, x_axis, y_freq,
            self.faded_line_ratio,
        )
        lines1 = VGroup(*x_lines1, *y_lines1)
        lines2 = VGroup(*x_lines2, *y_lines2)
        return lines1, lines2

    def get_lines_parallel_to_axis(self, axis1, axis2, freq, ratio):
        freq = axis1.x_step
        ratio = self.faded_line_ratio
        line = Line(axis1.get_start(), axis1.get_end())
        dense_freq = (1 + ratio)
        step = (1 / dense_freq) * freq

        lines1 = VGroup()
        lines2 = VGroup()
        #'''
        if axis2.x_min==-FRAME_X_RADIUS and axis2.x_max==FRAME_X_RADIUS:
           axis2x_min=int(axis2.x_min)
           axis2x_max=int(axis2.x_max)
        else:
           axis2x_min=axis2.x_min
           axis2x_max=axis2.x_max
        inputs = np.arange(axis2x_min, axis2x_max + step, step)
        for i, x in enumerate(inputs):
            new_line = line.copy()
            new_line.shift(axis2.n2p(x) - axis2.n2p(0))
            if i % (1 + ratio) == 0:
                lines1.add(new_line)
            else:
                lines2.add(new_line)
        '''
        ranges = (
            np.arange(0, axis2.x_max, step),
            np.arange(0, axis2.x_min, -step),
        )
        for inputs in ranges:
            for k, x in enumerate(inputs):
                new_line = line.copy()
                new_line.move_to(axis2.number_to_point(x))
                if k % (1 + ratio) == 0:
                    lines1.add(new_line)
                else:
                    lines2.add(new_line)
        '''
        return lines1, lines2

    def get_center_point(self):
        return self.coords_to_point(0, 0)

    def get_x_unit_size(self):
        return self.get_x_axis().get_unit_size()

    def get_y_unit_size(self):
        return self.get_x_axis().get_unit_size()

    def get_axes(self):
        return self.axes

    def get_vector(self, coords, **kwargs):
        kwargs["buff"] = 0
        return Arrow(self.c2p(0, 0), self.c2p(*coords), **kwargs)
        '''
        return Arrow(
            self.coords_to_point(0, 0),
            self.coords_to_point(*coords),
            **kwargs
        )
        '''
    def prepare_for_nonlinear_transform(self, num_inserted_curves=50):
        for mob in self.family_members_with_points():
            num_curves = mob.get_num_curves()
            if num_inserted_curves > num_curves:
                mob.insert_n_curves(
                    num_inserted_curves - num_curves
                )
            mob.make_smooth_after_applying_functions = True
        return self


class ComplexPlane(NumberPlane):
    CONFIG = {
        "color": BLUE,
        "line_frequency": 1,
    }

    def number_to_point(self, number):
        number = complex(number)
        return self.coords_to_point(number.real, number.imag)

    def n2p(self, number):
        return self.number_to_point(number)

    def point_to_number(self, point):
        x, y = self.point_to_coords(point)
        return complex(x, y)

    def p2n(self, point):
        return self.point_to_number(point)

    def get_default_coordinate_values(self):
        x_numbers = self.get_x_axis().get_tick_range()[1:]
        y_numbers = self.get_y_axis().get_tick_range()[1:]
        y_numbers = [complex(0, y) for y in y_numbers if y != 0]
        '''
        x_numbers = self.get_x_axis().default_numbers_to_display()
        y_numbers = self.get_y_axis().default_numbers_to_display()
        y_numbers = [
            complex(0, y) for y in y_numbers if y != 0
        ]
        '''
        return [*x_numbers, *y_numbers]

    def add_coordinate_labels(self, numbers=None, **kwargs):
        if numbers is None:
            numbers = self.get_default_coordinate_values()

        self.coordinate_labels = VGroup()
        for number in numbers:
            z = complex(number)
            if abs(z.imag) > abs(z.real):
                axis = self.get_y_axis()
                value = z.imag
                kwargs["unit"] = "i"
            else:
                axis = self.get_x_axis()
                value = z.real
            number_mob = axis.get_number_mobject(value, **kwargs)
            self.coordinate_labels.add(number_mob)
        self.add(self.coordinate_labels)
        return self
    def get_coordinate_labels(self, *numbers, **kwargs):
        if len(numbers) == 0:
            numbers = self.get_default_coordinate_values()

        self.coordinate_labels = VGroup()
        for number in numbers:
            z = complex(number)
            if abs(z.imag) > abs(z.real):
                axis = self.get_y_axis()
                value = z.imag
                kwargs = merge_dicts_recursively(
                    kwargs,
                    {"number_config": {"unit": "i"}},
                )
            else:
                axis = self.get_x_axis()
                value = z.real
            number_mob = axis.get_number_mobject(value, **kwargs)
            self.coordinate_labels.add(number_mob)
        return self.coordinate_labels

    def add_coordinates(self, *numbers):
        self.add(self.get_coordinate_labels(*numbers))
        return self
