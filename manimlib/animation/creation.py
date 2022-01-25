from manimlib.animation.animation import Animation
from manimlib.animation.composition import Succession
from manimlib.mobject.types.vectorized_mobject import VMobject,VGroup
from manimlib.mobject.mobject import Mobject, Group
from manimlib.mobject.svg.tex_mobject import TextMobject,TexMobject
from manimlib.utils.bezier import integer_interpolate
from manimlib.utils.config_ops import digest_config
from manimlib.utils.rate_functions import linear
from manimlib.utils.rate_functions import double_smooth
from manimlib.utils.rate_functions import smooth

import numpy as np
import itertools as it


class ShowPartial(Animation):
    """
    Abstract class for ShowCreation and ShowPassingFlash
    """

    def interpolate_submobject(self, submob, start_submob, alpha):
        #print(self.r_flag,self.r_color,self.r_width,self.r_opacity)
        if self.r_flag and (self.r_color is not None or self.r_width is not None or self.r_opacity is not None):
            self.mobject.set_stroke(self.r_color,self.r_width,self.r_opacity)
            self.r_flag=False
        if 1 and self.s_flag:
            for each in self.mobject:
                if each.get_stroke_width()==0 and each.get_fill_color() is None:
                    each.set_stroke(width=4)
                if each.get_stroke_opacity()==0 and each.get_fill_color() is None:
                    each.set_stroke(opacity=1)
            #self.s_flag=False
        submob.pointwise_become_partial(
            start_submob, *self.get_bounds(alpha)
        )

    def get_bounds(self, alpha):
        raise Exception("Not Implemented")


class ShowCreation(ShowPartial):
    CONFIG = {
        "lag_ratio": 1,
    }

    def get_bounds(self, alpha):
        return (0, alpha)

class Show(ShowCreation):

    '''*mobjects,\n
    +num:run_time; callable:rate_func
    -'''
    CONFIG = {
        #"run_time": 0.5,
        "rate_func": linear,
        "lag_ratio": 0,
        "r_color":None,
        "r_width":None,
        "r_opacity":None,
        "r_flag":True,
    }

    def __init__(self, *mobjects,  **kwargs):
        while not isinstance(mobjects[-1],(Mobject,VMobject,Group,VGroup)):
            if isinstance(mobjects[-1],(int,float)):
                self.run_time=mobjects[-1]
                mobjects=mobjects[:-1]
            elif callable(mobjects[-1]):
                self.rate_func=mobjects[-1]
                mobjects=mobjects[:-1]
        if len(mobjects)==1:
            mobject=mobjects[0]
        else:
            mobject=VGroup(*mobjects)
        assert(isinstance(mobject, Mobject))
        digest_config(self, kwargs)
        self.mobject = mobject
class zShow(ShowCreation):

    '''*mobjects,\n
    +num:run_time; callable:rate_func
    -'''
    CONFIG = {
        "run_time": 1,
        "rate_func": linear,
        "lag_ratio": 1,
    }

    def __init__(self, *mobjects,  **kwargs):
        while not isinstance(mobjects[-1],(Mobject,VMobject,Group,VGroup)):
            if isinstance(mobjects[-1],(int,float)):
                self.run_time=mobjects[-1]
                mobjects=mobjects[:-1]
            elif callable(mobjects[-1]):
                self.rate_func=mobjects[-1]
                mobjects=mobjects[:-1]
        mobject=Group(*mobjects)
        assert(isinstance(mobject, Mobject))
        digest_config(self, kwargs)
        self.mobject = mobject
        mobject.fade(0)
        if isinstance(mobject, VMobject):
            mobject.set_stroke(width=0)
            mobject.set_fill(opacity=0)
    def create_starting_mobject(self):
        start = super().create_starting_mobject()
        start.fade(0)
        if isinstance(start, VMobject):
            start.set_stroke(width=0)
            start.set_fill(opacity=0)
        return start


class Uncreate(ShowCreation):
    CONFIG = {
        "rate_func": lambda t: smooth(1 - t),
        "remover": True
    }


class DrawBorderThenFill(Animation):
    CONFIG = {
        "run_time": 2,
        "rate_func": double_smooth,
        "stroke_width": 2,
        "stroke_color": None,
        "draw_border_animation_config": {},
        "fill_animation_config": {},
    }

    def __init__(self, vmobject, **kwargs):
        self.validity_of_vmobject_input(vmobject)
        super().__init__(vmobject, **kwargs)

    def begin(self):
        self.outline = self.get_outline()
        super().begin()

    def get_outline(self):
        outline = self.mobject.copy()
        outline.set_fill(opacity=0)
        for sm in outline.family_members_with_points():
            sm.set_stroke(
                color=self.get_stroke_color(sm),
                width=self.stroke_width
            )
        return outline

    def get_stroke_color(self, vmobject):
        if self.stroke_color:
            return self.stroke_color
        elif vmobject.get_stroke_width() > 0:
            return vmobject.get_stroke_color()
        return vmobject.get_color()

    def get_all_mobjects(self):
        return [*super().get_all_mobjects(), self.outline]

    def interpolate_submobject(self, submob, start, outline, alpha):
        index, subalpha = integer_interpolate(0, 2, alpha)
        if index == 0:
            submob.pointwise_become_partial(
                outline, 0, subalpha
            )
            submob.match_style(outline)
        else:
            submob.interpolate(outline, start, subalpha)


class Write(DrawBorderThenFill):
    CONFIG = {
        # To be figured out in
        # set_default_config_from_lengths
        "run_time": None,
        "lag_ratio": None,
        "rate_func": linear,
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        self.set_default_config_from_length(mobject)
        super().__init__(mobject, **kwargs)

    def set_default_config_from_length(self, mobject):
        length = len(mobject.family_members_with_points())
        if self.run_time is None:
            if length < 15:
                self.run_time = 1
            else:
                self.run_time = 2
        if self.lag_ratio is None:
            self.lag_ratio = min(4.0 / length, 0.2)


class ShowIncreasingSubsets(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
        "int_func": np.floor,
    }

    def __init__(self, group, **kwargs):
        self.all_submobs = list(group.submobjects)
        super().__init__(group, **kwargs)

    def interpolate_mobject(self, alpha):
        n_submobs = len(self.all_submobs)
        index = int(self.int_func(alpha * n_submobs))
        self.update_submobject_list(index)

    def update_submobject_list(self, index):
        self.mobject.submobjects = self.all_submobs[:index]


class ShowSubmobjectsOneByOne(ShowIncreasingSubsets):
    def __init__(self, group, **kwargs):
        new_group = Group(*group)
        super().__init__(new_group, **kwargs)

    def update_submobject_list(self, index):
        # N = len(self.all_submobs)
        if index == 0:
            self.mobject.submobjects = []
        else:
            self.mobject.submobjects = self.all_submobs[index - 1]


# TODO, this is broken...
class AddTextWordByWord(Succession):
    CONFIG = {
        # If given a value for run_time, it will
        # override the time_per_char
        "run_time": None,
        "time_per_char": 0.06,
    }

    def __init__(self, text_mobject, **kwargs):
        digest_config(self, kwargs)
        tpc = self.time_per_char
        anims = it.chain(*[
            [
                ShowIncreasingSubsets(word, run_time=tpc * len(word)),
                Animation(word, run_time=0.005 * len(word)**1.5),
            ]
            for word in text_mobject
        ])
        super().__init__(*anims, **kwargs)
