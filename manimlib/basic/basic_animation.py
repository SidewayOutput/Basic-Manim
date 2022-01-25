from manimlib.animation.animation import AGroup, Animation
from manimlib.animation.composition import AnimationGroup, Succession, OneByOne,  AnimByAnim
from manimlib.animation.creation import ShowCreation, Show, Write
from manimlib.animation.fading import FadeIn, FadeOut
from manimlib.animation.growing import GrowFromCenter
from manimlib.animation.indication import Indicate, ShowPassingFlash, Highlight
from manimlib.animation.transform import ApplyMethod, ApplyFunction, Restore, Transform
from manimlib.constants import YELLOW,PINK
from manimlib.mobject.mobject import Mobject, Group
from manimlib.mobject.geometry import Square
from manimlib.mobject.svg.tex_mobject import TextMobject, TexMobject
from manimlib.mobject.types.vectorized_mobject import VGroup, VMobject
from manimlib.utils.config_ops import merge_config_kwargs, digest_config
from manimlib.utils.rate_functions import rush_into, there_and_back, linear, there_and_back_with_pause,shorten,pulse,step,linear_pulse,linear_with_delay
from manimlib.basic.basic_function import funz

class FadeInThenIndicate(Succession):
    CONFIG = {
        "rate_func": there_and_back,
        "scale_factor": 1.2,
        "color": YELLOW,
        # "remover": False,
    }

    def __init__(self, mobject, **kwargs):
        super().__init__(
            FadeIn(mobject, **kwargs),
            Indicate(mobject, **kwargs),
            **kwargs
        )


class ShowCreationThenIndicate(Succession):
    CONFIG = {
        "rate_func": there_and_back,
        "scale_factor": 1,
        "color": YELLOW,
        # "remover": False,
    }

    def __init__(self, mobject, run_time=1, indicate=True, **kwargs):
        kwargs = merge_config_kwargs(self, kwargs, self.CONFIG)
        if not indicate:
            kwargs['color'] = mobject.get_color()
        super().__init__(
            ShowCreation(mobject, run_time=run_time*0.95),
            Indicate(mobject, run_time=run_time*0.05, **kwargs),
            run_time=run_time, **kwargs
        )


class FadeInThenFadeOut(Succession):
    CONFIG = {
        # "rate_func": there_and_back,
        # "scale_factor": 1.2,
        # "color": YELLOW,
        # "remover": True,
        # "lag_ration": 0.1,
    }

    def __init__(self, mobject, run_time=1, ratio_array=[0.01, 0.5, 0.5], fadeout_func=rush_into, **kwargs):
        animations = AGroup(
            FadeIn(mobject, run_time=ratio_array[0]*run_time),
            #Indicate(mobject, run_time=ratio_array[1]*run_time,  **kwargs),
            FadeOut(mobject, run_time=ratio_array[2]*run_time, rate_func=fadeout_func))
        [animations.remove(animations[i])
         for i in range(len(ratio_array)) if ratio_array[i] == 0]
        super().__init__(*animations, **kwargs)


class FadeInThenIndicateThenFadeOut(Succession):
    CONFIG = {
        "rate_func": there_and_back,
        "scale_factor": 1.2,
        "color": YELLOW,
        # "remover": True,
        # "lag_ration": 0.1,
    }

    def __init__(self, mobject, run_time=1, ratio_array=[0.01, 0.5, 0.5], fadeout_func=rush_into, **kwargs):
        animations = AGroup(
            FadeIn(mobject, run_time=ratio_array[0]*run_time),
            Indicate(mobject, run_time=ratio_array[1]*run_time,  **kwargs),
            FadeOut(mobject, run_time=ratio_array[2]*run_time, rate_func=fadeout_func))
        [animations.remove(animations[i])
         for i in range(len(ratio_array)) if ratio_array[i] == 0]
        super().__init__(*animations, **kwargs)


class RateFunc(Succession):
    def __init__(self, *animations, rate=linear_with_delay, **kwargs):
        super().__init__(*animations,rate_function=rate,**kwargs)


class FadeoutSuccession(Succession):
    def __init__(self, *animations, run_time=0.1, **kwargs):
        anims = AGroup(
            #FadeIn(animation.mobject, run_time=0.01),
            *animations,
            # IndicateThenFadeOut(
            #    animation.mobject, run_time=0.1, scale_factor=1, color=None, ratio_array=[0.05, 0.95], rate_func=fadeout_func)  # ,ratio_array=[1.2, 1.1, 0.05]
            DFadeOut(AnimationGroup(*animations).mobject,
                     run_time=run_time, **kwargs)
        )
        super().__init__(*anims)


