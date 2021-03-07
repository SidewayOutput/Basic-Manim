from numpy import arange, array
from manimlib.constants import YELLOW
from manimlib.mobject.types.vectorized_mobject import VGroup, VMobject
from manimlib.utils.config_ops import digest_config


class ParametricCurve(VMobject):
    CONFIG = {
        "t_range": [0, 1, 0.1],
        "epsilon": 1e-8,
        # TODO, automatically figure out discontinuities
        "discontinuities": [],
        "use_smoothing": True,
    }

    def __init__(self, t_func, t_range=None, **kwargs):
        digest_config(self, kwargs)
        if t_range is not None:
            self.t_range[:len(t_range)] = t_range
        # To be backward compatible with all the scenes specifying t_min, t_max, step_size
        self.t_range = [
            kwargs.get("t_min", self.t_range[0]),
            kwargs.get("t_max", self.t_range[1]),
            kwargs.get("step_size", self.t_range[2]),
        ]
        self.t_func = t_func
        VMobject.__init__(self, **kwargs)

    def get_point_from_function(self, t):
        return self.t_func(t)

    def init_points(self):
        t_min, t_max, step = self.t_range

        jumps = array(self.discontinuities)
        jumps = jumps[(jumps >= t_min) & (jumps <= t_max)]
        if len(jumps) > 0:
            if t_min == jumps[0]:
                t_min = jumps[0]+self.epsilon
                jumps = jumps[1:]
            if t_max == jumps[-1]:
                t_max = jumps[0]-self.epsilon
                jumps = jumps[:-1]
        boundary_times = [t_min, t_max, *
                          (jumps - self.epsilon), *(jumps + self.epsilon)]
        boundary_times.sort()
        for t1, t2 in zip(boundary_times[0::2], boundary_times[1::2]):
            #t_range = [*arange(t1, t2, step), t2]
            t_range = list(arange(t1, t2, step))
            if t_range[-1] != t2:
                t_range.append(t2)

            points = array([self.t_func(t) for t in t_range])
            self.start_new_path(points[0])
            self.add_points_as_corners(points[1:])
        if self.use_smoothing:
            self.make_smooth()
            # self.make_approximately_smooth()

        return self


class ParametricFunction(ParametricCurve):
    CONFIG = {
        "t_min": 0,
        "t_max": 1,
        "step_size": 0.01,  # Use "auto" (lowercase) for automatic step size
    }

    def __init__(self, t_func, **kwargs):
        digest_config(self, kwargs)
        self.t_range = [self.t_min, self.t_max, self.get_step_size()]
        ParametricCurve.__init__(self, t_func, **kwargs)

    def get_function(self):
        return self.function

    def get_step_size(self, t=None):
        if self.step_size == "auto":
            """
            for x between -1 to 1, return 0.01
            else, return log10(x) (rounded)
            e.g.: 10.5 -> 0.1 ; 1040 -> 10
            """
            if t == 0:
                scale = 0
            else:
                scale = math.log10(abs(t))
                if scale < 0:
                    scale = 0

                scale = math.floor(scale)

            scale -= 2
            return math.pow(10, scale)
        else:
            return self.step_size


class FunctionGraph(ParametricCurve):
    CONFIG = {
        "color": YELLOW,
        "x_range": [-8, 8, 0.01],
        # "x_min": -FRAME_X_RADIUS,
        # "x_max": FRAME_X_RADIUS,
        # "step_size": 0.01,
    }

    def __init__(self, function, x_range=None, **kwargs):
        digest_config(self, kwargs)
        self.function = function
        if x_range is not None:
            self.x_range[:len(x_range)] = x_range

        def parametric_function(t):
            return [t, function(t), 0]
        super().__init__(
            parametric_function,
            # t_min=self.x_min,
            # t_max=self.x_max,
            self.x_range,
            **kwargs
        )

    def get_function(self):
        return self.function

    def get_point_from_function(self, x):
        return self.t_func(x)
        # return self.parametric_function(x)


class FunctionsGraph(VGroup):  # append_vectorized_mobject
    def __init__(self, *functiongraphs, **kwargs):
        VGroup.__init__(self, **kwargs)
        functionsgraphs = []
        # self.add(exec("FunctionGraph("+functiongraphs[0]+")"))
        [exec("functionsgraphs.append(FunctionGraph("+functiongraph+"))",
              {"functionsgraphs": functionsgraphs, "FunctionGraph": FunctionGraph}) for functiongraph in functiongraphs]

        vmobject = VMobject()
        [vmobject.append_vectorized_mobject(
            functionsgraph) for functionsgraph in functionsgraphs]
        self.add(vmobject)
