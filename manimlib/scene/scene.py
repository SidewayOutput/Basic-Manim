import inspect
import platform
import random as rrandom
import warnings
import itertools as it
import numpy as np
from numpy import arange, array, max, ndarray, random
from tqdm import tqdm as ProgressDisplay

from manimlib.animation.animation import Animation,  prepare_animation,_AnimationBuilder
from manimlib.animation.creation import DrawBorderThenFill, ShowCreation, ShowSubmobjectsOneByOne, Write
from manimlib.animation.fading import FadeIn, FadeOut
from manimlib.animation.growing import DiminishToCenter, GrowFromCenter  # ,
from manimlib.animation.transform import ApplyMethod, MoveToTarget,Transform
from manimlib.animation.update import  UpdateFromAlphaFunc
from manimlib.basic.basic_mobject import GroupedMobject, MobjectOrChars
from manimlib.camera.camera import Camera
from manimlib.camera.three_d_camera import ThreeDCamera
from manimlib.camera.moving_camera import MovingCamera
from manimlib.camera.multi_camera import MultiCamera
from manimlib.scene.window_scene import WindowScene

from manimlib.constants import DEFAULT_WAIT_TIME, FRAME_HEIGHT, FRAME_WIDTH, UP, DEGREES, RIGHT, DEFAULT_MOBJECT_TO_EDGE_BUFFER, ORIGIN,GREY,DOWN,LEFT,BLUE,GREEN,YELLOW,SMALL_BUFF,MED_SMALL_BUFF,BLACK,WHITE,FRAME_Y_RADIUS
from manimlib.container.container import Container
from manimlib.mobject.mobject import Group, Mobject
from manimlib.mobject.svg.tex_mobject import TextMobject,TexMobject
from manimlib.scene.scene_file_writer import SceneFileWriter
from manimlib.utils.iterables import list_update
from manimlib.utils.config_ops import digest_config
from manimlib.mobject.types.image_mobject import ImageMobjectFromCamera

from manimlib.mobject.types.vectorized_mobject import VGroup,VectorizedPoint
from manimlib.mobject.number_line import NumberLine
from manimlib.mobject.geometry import Line,Rectangle,RegularPolygon
from manimlib.mobject.functions import ParametricFunction
from manimlib.utils.bezier import interpolate
from manimlib.utils.simple_functions import fdiv
from manimlib.utils.space_ops import angle_of_vector
from manimlib.utils.color import color_gradient,invert_color