class FadeinSuccession(Succession):
    def __init__(self, animation, run_time=0.1, ratio_array=[1, 1, 1], fadeout_func=rush_into, **kwargs):
        animations = AGroup(
            FadeIn(animation.mobject, rate_func=linear, run_time=run_time),

            #ApplyMethod(VGroup(*animation.mobject[:]).set_stroke,{"opacity":1}, run_time=0),
            animation,
            # IndicateThenFadeOut(
            #    animation.mobject, run_time=1, scale_factor=1, color=None, ratio_array=[0.95, 0.05], rate_func=fadeout_func)  # ,ratio_array=[1.2, 1.1, 0.05]

        )
        super().__init__(*animations, **kwargs)


class IndicateThenFadeOut(Succession):
    CONFIG = {
        "rate_func": there_and_back,
        "scale_factor": 1.2,
        "color": YELLOW,
        "remover": False,
        "lag_ration": 0.1,
    }

    def __init__(self, mobject, run_time=1, ratio_array=[0.5, 0.5], **kwargs):
        super().__init__(
            Indicate(mobject, run_time=run_time *
                     ratio_array[0], **kwargs),  # 0.5
            FadeOut(mobject, run_time=run_time * \
                    ratio_array[1], **kwargs),  # 0.03
            **kwargs
        )


class ShowCreationThenFadeOut(Succession):
    CONFIG = {
        # "rate_func": there_and_back,
        # "scale_factor": 1.2,
        # "color": YELLOW,
        "remover": False,
        "lag_ration": 0.1,
    }

    def __init__(self, mobject, run_time=5, ratio_array=[0.95, 0.05], **kwargs):
        super().__init__(
            ShowCreation(mobject, run_time=run_time *
                         ratio_array[0], **kwargs),  # run_time *
            # ratio_array[0], **kwargs),  # 0.5
            FadeOut(mobject, run_time=run_time * \
                    ratio_array[1], **kwargs),  # 0.03
            **kwargs
        )


class DFadeOut(Succession):
    def __init__(self, *mobjects,run_time = 0.001, **kwargs):
        if isinstance(mobjects[-1], (int, float)):
            run_time = mobjects[-1]
            mobject = Group(*mobjects[:-1])
        else:
            
            mobject = Group(*mobjects)
        super().__init__(
            FadeOut(mobject, run_time=run_time*0.9),
            FadeOut(mobject, run_time=run_time*0.1),
            run_time=run_time,**kwargs)


class XFadeOut(Succession):
    def __init__(self, mobject, **kwargs):
        super().__init__(
            FadeoutSuccession(Animation(mobject, run_time=0.1), run_time=0.1),
            # FadeoutSuccession(Animation(mobject,run_time=0.1),run_time=0.1),

            **kwargs)


class ShowPassingFlashAndIndicateThenFadeOut(AnimationGroup):
    CONFIG = {
        "time_width": 0.2,
        "scale_factor": 1.2,
        "color": YELLOW,
    }

    def __init__(self, mobject, **kwargs):
        self.mobject_color = YELLOW
        self.total_run_time = 4
        self.total_lag_ratio = 1
        kwargs = merge_config_kwargs(self, kwargs)

        super().__init__(
            ShowPassingFlash(mobject.set_color(
                self.mobject_color), **kwargs),
            IndicateThenFadeOut(mobject.copy(), **kwargs),
            run_time=self.total_run_time, lag_ratio=self.total_lag_ratio)


class ShowCreations(AnimationGroup):
    def __init__(self, mobjects, **kwargs):
        animations = AGroup()
        [animations.add(ShowCreation(each, **kwargs)) for each in mobjects]
        super().__init__(
            AnimationGroup(*animations))


class Freeze(Animation):
    def __init__(self, run_time=1, **kwargs):
        Animation.__init__(self, Mobject(), run_time=run_time, **kwargs)


class Delay(OneByOne):
    '''*animations, time=1, group=False, time_wait=None,\n
    *+num:time, -num:time_wait, bool:group
    -'''
    CONFIG = {
        "delay": True,
        "time":1,
    }

    def __init__(self, *animations, time=None, group=False, time_wait=None, **kwargs):
        merge_config_kwargs(self, kwargs)
        while isinstance(animations[-1], (int, float, bool)):
            if isinstance(animations[-1], bool):
                if int(animations[-1]) == 1:
                    group = True
                animations = animations[:-1]
            elif isinstance(animations[-1], (int, float)):
                if animations[-1] > 0:
                    time = animations[-1]
                elif animations[-1] < 0:
                    time_wait = -animations[-1]
                animations = animations[:-1]
        if group:
            animations = [AnimationGroup(*animations, **kwargs)]
        anims = AGroup(*animations)
        if time is not None:
            self.time=time
        if self.delay:
            anims.add_to_back(Freeze(self.time))
        else:
            anims.add(Freeze(self.time))
        if time_wait is not None:
            anims.add(Freeze(time_wait))
        super().__init__(*anims, **kwargs)


