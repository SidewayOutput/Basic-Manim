import numpy as np

from manimlib.animation.animation import AGroup
from manimlib.animation.creation import ShowSubmobjectsOneByOne
from manimlib.animation.composition import AnimationGroup
from manimlib.animation.fading import FadeIn
from manimlib.animation.growing import GrowFromCenter
from manimlib.basic.basic_animation import FadeInThenIndicate, FadeoutSuccession, ShowPassingFlashAndIndicateThenFadeOut

from manimlib.basic.basic_compound import ShowSubmobjectsOneByOneAndFadeInThenIndicateThenFadeOut
from manimlib.basic.basic_mobject import ImageMobjectGroup, MobjectOrChars
from manimlib.constants import DOWN, GREEN, PoweredBy, Project, UP, WHITE, YELLOW
from manimlib.mobject.geometry import Circle, RegularPolygon, Square, Triangle
from manimlib.mobject.mobject import Group, Mobject
from manimlib.mobject.shape_matchers import Underline
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.utils.rate_functions import linear


class StartScreens01(AnimationGroup):
    '''
    mobjs_1, mobjs_1_scale, mobjs_1_interval, mobjs_1_rate_func, title_1, title_1_color, title_1_scale, title_1_position, title_1_shadow, title_1_indicate_scale_factor, title_1_extra = screen01 + ["", 2, 0.5, linear, "", "#0808B8", 2, [DOWN], [2, slice(0, 3, 2)], 1.2, ""][len(screen01):]

    mobjs_2, mobjs_2_scale, mobjs_2_interval, mobjs_2_rate_func, title_2, title_2_color, title_2_scale, title_2_position, title_2_shadow, title_2_indicate_scale_factor, title_2_extra = screen02 + ["", 2, 0.5, linear, "", "#0808B8", 1.2, [DOWN], [2, slice(1, 4, 2)], "", [slice(1, 2), WHITE, [-2.5, 0, 0]]][len(screen02):]

    [title, subtitle, filename, reference, warning, mobjes_3_run_time] = screen03 + [[], [], [], [], [], 3][len(screen03):]

    [title, title_color, title_scale, title_position] = title + ["", WHITE, 1, [UP]][len(title):]

    [subtitle, subtitle_color, subtitle_scale, subtitle_position] = subtitle + ["", WHITE, 1, [0, 0, 0]][len(subtitle):]

    [filename, filename_color, filename_scale, filename_position] = filename + ["", WHITE, 1, [0, -2.9, 0]][len(filename):]

    [reference, reference_color, reference_scale, reference_position] = reference + ["", YELLOW, 1, [0, -3.3, 0]][len(reference):]

    [warning, warning_color, warning_scale, warning_position] = warning + ["", YELLOW, 1, [0, -3.7, 0]
            ][len(warning):]
    '''

    def __init__(self, screen01=[], screen02=[], screen03=[], lag_ratio=1, **kwargs):
        mobjs_1, mobjs_1_scale, mobjs_1_interval, mobjs_1_rate_func, \
            title_1, title_1_color, title_1_scale, title_1_position, title_1_shadow, \
            title_1_indicate_scale_factor, title_1_extra = screen01 + \
            ["", 2, 0.5, linear, "", "#0808B8", 2, [DOWN], [2, slice(0, 3, 2)],
             1.2, ""][len(screen01):]
        mobjs_2, mobjs_2_scale, mobjs_2_interval, mobjs_2_rate_func, \
            title_2, title_2_color, title_2_scale, title_2_position, title_2_shadow, \
            title_2_indicate_scale_factor, title_2_extra = screen02 + \
            ["", 2, 0.5, linear, "", "#0808B8", 1.2, [DOWN], [2, slice(1, 4, 2)],
             "", [slice(1, 2), WHITE, [-2.5, 0, 0]]][len(screen02):]
        [title, subtitle, filename, reference, warning, mobjes_3_run_time] =\
            screen03 + [[], [], [], [], [], 3][len(screen03):]
        [title, title_color, title_scale, title_position] = title + \
            ["", WHITE, 1, [UP]][len(title):]
        [subtitle, subtitle_color, subtitle_scale, subtitle_position] = subtitle + \
            ["", WHITE, 1, [0, 0, 0]][len(subtitle):]
        [filename, filename_color, filename_scale, filename_position] = filename + \
            ["", WHITE, 1, [0, -2.9, 0]][len(filename):]
        [reference, reference_color, reference_scale, reference_position] = reference + \
            ["", YELLOW, 1, [0, -3.3, 0]][len(reference):]
        [warning, warning_color, warning_scale, warning_position] = warning + \
            ["", YELLOW, 1, [0, -3.7, 0]
             ][len(warning):]

        startscreens = AGroup()
        if mobjs_1 != None:
            if mobjs_1 == "":
                try:
                    mobjs_1 = ImageMobjectGroup(np.char.mod('%01d', range(
                        0, 10)), "sidewayoutput\\sidewayoutput2020yt")
                except:
                    mobjs_1 = ImageMobjectGroup(np.char.mod(
                        '%01d', range(9, -1, -1)), "001\\")
            if title_1 == "":
                title_1 = PoweredBy
            title_1 = MobjectOrChars(title_1)
            title_1.set_color(title_1_color).scale(title_1_scale).align_on_border(
                *title_1_position).add_shadow_mobjects(title_1_shadow[0], title_1[title_1_shadow[1]])
            if title_1_extra != "":
                title_1[title_1_extra[0]].set_color(
                    title_1_extra[1]).shift(title_1_extra[2])
            if title_1_indicate_scale_factor == "":
                title_width = mobjs_1.get_width()
                title_1_indicate_scale_factor = (title_width-0.5)/title_width
            startscreens.add(ShowSubmobjectsOneByOneAndFadeInThenIndicateThenFadeOut(
                mobjs_1.scale(mobjs_1_scale),
                title_1,
                indicate_scale_factor=title_1_indicate_scale_factor,
                show_rate_func=mobjs_1_rate_func,
                run_time=mobjs_1_interval*(len(mobjs_1)),
                **kwargs))
        if mobjs_2 != None:
            if mobjs_2 == "":
                strs = TextMobject(r"\textspA{%s}" % Project)
                mobjs_2 = Group(
                    Circle(fill_opacity=0.75),
                    RegularPolygon(fill_opacity=0.75),
                    Triangle(color=GREEN, fill_opacity=0.75),
                    Square(fill_opacity=0.75),
                    strs.set_color("#FFFFFF"),
                    strs.copy().set_color("#F8F8F8").scale(1.3),
                    strs.copy().set_color("#F8F8B8").scale(1.6),
                    strs.copy().set_color("#B8B8B8").scale(1.6),
                    strs.copy().set_color("#8888B8").scale(1.6),
                    strs.copy().set_color("#6868B8").scale(1.6),
                    strs.copy().set_color("#4848B8").scale(1.6),
                    strs.copy().set_color("#2828B8").scale(1.6),
                    strs.copy().set_color("#0808B8").scale(1.6),
                )
            if title_2 == "":
                title_2 = (r"{\tiny{\emph{Powered by}:}}\\ ", *PoweredBy)
            title_2 = MobjectOrChars(title_2)
            title_2.set_color(title_2_color).scale(title_2_scale).align_on_border(
                *title_2_position).add_shadow_mobjects(title_2_shadow[0], title_2[title_2_shadow[1]])
            if title_2_extra != "":
                title_2[title_2_extra[0]].set_color(
                    title_2_extra[1]).shift(title_2_extra[2])
            if title_2_indicate_scale_factor == "":
                title_width = mobjs_2.get_width()
                title_2_indicate_scale_factor = (title_width-0.5)/title_width
            startscreens.add(ShowSubmobjectsOneByOneAndFadeInThenIndicateThenFadeOut(
                mobjs_2.scale(mobjs_2_scale),
                title_2,
                indicate_scale_factor=title_2_indicate_scale_factor,
                show_rate_func=mobjs_2_rate_func,
                run_time=mobjs_2_interval*(len(mobjs_2)),
                **kwargs))
        if title != None or subtitle != None:
            mobjs_3 = [Group(), "", ""]
            if title != None:
                txt_title = TextMobject(title).scale(title_scale)
                if txt_title.get_width() > 14:
                    txt_title.stretch_to_fit_width(14)
                mobjs_3[1] = txt_title.set_color(
                    title_color).to_edge(*title_position)
                mobjs_3[0].add(mobjs_3[1])
            if subtitle != None:
                mobjs_3[0].add(TextMobject(subtitle).set_color(subtitle_color).scale(
                    subtitle_scale).shift(subtitle_position))
            if filename != None and filename != "":
                if reference == None or reference == "":
                    filename_position = reference_position
                mobjs_3[0].add(TextMobject(filename).set_color(
                    filename_color).scale(filename_scale).shift(filename_position))
            if reference != None and reference != "":
                txt_reference = TextMobject(reference).scale(reference_scale)
                if txt_reference.get_width() > 14:
                    txt_reference.stretch_to_fit_width(14)
                mobjs_3[0].add(txt_reference.set_color(
                    reference_color).shift(reference_position))
            if warning != None and warning != "":
                txt_warning = TextMobject(warning).scale(
                    warning_scale)  # height=0.3
                if txt_warning.get_width() > 14:
                    txt_warning.stretch_to_fit_width(14)
                mobjs_3[2] = txt_warning.set_color(
                    warning_color).shift(warning_position)
            animations = AGroup()
            if len(mobjs_3[0]) > 0:
                animations.add(
                    FadeIn(mobjs_3[0], run_time=0.5, scale_factor=1, color=None))
            if len(mobjs_3[1]) > 0:
                animations.add(GrowFromCenter(Underline(mobjs_3[1])))
            if len(mobjs_3[2]) > 0:
                animations.add(FadeInThenIndicate(
                    mobjs_3[2], run_time=1, scale_factor=1, color=None))
            startscreens.add(FadeoutSuccession(AnimationGroup(
                *animations, run_time=mobjes_3_run_time), run_time=0.05))
        super().__init__(AnimationGroup(*startscreens, lag_ratio=1), **kwargs)


class EndScreen01(AnimationGroup):
    def __init__(self, chars=r"\textrm{\textbf{THANKS\ FOR\ WATCHING}}", **kwargs):
        super().__init__(
            ShowPassingFlashAndIndicateThenFadeOut(
                MobjectOrChars(chars), **kwargs),
        )

class PlayMobject(AnimationGroup):
    def __init__(self, mobjs="", mobj=None, scale=1,shift=[0,0,0], **kwargs):
        if mobjs != None:
            if mobjs == "":
                try:
                    mobjs = ImageMobjectGroup(np.char.mod('%01d', range(
                        0, 10)), "sidewayoutput\\sidewayoutput2020yt")
                except:
                    mobjs = ImageMobjectGroup(np.char.mod(
                        '%01d', range(9, -1, -1)), "001\\")
        #if mobj!=None:
        t=mobj.get_critical_point([-1,1,0])-mobjs.get_critical_point([-1,1,0])
        mobjs.shift(t).shift(shift)
        super().__init__(
            ShowSubmobjectsOneByOne(mobjs.add(
                Mobject()).scale(scale),**kwargs),
        )
