from copy import deepcopy
import numpy as np
#import manimlib.constants
from manimlib.container.container import Manim
from manimlib.constants import DEFAULT_ANIMATION_RUN_TIME,DEFAULT_ANIMATION_LAG_RATIO
from manimlib.mobject.mobject import Mobject
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.utils.config_ops import digest_config
from manimlib.utils.iterables import list_update
from manimlib.utils.rate_functions import smooth
from manimlib.mobject.mobject import _AnimationBuilder

#DEFAULT_ANIMATION_RUN_TIME = 1.0
#DEFAULT_ANIMATION_LAG_RATIO = 0


class Animation(Manim):
    CONFIG = {
        "run_time": DEFAULT_ANIMATION_RUN_TIME,
        "rate_func": smooth,
        "name": None,
        # Does this animation add or remove a mobject form the screen
        "remover": False,
        # If 0, the animation is applied to all submobjects
        # at the same time
        # If 1, it is applied to each successively.
        # If 0 < lag_ratio < 1, its applied to each
        # with lagged start times
        "lag_ratio": DEFAULT_ANIMATION_LAG_RATIO,
        "suspend_mobject_updating": True,
        "r_color":None,
        "r_width":None,
        "r_opacity":None,
        "r_flag":True,
        "s_flag":True,
    }

    def __init__(self, mobject, **kwargs):
        assert(isinstance(mobject, Mobject))
        digest_config(self, kwargs)
        self.mobject = mobject


    def __str__(self):
        if self.name:
            return self.name
        return self.__class__.__name__ + str(self.mobject)

    def start(self):
        #self.mobjecte=self.interpolate(0)
        self.begin()

    def begin(self):
        # This is called right as an animation is being
        # played.  As much initialization as possible,
        # especially any mobject copying, should live in
        # this method
        self.starting_mobject = self.create_starting_mobject()
        if self.suspend_mobject_updating:
            # All calls to self.mobject's internal updaters
            # during the animation, either from this Animation
            # or from the surrounding scene, should do nothing.
            # It is, however, okay and desirable to call
            # the internal updaters of self.starting_mobject,
            # or any others among self.get_all_mobjects()
            self.mobject.suspend_updating()
        self.interpolate(0)

    def finish(self):
        self.interpolate(1)
        if self.suspend_mobject_updating:
            self.mobject.resume_updating()

    def clean_up_from_scene(self, scene):
        if self.is_remover():
            scene.remove(self.mobject)

    def create_starting_mobject(self):
        # Keep track of where the mobject starts
        return self.mobject.copy()

    def get_all_mobjects(self):
        """
        Ordering must match the ording of arguments to interpolate_submobject
        """
        return self.mobject, self.starting_mobject

    def get_all_families_zipped(self):
        return zip(*[
            mob.family_members_with_points()
            for mob in self.get_all_mobjects()
        ])

    def update_mobjects(self, dt):
        """
        Updates things like starting_mobject, and (for
        Transforms) target_mobject.  Note, since typically
        (always?) self.mobject will have its updating
        suspended during the animation, this will do
        nothing to self.mobject.
        """
        for mob in self.get_all_mobjects_to_update():
            mob.update(dt)

    def get_all_mobjects_to_update(self):
        # The surrounding scene typically handles
        # updating of self.mobject.  Besides, in
        # most cases its updating is suspended anyway
        return list(filter(
            lambda m: m is not self.mobject,
            self.get_all_mobjects()
        ))

    def copy(self):
        return deepcopy(self)

    def update_config(self, **kwargs):
        digest_config(self, kwargs)
        return self

    # Methods for interpolation, the mean of an Animation
    def interpolate(self, alpha):
        alpha = np.clip(alpha, 0, 1)
        self.interpolate_mobject(self.rate_func(alpha))

    def update(self, alpha):
        """
        This method shouldn't exist, but it's here to
        keep many old scenes from breaking
        """
        self.interpolate(alpha)

    def interpolate_mobject(self, alpha):
        families = list(self.get_all_families_zipped())
        for i, mobs in enumerate(families):
            sub_alpha = self.get_sub_alpha(alpha, i, len(families))
            self.interpolate_submobject(*mobs, sub_alpha)

    def interpolate_submobject(self, submobject, starting_sumobject, alpha):
        # Typically ipmlemented by subclass
        pass

    def get_sub_alpha(self, alpha, index, num_submobjects):
        # TODO, make this more understanable, and/or combine
        # its functionality with AnimationGroup's method
        # build_animations_with_timings
        lag_ratio = self.lag_ratio
        full_length = (num_submobjects - 1) * lag_ratio + 1
        value = alpha * full_length
        lower = index * lag_ratio
        return np.clip((value - lower), 0, 1)

    # Getters and setters
    def set_run_time(self, run_time):
        self.run_time = run_time
        return self

    def get_run_time(self):
        return self.run_time

    def set_rate_func(self, rate_func):
        self.rate_func = rate_func
        return self

    def get_rate_func(self):
        return self.rate_func

    def set_name(self, name):
        self.name = name
        return self

    def is_remover(self):
        return self.remover

    def zbe(self, name=None,module=None):
        #??if name in vars(manimlib.constants):
        #    raise Warning("Duplicate Variable")
        if module is None:
            exec('manimlib.constants.'+name+'=self')
        else:
            #x=f'{module=}'.split('=')[0] 
            #print(x)
            #exec(x+'=module')
            #exec(x+'.'+name+'=self',globals(),locals())
            exec("module"+'.'+name+'=self',globals(),locals())
        return self


def prepare_animation(anim):
    if isinstance(anim, _AnimationBuilder):
        return anim.build()

    if isinstance(anim, Animation):
        return anim

    raise TypeError(f"Object {anim} cannot be converted to an animation")

class Animations(Animation):
    def __init__(self, *mobjects, **kwargs):
        mobject=VGroup(*mobjects)
        Animation.__init__(self, mobject, **kwargs)


class AGroup(Animation):
    def __init__(self, *animations, **kwargs):
        if not all([isinstance(m, (Animation)) for m in animations]):
            raise Exception("All subanimations must be of type Animation")
        digest_config(self, kwargs)
        if self.name is None:
            self.name = self.__class__.__name__
        self.subanimations = []
        Animation.__init__(self, Mobject(),  **kwargs)
        self.add(*animations)

    def __str__(self):
        return str(self.name)

    def add(self, *animations):
        if self in animations:
            raise Exception("Animation cannot contain self")
        self.subanimations = list_update(self.subanimations, animations)
        return self

    def add_to_back(self, *animations):
        self.remove(*animations)
        self.subanimations = list(animations) + self.subanimations
        return self

    def remove(self, *animations):
        for aobject in animations:
            if aobject in self.subanimations:
                self.subanimations.remove(aobject)
        return self

    # Family matters

    def __getitem__(self, value):
        self_list = self.split()
        if isinstance(value, slice):
            GroupClass = self.get_group_class()
            return GroupClass(*self_list.__getitem__(value))
        return self_list.__getitem__(value)

    def __iter__(self):
        return iter(self.split())

    def __len__(self):
        return len(self.split())

    def get_group_class(self):
        return AGroup

    def split(self):
        return self.subanimations
