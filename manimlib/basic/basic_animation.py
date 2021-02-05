from manimlib.animation.animation import AGroup
from manimlib.animation.composition import AnimationGroup, Succession
from manimlib.animation.fading import FadeIn, FadeOut
from manimlib.animation.indication import Indicate, ShowPassingFlash
from manimlib.constants import YELLOW
from manimlib.utils.config_ops import merge_config_kwargs
from manimlib.utils.rate_functions import rush_into, there_and_back


class FadeInThenIndicate(Succession):
    CONFIG = {
        "rate_func": there_and_back,
        "scale_factor": 1.2,
        "color": YELLOW,
        # "remover": False,
    }

    def __init__(self, mobject, **kwargs):
        super().__init__(
            FadeIn(mobject),
            Indicate(mobject),
            **kwargs
        )


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


class FadeoutSuccession(Succession):
    def __init__(self, animation, run_time=1, ratio_array=[1, 1, 1], fadeout_func=rush_into, **kwargs):
        animations = AGroup(
            #FadeIn(animation.mobject, run_time=0.01),
            animation,
            IndicateThenFadeOut(
                animation.mobject, run_time=animation.run_time*0.1, scale_factor=1, color=None, ratio_array=[0.95, 0.05], rate_func=fadeout_func)  # ,ratio_array=[1.2, 1.1, 0.05]
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
