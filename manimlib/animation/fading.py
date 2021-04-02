from manimlib.animation.animation import Animation
from manimlib.animation.animation import DEFAULT_ANIMATION_LAG_RATIO
from manimlib.animation.transform import Transform
from manimlib.constants import DOWN
from manimlib.mobject.mobject import Group
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.bezier import interpolate
from manimlib.utils.rate_functions import there_and_back


DEFAULT_FADE_LAG_RATIO = 0


class FadeOut(Transform):
    CONFIG = {
        "remover": True,
        "lag_ratio": DEFAULT_FADE_LAG_RATIO,
    }

    def create_target(self):
        return self.mobject.copy().fade(1)

    def clean_up_from_scene(self, scene=None):
        super().clean_up_from_scene(scene)
        self.interpolate(0)


class FadeIn(Transform):
    CONFIG = {
        "lag_ratio": DEFAULT_FADE_LAG_RATIO,
    }

    def create_target(self):
        return self.mobject

    def create_starting_mobject(self):
        start = super().create_starting_mobject()
        start.fade(1)
        if isinstance(start, VMobject):
            start.set_stroke(width=0)
            start.set_fill(opacity=0)
        return start


class FadeInFrom(Transform):
    CONFIG = {
        "direction": DOWN,
        "lag_ratio": DEFAULT_ANIMATION_LAG_RATIO,
    }

    def __init__(self, mobject, direction=None, **kwargs):
        if direction is not None:
            self.direction = direction
        super().__init__(mobject, **kwargs)

    def create_target(self):
        return self.mobject.copy()

    def begin(self):
        super().begin()
        self.starting_mobject.shift(self.direction)
        self.starting_mobject.fade(1)


class FadeInFromDown(FadeInFrom):
    """
    Identical to FadeInFrom, just with a name that
    communicates the default
    """
    CONFIG = {
        "direction": DOWN,
        "lag_ratio": DEFAULT_ANIMATION_LAG_RATIO,
    }


class FadeOutAndShift(FadeOut):
    CONFIG = {
        "direction": DOWN,
    }

    def __init__(self, mobject, direction=None, **kwargs):
        if direction is not None:
            self.direction = direction
        super().__init__(mobject, **kwargs)

    def create_target(self):
        target = super().create_target()
        target.shift(self.direction)
        return target


class FadeOutAndShiftDown(FadeOutAndShift):
    """
    Identical to FadeOutAndShift, just with a name that
    communicates the default
    """
    CONFIG = {
        "direction": DOWN,
    }


class FadeInFromPoint(FadeIn):
    def __init__(self, mobject, point, **kwargs):
        self.point = point
        super().__init__(mobject, **kwargs)

    def create_starting_mobject(self):
        start = super().create_starting_mobject()
        start.scale(0)
        start.move_to(self.point)
        return start


class FadeInFromLarge(FadeIn):
    CONFIG = {
        "scale_factor": 2,
    }

    def __init__(self, mobject, scale_factor=2, **kwargs):
        if scale_factor is not None:
            self.scale_factor = scale_factor
        super().__init__(mobject, **kwargs)

    def create_starting_mobject(self):
        start = super().create_starting_mobject()
        start.scale(self.scale_factor)
        return start


class FadeOutToPoint(FadeOut):
    def __init__(self, mobject, point, **kwargs):
        super().__init__(
            mobject,
            shift=point - mobject.get_center(),
            scale=0,
            **kwargs,
        )


class FadeTransform(Transform):
    CONFIG = {
        "stretch": True,
        "dim_to_match": 1,
    }

    def __init__(self, mobject, target_mobject, **kwargs):
        self.to_add_on_completion = target_mobject
        mobject.save_state()
        super().__init__(
            Group(mobject, target_mobject.copy()),
            **kwargs
        )

    def begin(self):
        self.ending_mobject = self.mobject.copy()
        Animation.begin(self)
        # Both 'start' and 'end' consists of the source and target mobjects.
        # At the start, the traget should be faded replacing the source,
        # and at the end it should be the other way around.
        start, end = self.starting_mobject, self.ending_mobject
        for m0, m1 in ((start[1], start[0]), (end[0], end[1])):
            self.ghost_to(m0, m1)

    def ghost_to(self, source, target):
        source.replace(target, stretch=self.stretch, dim_to_match=self.dim_to_match)
        source.set_opacity(0)

    def get_all_mobjects(self):
        return [
            self.mobject,
            self.starting_mobject,
            self.ending_mobject,
        ]

    def get_all_families_zipped(self):
        return Animation.get_all_families_zipped(self)

    def clean_up_from_scene(self, scene):
        Animation.clean_up_from_scene(self, scene)
        scene.remove(self.mobject)
        self.mobject[0].restore()
        scene.add(self.to_add_on_completion)


class FadeTransformPieces(FadeTransform):
    def begin(self):
        self.mobject[0].align_family(self.mobject[1])
        super().begin()

    def ghost_to(self, source, target):
        for sm0, sm1 in zip(source.get_family(), target.get_family()):
            super().ghost_to(sm0, sm1)


class VFadeIn(Animation):
    """
    VFadeIn and VFadeOut only work for VMobjects,
    """
    CONFIG = {
        "suspend_mobject_updating": False,
    }

    def interpolate_submobject(self, submob, start, alpha):
        submob.set_stroke(
            opacity=interpolate(0, start.get_stroke_opacity(), alpha)
        )
        submob.set_fill(
            opacity=interpolate(0, start.get_fill_opacity(), alpha)
        )


class VFadeOut(VFadeIn):
    CONFIG = {
        "remover": True
    }

    def interpolate_submobject(self, submob, start, alpha):
        super().interpolate_submobject(submob, start, 1 - alpha)


class VFadeInThenOut(VFadeIn):
    CONFIG = {
        "rate_func": there_and_back,
        "remover": True,
    }