class Scene(WindowScene):
    CONFIG = {
        "camera_class": MultiCamera,
        # <--Camera3D
        "ambient_camera_rotation": None,
        "default_camera_orientation_kwargs": {
            "phi": 70 * DEGREES,
            "theta": -110 * DEGREES,
            # "phi": 90 * DEGREES,
            # "theta": 90 * DEGREES,
            # "gamma ": 0 * DEGREES,
        },
        "default_angled_camera_orientation_kwargs": {
            "phi": 70 * DEGREES,
            "theta": -135 * DEGREES,
        },
        # Camera3D
        # <--ZoomedCamera
        "zoomed_display_height": 3,
        "zoomed_display_width": 3,
        "zoomed_display_center": None,
        "zoomed_display_corner": UP + RIGHT,
        "zoomed_display_corner_buff": DEFAULT_MOBJECT_TO_EDGE_BUFFER,
        "zoomed_camera_config": {"default_frame_stroke_width": 2, "background_opacity": 1, },
        "zoomed_camera_image_mobject_config": {},
        "zoomed_camera_frame_starting_position": ORIGIN,
        "zoom_factor": 0.15,
        "image_frame_stroke_width": 3,
        "zoom_activated": False,


        # ZoomedCamera-->
        # <--GraphicScene
        "x_min": -1,
        "x_max": 10,
        "x_axis_width": 9,
        "x_tick_frequency": 1,
        "x_leftmost_tick": None,  # Change if different from x_min
        "x_labeled_nums": None,
        "x_axis_label": "$x$",
        "y_min": -1,
        "y_max": 10,
        "y_axis_height": 6,
        "y_tick_frequency": 1,
        "y_bottom_tick": None,  # Change if different from y_min
        "y_labeled_nums": None,
        "y_axis_label": "$y$",
        "axes_color": GREY,
        "graph_origin": 2.5 * DOWN + 4 * LEFT,
        "exclude_zero_label": True,
        "default_graph_colors": [BLUE, GREEN, YELLOW],
        "default_derivative_color": GREEN,
        "default_input_color": YELLOW,
        "default_riemann_start_color": BLUE,
        "default_riemann_end_color": GREEN,
        "area_opacity": 0.8,
        "num_rects": 50,
        #setup
        "default_graph_colors_cycle":it.cycle([BLUE, GREEN, YELLOW]),
        "left_T_label":VGroup(),
        "left_v_line":VGroup(),
        "right_T_label":VGroup(),
        "right_v_line":VGroup(),
        # GraphicScene-->
        "variable_point_label":"",
        "area":0.,
        "v_graph":None
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        self.init_vars()
        super().__init__(**kwargs)

    def get_moving_mobjects(self, *animations):

        moving_mobjects = WindowScene.get_moving_mobjects(self, *animations)
        all_moving_mobjects = self.camera.extract_mobject_family_members(
            moving_mobjects
        )
        movement_indicators = self.camera.get_mobjects_indicating_movement()
        for movement_indicator in movement_indicators:
            if movement_indicator in all_moving_mobjects:
                # When one of these is moving, the camera should
                # consider all mobjects to be moving
                return list_update(self.mobjects, moving_mobjects)
        # camera3d
        if self.camera_class == ThreeDCamera:
            camera_mobjects = self.camera.get_value_trackers()
            if any([cm in moving_mobjects for cm in camera_mobjects]):
                return self.mobjects
        # camera3d
        return moving_mobjects

    # <--Camera3D
    def set_camera_orientation(self, phi=None, theta=None, distance=None, gamma=None):
        if phi is not None:
            self.camera.set_phi(phi)
        if theta is not None:
            self.camera.set_theta(theta)
        if distance is not None:
            self.camera.set_distance(distance)
        if gamma is not None:
            self.camera.set_gamma(gamma)

    def begin_ambient_camera_rotation(self, rate=0.02):
        # TODO, use a ValueTracker for rate, so that it
        # can begin and end smoothly
        self.camera.theta_tracker.add_updater(
            lambda m, dt: m.increment_value(rate * dt)
        )
        self.add(self.camera.theta_tracker)

    def stop_ambient_camera_rotation(self):
        self.camera.theta_tracker.clear_updaters()
        self.remove(self.camera.theta_tracker)

    def move_camera(self,
                    phi=None,
                    theta=None,
                    distance=None,
                    gamma=None,
                    frame_center=None,
                    added_anims=[],
                    **kwargs):
        anims = []
        value_tracker_pairs = [
            (phi, self.camera.phi_tracker),
            (theta, self.camera.theta_tracker),
            (distance, self.camera.distance_tracker),
            (gamma, self.camera.gamma_tracker),
        ]
        for value, tracker in value_tracker_pairs:
            if value is not None:
                anims.append(
                    ApplyMethod(tracker.set_value, value, **kwargs)
                )
        if frame_center is not None:
            anims.append(ApplyMethod(
                self.camera.frame_center.move_to,
                frame_center
            ))

        self.play(*anims + added_anims)

    def add_fixed_orientation_mobjects(self, *mobjects, **kwargs):
        self.add(*mobjects)
        self.camera.add_fixed_orientation_mobjects(*mobjects, **kwargs)

    def add_fixed_in_frame_mobjects(self, *mobjects):
        self.add(*mobjects)
        self.camera.add_fixed_in_frame_mobjects(*mobjects)

    def remove_fixed_orientation_mobjects(self, *mobjects):
        self.camera.remove_fixed_orientation_mobjects(*mobjects)

    def remove_fixed_in_frame_mobjects(self, *mobjects):
        self.camera.remove_fixed_in_frame_mobjects(*mobjects)

    def set_to_default_angled_camera_orientation(self, **kwargs):
        config = dict(self.default_camera_orientation_kwargs)
        config.update(kwargs)
        self.set_camera_orientation(**config)
    # Camera3D-->
    # <--ZoomedCamera

    def setup(self):
        WindowScene.setup(self)
        # Initialize camera and display
        zoomed_camera = Camera(**self.zoomed_camera_config)
        zoomed_display = ImageMobjectFromCamera(
            zoomed_camera, **self.zoomed_camera_image_mobject_config
        )
        zoomed_display.add_display_frame()
        for mob in zoomed_camera.frame, zoomed_display:
            mob.stretch_to_fit_height(self.zoomed_display_height)
            mob.stretch_to_fit_width(self.zoomed_display_width)
        zoomed_camera.frame.scale(self.zoom_factor)

        # Position camera and display
        zoomed_camera.frame.move_to(self.zoomed_camera_frame_starting_position)
        if self.zoomed_display_center is not None:
            zoomed_display.move_to(self.zoomed_display_center)
        else:
            zoomed_display.to_corner(
                self.zoomed_display_corner,
                buff=self.zoomed_display_corner_buff
            )

        self.zoomed_camera = zoomed_camera
        self.zoomed_display = zoomed_display

    def activate_zooming(self, animate=False):
        self.zoom_activated = True
        #self.camera.frame.default_frame_stroke_width=2
        self.camera.add_image_mobject_from_camera(self.zoomed_display)
        if animate:
            self.play(self.get_zoom_in_animation())
            self.play(self.get_zoomed_display_pop_out_animation())
        self.add_foreground_mobjects(
            self.zoomed_camera.frame,
            self.zoomed_display,
        )

    def get_zoom_in_animation(self, run_time=2, **kwargs):
        frame = self.zoomed_camera.frame
        full_frame_height = self.camera.get_frame_height()
        full_frame_width = self.camera.get_frame_width()
        frame.save_state()
        frame.stretch_to_fit_width(full_frame_width)
        frame.stretch_to_fit_height(full_frame_height)
        frame.center()
        frame.set_stroke(width=0)
        return ApplyMethod(frame.restore, run_time=run_time, **kwargs)

    def get_zoomed_display_pop_out_animation(self, **kwargs):
        display = self.zoomed_display
        display.save_state(use_deepcopy=True)
        display.replace(self.zoomed_camera.frame, stretch=True)
        return ApplyMethod(display.restore)

    def get_zoom_factor(self):
        return fdiv(
            self.zoomed_camera.frame.get_height(),
            self.zoomed_display.get_height()
        )
    # ZoomedCamera-->
    #<--GraphicScene
    def setup_axes(self, animate=False):
        # TODO, once eoc is done, refactor this to be less redundant.
        x_num_range = float(self.x_max - self.x_min)
        self.space_unit_to_x = self.x_axis_width / x_num_range
        if self.x_labeled_nums is None:
            self.x_labeled_nums = []
        if self.x_leftmost_tick is None:
            self.x_leftmost_tick = self.x_min
        x_axis = NumberLine(
            x_min=self.x_min,
            x_max=self.x_max,
            unit_size=self.space_unit_to_x,
            tick_frequency=self.x_tick_frequency,
            leftmost_tick=self.x_leftmost_tick,
            numbers_with_elongated_ticks=self.x_labeled_nums,
            color=self.axes_color
        )
        x_axis.shift(self.graph_origin - x_axis.number_to_point(0))
        if len(self.x_labeled_nums) > 0:
            if self.exclude_zero_label:
                self.x_labeled_nums = [
                    x for x in self.x_labeled_nums if x != 0]
            x_axis.add_numbers(*self.x_labeled_nums)
        if self.x_axis_label:
            x_label = TextMobject(self.x_axis_label)
            x_label.next_to(
                x_axis.get_tick_marks(), UP + RIGHT,
                buff=SMALL_BUFF
            )
            x_label.shift_onto_screen()
            x_axis.add(x_label)
            self.x_axis_label_mob = x_label

        y_num_range = float(self.y_max - self.y_min)
        self.space_unit_to_y = self.y_axis_height / y_num_range

        if self.y_labeled_nums is None:
            self.y_labeled_nums = []
        if self.y_bottom_tick is None:
            self.y_bottom_tick = self.y_min
        y_axis = NumberLine(
            x_min=self.y_min,
            x_max=self.y_max,
            unit_size=self.space_unit_to_y,
            tick_frequency=self.y_tick_frequency,
            leftmost_tick=self.y_bottom_tick,
            numbers_with_elongated_ticks=self.y_labeled_nums,
            color=self.axes_color,
            line_to_number_vect=LEFT,
            label_direction=LEFT,
        )
        y_axis.shift(self.graph_origin - y_axis.number_to_point(0))
        y_axis.rotate(np.pi / 2, about_point=y_axis.number_to_point(0))
        if len(self.y_labeled_nums) > 0:
            if self.exclude_zero_label:
                self.y_labeled_nums = [
                    y for y in self.y_labeled_nums if y != 0]
            y_axis.add_numbers(*self.y_labeled_nums)
        if self.y_axis_label:
            y_label = TextMobject(self.y_axis_label)
            y_label.next_to(
                y_axis.get_corner(UP + RIGHT), UP + RIGHT,
                buff=SMALL_BUFF
            )
            y_label.shift_onto_screen()
            y_axis.add(y_label)
            self.y_axis_label_mob = y_label

        if animate:
            self.play(Write(VGroup(x_axis, y_axis)))
        else:
            self.add(x_axis, y_axis)
        self.x_axis, self.y_axis = self.axes = VGroup(x_axis, y_axis)
        self.default_graph_colors = it.cycle(self.default_graph_colors)
    def coords_to_point(self, x, y):
        assert(hasattr(self, "x_axis") and hasattr(self, "y_axis"))
        result = self.x_axis.number_to_point(x)[0] * RIGHT
        result += self.y_axis.number_to_point(y)[1] * UP
        return result

    def point_to_coords(self, point):
        return (self.x_axis.point_to_number(point),
                self.y_axis.point_to_number(point))

    def get_graph(
        self, func,
        color=None,
        x_min=None,
        x_max=None,
        **kwargs):
        if color is None:
            color = next(self.default_graph_colors_cycle)
        if x_min is None:
            x_min = self.x_min
        if x_max is None:
            x_max = self.x_max

        def parameterized_function(alpha):
            x = interpolate(x_min, x_max, alpha)
            y = func(x)
            if not np.isfinite(y):
                y = self.y_max
            return self.coords_to_point(x, y)

        graph = ParametricFunction(
            parameterized_function,
            color=color,
            **kwargs
        )
        graph.underlying_function = func
        return graph

    def input_to_graph_point(self, x, graph):
        return self.coords_to_point(x, graph.underlying_function(x))

    def angle_of_tangent(self, x, graph, dx=0.01):
        vect = self.input_to_graph_point(
            x + dx, graph) - self.input_to_graph_point(x, graph)
        return angle_of_vector(vect)

    def slope_of_tangent(self, *args, **kwargs):
        return np.tan(self.angle_of_tangent(*args, **kwargs))

    def get_derivative_graph(self, graph, dx=0.01, **kwargs):
        if "color" not in kwargs:
            kwargs["color"] = self.default_derivative_color

        def deriv(x):
            return self.slope_of_tangent(x, graph, dx) / self.space_unit_to_y
        return self.get_graph(deriv, **kwargs)

    def get_graph_label(
        self,
        graph,
        label="f(x)",
        x_val=None,
        direction=RIGHT,
        buff=MED_SMALL_BUFF,
        color=None,):
        label = TexMobject(label)
        color = color or graph.get_color()
        label.set_color(color)
        if x_val is None:
            # Search from right to left
            for x in np.linspace(self.x_max, self.x_min, 100):
                point = self.input_to_graph_point(x, graph)
                if point[1] < FRAME_Y_RADIUS:
                    break
            x_val = x
        label.next_to(
            self.input_to_graph_point(x_val, graph),
            direction,
            buff=buff
        )
        label.shift_onto_screen()
        return label

    def get_riemann_rectangles(
        self,
        graph,
        x_min=None,
        x_max=None,
        dx=0.1,
        input_sample_type="left",
        stroke_width=1,
        stroke_color=BLACK,
        fill_opacity=1,
        start_color=None,
        end_color=None,
        show_signed_area=True,
        width_scale_factor=1.001):
        x_min = x_min if x_min is not None else self.x_min
        x_max = x_max if x_max is not None else self.x_max
        if start_color is None:
            start_color = self.default_riemann_start_color
        if end_color is None:
            end_color = self.default_riemann_end_color
        rectangles = VGroup()
        x_range = np.arange(x_min, x_max, dx)
        colors = color_gradient([start_color, end_color], len(x_range))
        for x, color in zip(x_range, colors):
            if input_sample_type == "left":
                sample_input = x
            elif input_sample_type == "right":
                sample_input = x + dx
            elif input_sample_type == "center":
                sample_input = x + 0.5 * dx
            else:
                raise Exception("Invalid input sample type")
            graph_point = self.input_to_graph_point(sample_input, graph)
            points = VGroup(*list(map(VectorizedPoint, [
                self.coords_to_point(x, 0),
                self.coords_to_point(x + width_scale_factor * dx, 0),
                graph_point
            ])))

            rect = Rectangle()
            rect.replace(points, stretch=True)
            if graph_point[1] < self.graph_origin[1] and show_signed_area:
                fill_color = invert_color(color)
            else:
                fill_color = color
            rect.set_fill(fill_color, opacity=fill_opacity)
            rect.set_stroke(stroke_color, width=stroke_width)
            rectangles.add(rect)
        return rectangles

    def get_riemann_rectangles_list(
        self,
        graph,
        n_iterations,
        max_dx=0.5,
        power_base=2,
        stroke_width=1,
        **kwargs):
        return [
            self.get_riemann_rectangles(
                graph=graph,
                dx=float(max_dx) / (power_base**n),
                stroke_width=float(stroke_width) / (power_base**n),
                **kwargs
            )
            for n in range(n_iterations)
        ]

    def get_area(self, graph, t_min, t_max):
        numerator = max(t_max - t_min, 0.0001)
        dx = float(numerator) / self.num_rects
        return self.get_riemann_rectangles(
            graph,
            x_min=t_min,
            x_max=t_max,
            dx=dx,
            stroke_width=0,
        ).set_fill(opacity=self.area_opacity)

    def transform_between_riemann_rects(self, curr_rects, new_rects, **kwargs):
        transform_kwargs = {
            "run_time": 2,
            "lag_ratio": 0.5
        }
        added_anims = kwargs.get("added_anims", [])
        transform_kwargs.update(kwargs)
        curr_rects.align_submobjects(new_rects)
        x_coords = set()  # Keep track of new repetitions
        for rect in curr_rects:
            x = rect.get_center()[0]
            if x in x_coords:
                rect.set_fill(opacity=0)
            else:
                x_coords.add(x)
        self.play(
            Transform(curr_rects, new_rects, **transform_kwargs),
            *added_anims
        )

    def get_vertical_line_to_graph(
        self,
        x, graph,
        line_class=Line,
        **line_kwargs):
        if "color" not in line_kwargs:
            line_kwargs["color"] = graph.get_color()
        return line_class(
            self.coords_to_point(x, 0),
            self.input_to_graph_point(x, graph),
            **line_kwargs
        )

    def get_vertical_lines_to_graph(
        self, graph,
        x_min=None,
        x_max=None,
        num_lines=20,
        **kwargs):
        x_min = x_min or self.x_min
        x_max = x_max or self.x_max
        return VGroup(*[
            self.get_vertical_line_to_graph(x, graph, **kwargs)
            for x in np.linspace(x_min, x_max, num_lines)
        ])

    def get_secant_slope_group(
        self,
        x, graph,
        dx=None,
        dx_line_color=None,
        df_line_color=None,
        dx_label=None,
        df_label=None,
        include_secant_line=True,
        secant_line_color=None,
        secant_line_length=10,):
        """
        Resulting group is of the form VGroup(
            dx_line,
            df_line,
            dx_label, (if applicable)
            df_label, (if applicable)
            secant_line, (if applicable)
        )
        with attributes of those names.
        """
        kwargs = locals()
        kwargs.pop("self")
        group = VGroup()
        group.kwargs = kwargs

        dx = dx or float(self.x_max - self.x_min) / 10
        dx_line_color = dx_line_color or self.default_input_color
        df_line_color = df_line_color or graph.get_color()

        p1 = self.input_to_graph_point(x, graph)
        p2 = self.input_to_graph_point(x + dx, graph)
        interim_point = p2[0] * RIGHT + p1[1] * UP

        group.dx_line = Line(
            p1, interim_point,
            color=dx_line_color
        )
        group.df_line = Line(
            interim_point, p2,
            color=df_line_color
        )
        group.add(group.dx_line, group.df_line)

        labels = VGroup()
        if dx_label is not None:
            group.dx_label = TexMobject(dx_label)
            labels.add(group.dx_label)
            group.add(group.dx_label)
        if df_label is not None:
            group.df_label = TexMobject(df_label)
            labels.add(group.df_label)
            group.add(group.df_label)

        if len(labels) > 0:
            max_width = 0.8 * group.dx_line.get_width()
            max_height = 0.8 * group.df_line.get_height()
            if labels.get_width() > max_width:
                labels.set_width(max_width)
            if labels.get_height() > max_height:
                labels.set_height(max_height)

        if dx_label is not None:
            group.dx_label.next_to(
                group.dx_line,
                np.sign(dx) * DOWN,
                buff=group.dx_label.get_height() / 2
            )
            group.dx_label.set_color(group.dx_line.get_color())

        if df_label is not None:
            group.df_label.next_to(
                group.df_line,
                np.sign(dx) * RIGHT,
                buff=group.df_label.get_height() / 2
            )
            group.df_label.set_color(group.df_line.get_color())

        if include_secant_line:
            secant_line_color = secant_line_color or self.default_derivative_color
            group.secant_line = Line(p1, p2, color=secant_line_color)
            group.secant_line.scale_in_place(
                secant_line_length / group.secant_line.get_length()
            )
            group.add(group.secant_line)

        return group

    def add_T_label(self, x_val, side=RIGHT, label=None, color=WHITE, animated=False, **kwargs):
        triangle = RegularPolygon(n=3, start_angle=np.pi / 2)
        triangle.set_height(MED_SMALL_BUFF)
        triangle.move_to(self.coords_to_point(x_val, 0), UP)
        triangle.set_fill(color, 1)
        triangle.set_stroke(width=0)
        if label is None:
            T_label = TexMobject(self.variable_point_label, fill_color=color)
        else:
            T_label = TexMobject(label, fill_color=color)

        T_label.next_to(triangle, DOWN)
        v_line = self.get_vertical_line_to_graph(
            x_val, self.v_graph,
            color=YELLOW
        )

        if animated:
            self.play(
                DrawBorderThenFill(triangle),
                ShowCreation(v_line),
                Write(T_label, run_time=1),
                **kwargs
            )

        if np.all(side == LEFT):
            self.left_T_label_group = VGroup(T_label, triangle)
            self.left_v_line = v_line
            self.add(self.left_T_label_group, self.left_v_line)
        elif np.all(side == RIGHT):
            self.right_T_label_group = VGroup(T_label, triangle)
            self.right_v_line = v_line
            self.add(self.right_T_label_group, self.right_v_line)

    def get_animation_integral_bounds_change(
        self,
        graph,
        new_t_min,
        new_t_max,
        fade_close_to_origin=True,
        run_time=1.0):
        curr_t_min = self.x_axis.point_to_number(self.area.get_left())
        curr_t_max = self.x_axis.point_to_number(self.area.get_right())
        if new_t_min is None:
            new_t_min = curr_t_min
        if new_t_max is None:
            new_t_max = curr_t_max

        group = VGroup(self.area)
        group.add(self.left_v_line)
        group.add(self.left_T_label_group)
        group.add(self.right_v_line)
        group.add(self.right_T_label_group)

        def update_group(group, alpha):
            area, left_v_line, left_T_label, right_v_line, right_T_label = group
            t_min = interpolate(curr_t_min, new_t_min, alpha)
            t_max = interpolate(curr_t_max, new_t_max, alpha)
            new_area = self.get_area(graph, t_min, t_max)

            new_left_v_line = self.get_vertical_line_to_graph(
                t_min, graph
            )
            new_left_v_line.set_color(left_v_line.get_color())
            left_T_label.move_to(new_left_v_line.get_bottom(), UP)

            new_right_v_line = self.get_vertical_line_to_graph(
                t_max, graph
            )
            new_right_v_line.set_color(right_v_line.get_color())
            right_T_label.move_to(new_right_v_line.get_bottom(), UP)

            # Fade close to 0
            if fade_close_to_origin:
                if len(left_T_label) > 0:
                    left_T_label[0].set_fill(opacity=min(1, np.abs(t_min)))
                if len(right_T_label) > 0:
                    right_T_label[0].set_fill(opacity=min(1, np.abs(t_max)))

            Transform(area, new_area).update(1)
            Transform(left_v_line, new_left_v_line).update(1)
            Transform(right_v_line, new_right_v_line).update(1)
            return group

        return UpdateFromAlphaFunc(group, update_group, run_time=run_time)

    def animate_secant_slope_group_change(
        self, secant_slope_group,
        target_dx=None,
        target_x=None,
        run_time=3,
        added_anims=None,
        **anim_kwargs):
        if target_dx is None and target_x is None:
            raise Exception(
                "At least one of target_x and target_dx must not be None")
        if added_anims is None:
            added_anims = []

        start_dx = secant_slope_group.kwargs["dx"]
        start_x = secant_slope_group.kwargs["x"]
        if target_dx is None:
            target_dx = start_dx
        if target_x is None:
            target_x = start_x

        def update_func(group, alpha):
            dx = interpolate(start_dx, target_dx, alpha)
            x = interpolate(start_x, target_x, alpha)
            kwargs = dict(secant_slope_group.kwargs)
            kwargs["dx"] = dx
            kwargs["x"] = x
            new_group = self.get_secant_slope_group(**kwargs)
            group.become(new_group)
            return group

        self.play(
            UpdateFromAlphaFunc(
                secant_slope_group, update_func,
                run_time=run_time,
                **anim_kwargs
            ),
            *added_anims
        )
        secant_slope_group.kwargs["x"] = target_x
        secant_slope_group.kwargs["dx"] = target_dx

    #GraphicScene-->
    def init_vars(self):
        self.default_angled_camera_orientation_kwargs = vars(
            self)['default_angled_camera_orientation_kwargs']
        self.default_camera_orientation_kwargs = vars(
            self)['default_camera_orientation_kwargs']
        self.zoomed_camera_config=vars(self)['zoomed_camera_config']
        self.zoomed_camera_image_mobject_config=vars(self)['zoomed_camera_image_mobject_config']
        self.zoomed_display_height=vars(self)['zoomed_display_height']
        self.zoomed_display_width=vars(self)['zoomed_display_width']
        self.zoom_factor=vars(self)['zoom_factor']
        self.zoomed_camera_frame_starting_position=vars(self)['zoomed_camera_frame_starting_position']
        self.zoomed_display_center=vars(self)['zoomed_display_center']
        self.zoomed_display_corner=vars(self)['zoomed_display_corner']
        self.zoomed_display_corner_buff=vars(self)['zoomed_display_corner_buff']
        self.x_max=vars(self)['x_max']
        self.x_min=vars(self)['x_min']
        self.x_axis_width=vars(self)['x_axis_width']
        self.x_tick_frequency=vars(self)['x_tick_frequency']
        self.axes_color=vars(self)['axes_color']
        self.graph_origin=vars(self)['graph_origin']
        self.exclude_zero_label=vars(self)['exclude_zero_label']
        self.x_axis_label=vars(self)['x_axis_label']
        self.y_max=vars(self)['y_max']
        self.y_min=vars(self)['y_min']
        self.y_axis_height=vars(self)['y_axis_height']
        self.y_tick_frequency=vars(self)['y_tick_frequency']
        self.y_axis_label=vars(self)['y_axis_label']
        self.default_graph_colors_cycle=vars(self)['default_graph_colors_cycle']
        self.default_derivative_color=vars(self)['default_derivative_color']
        self.default_riemann_start_color=vars(self)['default_riemann_start_color']
        self.default_riemann_end_color=vars(self)['default_riemann_end_color']
        self.num_rects=vars(self)['num_rects']
        self.area_opacity=vars(self)['area_opacity']
        self.default_input_color=vars(self)['default_input_color']
        self.variable_point_label=vars(self)['variable_point_label']
        self.v_graph=vars(self)['v_graph']
        self.area=vars(self)['area']
        self.x_labeled_nums=vars(self)['x_labeled_nums']
        self.y_labeled_nums=vars(self)['y_labeled_nums']
        self.x_leftmost_tick=vars(self)['x_leftmost_tick']
        self.y_bottom_tick=vars(self)['y_bottom_tick']

class EndSceneEarlyException(Exception):
    pass
