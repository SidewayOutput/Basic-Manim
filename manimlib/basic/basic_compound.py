from manimlib.animation.composition import AnimationGroup, Succession
from manimlib.animation.creation import ShowSubmobjectsOneByOne,ShowCreation
from manimlib.animation.fading import FadeOut
from manimlib.basic.basic_animation import FadeInThenIndicateThenFadeOut,ShowCreationThenFadeOut
from manimlib.mobject.mobject import Mobject
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.utils.config_ops import merge_config_kwargs
from manimlib.utils.rate_functions import linear


class ShowSubmobjectsOneByOneAndFadeInThenIndicateThenFadeOut(AnimationGroup):
    CONFIG = {
        "scale_factor": 1.2,
    }

    def __init__(self, *mobjects, **kwargs):
        self.show_rate_func = linear
        kwargs = merge_config_kwargs(self, kwargs)
        super().__init__(
            ShowSubmobjectsOneByOne(mobjects[0].add(
                Mobject()), rate_func=self.show_rate_func, **kwargs),
            FadeInThenIndicateThenFadeOut(
                mobjects[1],   **kwargs),
            **kwargs)


class ShowCreationOneByOneThenFadeOut(Succession):
    CONFIG = {
        # "rate_func": there_and_back,
        # "scale_factor": 1.2,
        # "color": YELLOW,
        "remover": False,
        "lag_ration": 0.1,
    }

    def __init__(self, *mobjects, run_time=5, ratio_array=[0.95, 0.05], **kwargs):
        super().__init__(
            ShowCreationThenFadeOut(mobjects[0], run_time=run_time*ratio_array[0], **kwargs),  # run_time *
            # ratio_array[0], **kwargs),  # 0.5
            ShowCreationThenFadeOut(mobjects[1], run_time=run_time*ratio_array[0], **kwargs),  # run_time *
            # ratio_array[0], **kwargs),  # 0.5
            FadeOut(VGroup(*mobjects), run_time=run_time * \
                    ratio_array[1], **kwargs),  # 0.03
            **kwargs
        )