class Wait(Delay):
    '''*animations, time=1, group=False, time_wait=None,\n
    *+num:time, bool:group
    -'''
    CONFIG = {
        "delay": False,
    }


class Pause(Wait):
    '''
    *animations, time=0.33, group=False,
    '''
    CONFIG = {
        "time": 1./3,
    }

    def __zinit__(self, *animations, time=0.33, group=False, **kwargs):
        super().__init__(*animations, time=time, group=group, **kwargs)


class Shock(Wait):
    CONFIG = {
        "time": 0.1,
    }
    def __zinit__(self, *animations, time=0.001, group=False, **kwargs):
        super().__init__(*animations, time=time, group=group, **kwargs)


class GrowTitle(GrowFromCenter):
    def __init__(self, str, shift=[0, 3.6, 0], **kwargs):
        GrowFromCenter.__init__(self, TextMobject(
            r"\titleA{"+str+"}").shift(shift))


class Display(AnimationGroup):
    '''*mobjects, run_time=0.001, lag_ratio=1,\n
    num:run_time
    -'''

    def __init__(self, *mobjects, run_time=0.05, lag_ratio=1, **kwargs):
        while isinstance(mobjects[-1], (int, float)):
            run_time = run_time
            mobjects = mobjects[:-1]
        animations = AGroup()
        vmobjs = VGroup()
        mobjs = Group()
        for each in mobjects:
            if isinstance(each, (VMobject)):
                vmobjs.add(each)
            else:
                mobjs.add(each)
        if len(mobjs) > 0:
            animations.add(Show(mobjs, run_time=run_time, **kwargs))
        if len(vmobjs) > 0:
            animations.add(Write(vmobjs, run_time=run_time, **kwargs))
        super().__init__(
            AnimationGroup(*animations, run_time=run_time, lag_ratio=lag_ratio, **kwargs))


class Remove(Animation):
    CONFIG = {
        "remover": True,
    }
    def __init__(self, *mobjects, run_time=0.001, lag_ratio=1, **kwargs):
        if isinstance(mobjects[-1], (int, float)):
            run_time = run_time
            mobjects = mobjects[:-1]
        super().__init__(Group(*mobjects), run_time=run_time, **kwargs)

class Add(Animation):
    def __init__(self, *mobjects, run_time=0.001, lag_ratio=1, **kwargs):
        if isinstance(mobjects[-1], (int, float)):
            run_time = run_time
            mobjects = mobjects[:-1]
        super().__init__(Group(*mobjects), run_time=run_time, **kwargs)


class AnimateStroke(AnimByAnim):
    '''mobject, color=None, width=None, opacity=None, scale_factor=1, run_time=1, highlight=1, func=None, rate_func=linear, pause_ratio=4./5, f_color=None, f_width=None,\n
    color->-num:run_time
    -'''
    CONFIG = {
        # "run_time": 1,
        # "rate_func": lambda t:there_and_back_with_pause(t, pause_ratio=9.9 / 10),
        # "scale_factor": 1,
        # "color": YELLOW,
        # "stroke_opacity":1
    }

    def __init__(self, mobject, color=YELLOW, width=10, opacity=None, scale_factor=1, run_time=1, highlight=1, func=None, rate_func=linear, pause_ratio=4./5, f_color=None, f_width=None, f_opacity=None, lag_ratio=1, copy=False, fadeout=None,offset=4, ratio=[0.95, 0.05], name="mobject", **kwargs):
        #for each in ["zrate_func", "scale_factor", "color", "stroke_opacity", "width"]:
        #    try:
        #        if locals()[each]:
        #            kwargs[each] = locals()[each]
        #    except:
        #        pass
        #kwargs = merge_config_kwargs(self, kwargs,self.CONFIG)
        if copy:
            mobject=mobject.copy()
        if isinstance(color, (int, float)):
            if color < 0:
                run_time = -color
                color = None
        animations = AGroup()
        if f_color is not None or f_width is not None or f_opacity is not None:
            animations.add(
                ApplyMethod(mobject.set_stroke, f_color,f_width, f_opacity,  rate_func=funz(step,0.05),run_time=run_time*ratio[1]))
                
            run_time = run_time*ratio[0]
        elif (copy and fadeout is None) or fadeout:
            animations.add(FadeOut(mobject,run_time=0.001))
        if highlight:
            kws=dict()
            if color is not None:
                kws['color']=color
            if width is not None:
                kws['width']=width
            if opacity is not None:
                kws['opacity']=opacity
            animations.add_to_back(Highlight(
                    mobject,scale_factor=scale_factor, run_time=run_time,**kws))
        else:
            animations.add_to_back(
                ApplyMethod(mobject.set_stroke, color, width, opacity, rate_func=funz(linear_pulse,0.05,0.9), run_time=run_time))
                #Transform(mobject,mobject.copy().set_stroke(color, width, opacity), rate_func=funz(linear_pulse,0.05,0.9), run_time=run_time))
                #ShowCreation(mobject.copy().set_stroke(color, width, opacity), rate_func=funz(linear_pulse,0.05,0.9), run_time=run_time))
        super().__init__(*animations, **kwargs)


