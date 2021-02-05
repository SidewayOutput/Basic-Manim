from manimlib.animation.composition import AnimationGroup
from manimlib.animation.creation import ShowSubmobjectsOneByOne
from manimlib.basic.basic_animation import FadeInThenIndicateThenFadeOut
from manimlib.mobject.mobject import Mobject
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
