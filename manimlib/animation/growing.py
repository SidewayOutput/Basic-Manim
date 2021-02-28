from manimlib.animation.transform import Transform
from manimlib.basic.basic_function import to_expand_lists, to_get_point
from manimlib.constants import PI
from manimlib.utils.config_ops import generate_args, merge_config_kwargs


class GrowFromPoint(Transform):
    def __init__(self, mobject, mobject_or_point="get_center()", *args, **kwargs):
        self.mobject_or_point = to_get_point(mobject_or_point, mobject)
        self.args_name = ["point_color", "scale"]
        self.args = [None, 0]
        [self.point_color, self.scale] = \
            generate_args(self, args, self.args)
        kwargs = merge_config_kwargs(self, kwargs, self.args_name)
        super().__init__(mobject, **kwargs)

    def create_target(self):
        return self.mobject

    def create_starting_mobject(self):
        mobject = self.create_initial_mobject()
        mobject.set_stroke(
            width=(mobject.stroke_width*self.scale))
        if self.point_color:
            mobject.set_color(self.point_color)
        return mobject

    def create_initial_mobject(self):
        mobject = super().create_starting_mobject()
        return mobject.scale(self.scale).move_to(self.mobject_or_point)


class GrowFromCenter(GrowFromPoint):
    def __init__(self, mobject, *args, **kwargs):
        super().__init__(mobject, mobject.get_center(), *args, **kwargs)


class GrowFromEdge(GrowFromPoint):
    def __init__(self, mobject, edge=[-1, 1, 0], *args, **kwargs):
        super().__init__(mobject, mobject.get_critical_point(edge), *args, **kwargs)


class GrowFromSide(GrowFromPoint):
    def __init__(self, mobject, side=[0, 1, 0], center=False, *args, **kwargs):
        self.side = side
        self.center = center
        super().__init__(mobject, mobject.get_critical_point(side), *args, **kwargs)

    def create_initial_mobject(self):
        mobject = self.mobject.copy()
        dim = [i for i, each in enumerate(self.side) if each]
        mobject.stretch_to_fit(to_expand_lists(self.scale, dim), dim)
        if not self.center:
            mobject.move_to(self.mobject_or_point)
        else:
            mobject.move_to(self.mobject.get_center())
        return mobject


class DiminishToPoint(GrowFromPoint):
    def __init__(self, mobject, mobject_or_point="get_center()", *args, **kwargs):
        super().__init__(mobject, mobject_or_point, *args, **kwargs)

    def create_target(self):
        mobject = self.create_final_mobject()
        mobject.set_stroke(
            width=(mobject.stroke_width*self.scale))
        if self.point_color:
            mobject.set_color(self.point_color)
        return mobject

    def create_starting_mobject(self):
        mobject = self.mobject.copy()
        return mobject

    def create_final_mobject(self):
        mobject = self.mobject.copy()
        return mobject.scale(self.scale).move_to(self.mobject_or_point)


class DiminishToCenter(DiminishToPoint):
    def __init__(self, mobject, *args, **kwargs):
        super().__init__(mobject, mobject.get_center(), *args, **kwargs)


class DiminishToEdge(DiminishToPoint):
    def __init__(self, mobject, edge=[-1, 1, 0], *args, **kwargs):
        super().__init__(mobject, mobject.get_critical_point(edge), *args, **kwargs)


class DiminishToSide(DiminishToPoint):
    def __init__(self, mobject, side=[0, 1, 0], center=False, *args, **kwargs):
        self.side = side
        self.center = center
        super().__init__(mobject, mobject.get_critical_point(side), *args, **kwargs)

    def create_final_mobject(self):
        mobject = self.mobject.copy()
        dim = [i for i, each in enumerate(self.side) if each]
        mobject.stretch_to_fit(to_expand_lists(self.scale, dim), dim)
        if not self.center:
            mobject.move_to(self.mobject_or_point)
        else:
            mobject.move_to(self.mobject.get_center())
        return mobject


class GrowArrow(GrowFromPoint):
    def __init__(self, arrow, point_by_ratio=0, *args, **kwargs):
        super().__init__(arrow, point_by_ratio, *args, **kwargs)


class ExpandArrow(GrowArrow):
    def __init__(self, arrow, point_by_ratio=1, *args, **kwargs):
        super().__init__(arrow, point_by_ratio, *args, **kwargs)


class DiminishArrow(DiminishToPoint):
    def __init__(self, arrow, point_by_ratio=1, *args, **kwargs):
        super().__init__(arrow, point_by_ratio, *args, **kwargs)


class RetractArrow(DiminishToPoint):
    def __init__(self, arrow, point_by_ratio=0, *args, **kwargs):
        super().__init__(arrow, point_by_ratio, *args, **kwargs)


class SpinInFromNothing(GrowFromCenter):
    CONFIG = {
        "path_arc": PI,
    }


class SpinInFrom(GrowFromPoint):
    CONFIG = {
        "path_arc": PI,
    }

    def __init__(self, mobject, point="get_center()", *args, **kwargs):
        super().__init__(mobject, point, *args, **kwargs)


class SpinOutFrom(SpinInFrom):
    CONFIG = {
        "path_arc": -PI,
    }


class SpinInTo(DiminishToPoint):
    CONFIG = {
        "path_arc": PI,
    }

    def __init__(self, mobject, point="get_center()", *args, **kwargs):
        super().__init__(mobject, point, *args, **kwargs)


class SpinOutTo(SpinInTo):
    CONFIG = {
        "path_arc": -PI,
    }
