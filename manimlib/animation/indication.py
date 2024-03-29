import numpy as np

from manimlib.constants import *
from manimlib.animation.animation import Animation
from manimlib.animation.movement import Homotopy
from manimlib.animation.composition import AnimationGroup
from manimlib.animation.composition import Succession
from manimlib.animation.creation import ShowCreation
from manimlib.animation.creation import ShowPartial
from manimlib.animation.fading import FadeOut
from manimlib.animation.transform import Transform
from manimlib.basic.basic_mobject import ListedVMobject
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.mobject.geometry import Circle
from manimlib.mobject.geometry import Dot
from manimlib.mobject.shape_matchers import SurroundingRectangle
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.geometry import Line
from manimlib.mobject.mobject import Group
from manimlib.utils.bezier import interpolate
from manimlib.utils.config_ops import digest_config
from manimlib.utils.rate_functions import there_and_back,there_and_back_with_pause
from manimlib.utils.rate_functions import wiggle


class FocusOn(Transform):
    CONFIG = {
        "opacity": 0.2,
        "color": GREY,
        "run_time": 2,
        "remover": True,
    }

    def __init__(self, focus_point, **kwargs):
        self.focus_point = focus_point
        # Initialize with blank mobject, while create_target
        # and create_starting_mobject handle the meat
        super().__init__(VMobject(), **kwargs)

    def create_target(self):
        little_dot = Dot(radius=0)
        little_dot.set_fill(self.color, opacity=self.opacity)
        little_dot.add_updater(
            lambda d: d.move_to(self.focus_point)
        )
        return little_dot

    def create_starting_mobject(self):
        return Dot(
            radius=FRAME_X_RADIUS + FRAME_Y_RADIUS,
            stroke_width=0,
            fill_color=self.color,
            fill_opacity=0,
        )


class Indicate(Transform):
    CONFIG = {
        "rate_func": there_and_back,
        "scale_factor": 1.2,
        "color": YELLOW,
        "lag_ratio":0,
    }


    def create_target(self):
        target = self.mobject.copy()
        target.scale_in_place(self.scale_factor)
        target.set_color(self.color)
        '''
        for each in target:
            w=each.get_stroke_width()
            if w<=5:
                each.set_stroke(width=6)
        '''
        return target


class Highlight(Transform):
    '''*mobjects, target_mobject=None, width=None, run_time=1\n
    +num:width; -num:run_time
    -'''
    CONFIG = {  
        #"run_time":0.6,
        "rate_func": lambda t:there_and_back_with_pause(t, pause_ratio=9. / 10),
        "scale_factor": 1,
        "color": YELLOW,
        "stroke_opacity":1,
        #"lag_ratio":0,
    }

    def __init__(self, *mobjects, target_mobject=None, width=None, run_time=1,**kwargs):
        while isinstance(mobjects[-1],(int,float)):
            if mobjects[-1]>=0:
                width=mobjects[-1]
                mobjects=mobjects[:-1]
            else:
                run_time=-mobjects[-1]
                mobjects=mobjects[:-1]
        self.width=width
        mobject=VGroup(*mobjects)
        super().__init__(mobject,  target_mobject=None, run_time=run_time, **kwargs)

    def create_target(self):
        target = self.mobject.copy()
        target.scale_in_place(self.scale_factor)
        target.set_color(self.color)
        
        for each in ListedVMobject(target):
            try: #?
                width=each.get_stroke_width()
                if self.width is not None:
                    each.set_stroke(width=self.width)
                elif width<=2:
                    each.set_stroke(width=4)
                elif width<=8:
                    each.set_stroke(width=width*(2.6-((width-2)/6)*0.6))
                else:
                    each.set_stroke(width=width*1.26)
            except:
                pass
        target.set_stroke(opacity=self.stroke_opacity)
        return target


class Flash(AnimationGroup):
    CONFIG = {
        "line_length": 0.2,
        "num_lines": 12,
        "flash_radius": 0.3,
        "line_stroke_width": 3,
        "run_time": 1,
    }

    def __init__(self, point, color=YELLOW, **kwargs):
        self.point = point
        self.color = color
        digest_config(self, kwargs)
        self.lines = self.create_lines()
        animations = self.create_line_anims()
        super().__init__(
            *animations,
            group=self.lines,
            **kwargs,
        )

    def create_lines(self):
        lines = VGroup()
        for angle in np.arange(0, TAU, TAU / self.num_lines):
            line = Line(ORIGIN, self.line_length * RIGHT)
            line.shift((self.flash_radius - self.line_length) * RIGHT)
            line.rotate(angle, about_point=ORIGIN)
            lines.add(line)
        lines.set_color(self.color)
        lines.set_stroke(width=3)
        lines.add_updater(lambda l: l.move_to(self.point))
        return lines

    def create_line_anims(self):
        return [
            ShowCreationThenDestruction(line)
            for line in self.lines
        ]