class MoveTo(AnimationGroup):
    CONFIG = {
        "name": None,
    }

    def func(self, mobj):
        return mobj.move_to

    def __init__(self, mobjs1, mobjs2, run_time=1, transpose=1, lag_ratio=0, **kwargs):
        kwargs = merge_config_kwargs(self, kwargs)
        animations = AGroup()
        if transpose:
            #[a, b, c], [x, y, z]
            mobjects = list(map(list, zip(mobjs1, mobjs2)))
            #[a, x], [b, y], [c, z]
        [animations.add(ApplyMethod(self.func(each[0]), each[1], **kwargs))
         for each in mobjects]
        super().__init__(*animations, lag_ratio=lag_ratio, run_time=run_time, **kwargs)


class SwingTo(MoveTo):
    CONFIG = {
        "rate_func": there_and_back_with_pause,
    }


class BounceBack(MoveTo):
    CONFIG = {
        "rate_func": there_and_back,
    }


class NextTo(MoveTo):
    def func(self, mobj):
        return mobj.next_to


class ShiftTo(MoveTo):
    def func(self, mobj):
        return mobj.shift


class Transforms(AnimationGroup):
    def func(self, mobj1, mobj2, path, **kwargs):
        return Transform(mobj1, mobj2, path_func=path, **kwargs)

    def __init__(self, mobjs1, mobjs2, paths=None, pre=None, post=None, group=True, run_time=1, transpose=1, **kwargs):
        animations = AGroup()
        if group:
            lag_ratio = 0
        else:
            lag_ratio = 1
        if paths is None:
            paths = [None]*min(len(mobjs1), len(mobjs2))
        if transpose:
            #[a, b, c], [x, y, z]
            mobjects = list(map(list, zip(mobjs1, mobjs2, paths)))
            #[a, x], [b, y], [c, z]
        [animations.add(self.func(each[0], each[1], each[2], **kwargs))
         for each in mobjects]
        if pre is not None:
            animations.add_to_back(*pre)
        if post is not None:
            animations.add(*post)

        super().__init__(*animations, lag_ratio=lag_ratio, run_time=run_time, **kwargs)


class Shows(OneByOne):
    '''*mobjects, rate_func=shorten, **kwargs\n
    '''
    CONFIG = {
        "funx": Show,
    }
    
    def __init__(self, *mobjects, rate_func=shorten, **kwargs):
        animations = AGroup()
        for mobject in mobjects:
            animations.add(self.CONFIG["funx"](mobject, rate_func=rate_func,**kwargs))
        super().__init__(*animations, **kwargs)

class Highlights(OneByOne):
    CONFIG = {
        "funx": Highlight,
    }

    def __init__(self, *mobjects, width=None, run_time=1, lag_ratio=1, rate_func=shorten, **kwargs):
        while isinstance(mobjects[-1],(int,float)):
            if mobjects[-1]>=0:
                width=mobjects[-1]
                mobjects=mobjects[:-1]
            else:
                run_time=-mobjects[-1]
                mobjects=mobjects[:-1]
        animations = AGroup()
        for mobject in mobjects:
            animations.add(self.CONFIG["funx"](mobject, width=width,**kwargs))
        super().__init__(*animations, run_time=run_time,lag_ratio=lag_ratio, rate_func=rate_func, **kwargs)

class AnimateStrokes(AnimationGroup):#
    def __init__(self, *args, func=AnimateStroke, run_time=None, fix_time=None, lag_ratio=0,**kwargs):
        animations=AGroup()
        runtime={}
        fixtime={}
        if isinstance(args[-1], (int,float)):
            if args[-1]>=0:
                runtime.update({'run_time':args[-1]})
            else:
                fixtime.update({'run_time':-args[-1]})
            args=args[:-1]
        if run_time is not None:
            runtime.update({'runtime':runtime})
        if fix_time is not None:
            fixtime.update({'fix_time':fix_time})
        for arg in args:
            kws={}
            if isinstance(arg[-1], dict):
                kws=arg[-1]
                arg=arg[:-1]
            kws.update(fixtime)
            kws.update(kwargs)
            mobj=VMobject()
            for each in arg:
                if isinstance(arg[0],(Mobject,Group,VMobject,VGroup)):
                    mobj.add(arg[0])
                    arg=arg[1:]
            animations.add(func(mobj,*arg,**kws))
        super().__init__(*animations,lag_ratio=lag_ratio,**runtime)