class CircleIndicate(Indicate):
    CONFIG = {
        "rate_func": there_and_back,
        "remover": True,
        "circle_config": {
            "color": YELLOW,
        },
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        circle = self.get_circle(mobject)
        super().__init__(circle, **kwargs)

    def get_circle(self, mobject):
        circle = Circle(**self.circle_config)
        circle.add_updater(lambda c: c.surround(mobject))
        return circle

    def interpolate_mobject(self, alpha):
        super().interpolate_mobject(alpha)
        self.mobject.set_stroke(opacity=alpha)


class ShowPassingFlash(ShowPartial):
    CONFIG = {
        "time_width": 0.1,
        "remover": True,
    }

    def get_bounds(self, alpha):
        tw = self.time_width
        upper = interpolate(0, 1 + tw, alpha)
        lower = upper - tw
        upper = min(upper, 1)
        lower = max(lower, 0)
        return (lower, upper)

    def finish(self):
        super().finish()
        for submob, start in self.get_all_families_zipped():
            submob.pointwise_become_partial(start, 0, 1)


class ShowCreationThenDestruction(ShowPassingFlash):
    CONFIG = {
        "time_width": 2.0,
        "run_time": 1,
    }


class ShowCreationThenFadeOut(Succession):
    CONFIG = {
        "remover": True,
    }

    def __init__(self, mobject, **kwargs):
        super().__init__(
            ShowCreation(mobject),
            FadeOut(mobject),
            **kwargs
        )


class AnimationOnSurroundingRectangle(AnimationGroup):
    CONFIG = {
        "surrounding_rectangle_config": {},
        # Function which takes in a rectangle, and spits
        # out some animation.  Could be some animation class,
        # could be something more
        "rect_animation": Animation
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        if "surrounding_rectangle_config" in kwargs:
            kwargs.pop("surrounding_rectangle_config")
        self.mobject_to_surround = mobject

        rect = self.get_rect()
        rect.add_updater(lambda r: r.move_to(mobject))

        super().__init__(
            self.rect_animation(rect, **kwargs),
        )

    def get_rect(self):
        return SurroundingRectangle(
            self.mobject_to_surround,
            **self.surrounding_rectangle_config
        )


class ShowPassingFlashAround(AnimationOnSurroundingRectangle):
    CONFIG = {
        "rect_animation": ShowPassingFlash
    }


class ShowCreationThenDestructionAround(AnimationOnSurroundingRectangle):
    CONFIG = {
        "rect_animation": ShowCreationThenDestruction
    }


class ShowCreationThenFadeAround(AnimationOnSurroundingRectangle):
    CONFIG = {
        "rect_animation": ShowCreationThenFadeOut
    }


class ApplyWave(Homotopy):
    CONFIG = {
        "direction": UP,
        "amplitude": 0.2,
        "run_time": 1,
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs, locals())
        left_x = mobject.get_left()[0]
        right_x = mobject.get_right()[0]
        vect = self.amplitude * self.direction

        def homotopy(x, y, z, t):
            alpha = (x - left_x) / (right_x - left_x)
            power = np.exp(2.0 * (alpha - 0.5))
            nudge = there_and_back(t**power)
            return np.array([x, y, z]) + nudge * vect

        super().__init__(homotopy, mobject, **kwargs)


class WiggleOutThenIn(Animation):
    CONFIG = {
        "scale_value": 1.1,
        "rotation_angle": 0.01 * TAU,
        "n_wiggles": 6,
        "run_time": 2,
        "scale_about_point": None,
        "rotate_about_point": None,
    }

    def get_scale_about_point(self):
        if self.scale_about_point is None:
            return self.mobject.get_center()

    def get_rotate_about_point(self):
        if self.rotate_about_point is None:
            return self.mobject.get_center()

    def interpolate_submobject(self, submobject, starting_sumobject, alpha):
        submobject.points[:, :] = starting_sumobject.points
        submobject.scale(
            interpolate(1, self.scale_value, there_and_back(alpha)),
            about_point=self.get_scale_about_point()
        )
        submobject.rotate(
            wiggle(alpha, self.n_wiggles) * self.rotation_angle,
            about_point=self.get_rotate_about_point()
        )


class TurnInsideOut(Transform):
    CONFIG = {
        "path_arc": TAU / 4,
    }

    def create_target(self):
        return self.mobject.copy().reverse_points()
