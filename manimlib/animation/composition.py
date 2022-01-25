import numpy as np

from typing import Optional

from manimlib.animation.animation import Animation
from manimlib.constants import DEFAULT_LAGGED_START_LAG_RATIO
from manimlib.mobject.mobject import Group, Mobject
from manimlib.utils.bezier import integer_interpolate
from manimlib.utils.bezier import interpolate
from manimlib.utils.config_ops import digest_config
from manimlib.utils.iterables import remove_list_redundancies
from manimlib.utils.rate_functions import linear


#DEFAULT_LAGGED_START_LAG_RATIO = 0.05


class AnimationGroup(Animation):
    '''*animations,\n
    +num:run_time; -num:fix_time
    -'''
    CONFIG = {
        # If None, this defaults to the sum of all
        # internal animations
        "run_time": None,
        "rate_func": linear,
        # If 0, all animations are played at once.
        # If 1, all are played successively.
        # If >0 and <1, they start at lagged times
        # from one and other.
        "lag_ratio": 0,
        "group": None,
        "fix_time": None,
        "retain":False,
        "error":0
    }

    def __init__(self, *animations, **kwargs):
        digest_config(self, kwargs)
        if len(animations)>1:
            if isinstance(animations[-1], (int, float)):
                if animations[-1] >= 0:
                    self.run_time = animations[-1]
                    animations = animations[:-1]
                else:
                    self.fix_time = -animations[-1]
                    animations = animations[:-1]
            if animations[-1].run_time<1./60:#./15
                #self.error=animations[-1].run_time
                animations[-1].run_time=1./15
        self.animations = animations
        if self.fix_time is not None and self.run_time is None:
            for anim in self.animations:
                if  not self.retain or (anim.run_time is None or (anim.run_time>=0.001 and anim.run_time<=1)):
                    anim.run_time = self.fix_time
        if self.group is None:
            self.group = Group(*remove_list_redundancies(
                [anim.mobject for anim in animations]
            ))

        self.init_run_time()
        Animation.__init__(self, self.group, **kwargs)

    def get_all_mobjects(self):
        return self.group

    def begin(self):
        for anim in self.animations:
            anim.begin()
        # self.init_run_time()

    def finish(self):
        for anim in self.animations:
            anim.finish()

    def clean_up_from_scene(self, scene):
        for anim in self.animations:
            anim.clean_up_from_scene(scene)

    def update_mobjects(self, dt):
        for anim in self.animations:
            anim.update_mobjects(dt)

    def init_run_time(self):
        self.build_animations_with_timings()
        if self.anims_with_timings:
            self.max_end_time = np.max([
                awt[2] for awt in self.anims_with_timings
            ])
        else:
            self.max_end_time = 0
        if self.run_time is None:
            self.run_time = self.max_end_time

    def build_animations_with_timings(self):
        """
        Creates a list of triplets of the form
        (anim, start_time, end_time)
        """
        self.anims_with_timings = []
        curr_time = 0
        for anim in self.animations:
            start_time = curr_time
            end_time = start_time + anim.get_run_time()
            self.anims_with_timings.append(
                (anim, start_time, end_time)
            )
            # Start time of next animation is based on
            # the lag_ratio
            curr_time = interpolate(
                start_time, end_time, self.lag_ratio
            )

    def interpolate(self, alpha):
        # Note, if the run_time of AnimationGroup has been
        # set to something other than its default, these
        # times might not correspond to actual times,
        # e.g. of the surrounding scene.  Instead they'd
        # be a rescaled version.  But that's okay!
        time = alpha * self.max_end_time
        for anim, start_time, end_time in self.anims_with_timings:
            anim_time = end_time - start_time
            if anim_time == 0:
                sub_alpha = 0
            else:
                sub_alpha = np.clip(
                    (time - start_time) / anim_time,
                    0, 1
                )
            anim.interpolate(sub_alpha)


class Succession(AnimationGroup):
    CONFIG = {
        "lag_ratio": 1,
    }

    def begin(self):
        assert(len(self.animations) > 0)
        self.init_run_time()
        self.active_animation = self.animations[0]
        self.active_animation.begin()

    def finish(self):
        self.active_animation.finish()

    def update_mobjects(self, dt):
        self.active_animation.update_mobjects(dt)

    def interpolate(self, alpha):
        index, subalpha = integer_interpolate(
            0, len(self.animations), alpha
        )
        animation = self.animations[index]
        if animation is not self.active_animation:
            self.active_animation.finish()
            animation.begin()
            self.active_animation = animation
        animation.interpolate(subalpha)


class AnimByAnim(Succession):
    CONFIG = {
        "index": 0,
        "active_index": 0,
        "active_start_time": None,
    }

    def zbegin(self):
        for anim in self.animations:
            anim.starting_mobject = anim.create_starting_mobject()
        assert(len(self.animations) > 0)
        self.init_run_time()
        self.active_animation = self.animations[0]
        self.active_animation.begin()


    def interpolate(self, alpha):
        current_time = alpha * self.run_time
        flag = 1
        while flag:
            if self.active_start_time == None:
                self.active_start_time = self.anims_with_timings[self.active_index][1]
                self.active_end_time = self.anims_with_timings[self.active_index][2]
            if current_time >= self.active_start_time:
                elapsed = min(current_time, self.active_end_time) - \
                    self.active_start_time
                active_run_time = self.active_animation.get_run_time()
                subalpha = elapsed / active_run_time if active_run_time != 0 else 1.
                self.active_animation.interpolate(subalpha)
            if current_time >= self.active_end_time-self.error and self.active_index < len(self.animations)-1:
                self.active_animation.finish()
                self.active_index += 1
                self.active_start_time = None
                self.active_animation = self.animations[self.active_index]
                self.active_animation.mobject.update()
                self.active_animation.begin()
            else:
                flag = 0

class PulseAnim(AnimByAnim):
    CONFIG = {
        "retain": True,
        "fix_time": 0.001,
    }

class LaggedAnim(Succession):#AnimByAnim
    CONFIG = {
        "lag_ratio": 1.,
        "active_index": 0,
        "pre_init": True  # False,
    }

    def begin(self):
        super().begin()
        if self.pre_init:
            for i in range(1, len(self.animations)):
                self.animations[i].begin()
        for anim in self.animations:
            anim.begin()
 
    def interpolate(self, alpha):
        current_time = alpha * self.run_time
        index = self.active_index
        flag = 1
        while flag:
            if current_time >= self.anims_with_timings[index][1]:
                elapsed = min(current_time, self.anims_with_timings[index][2]) - \
                    self.anims_with_timings[index][1]
                active_run_time = self.animations[index].get_run_time()
                subalpha = elapsed / active_run_time if active_run_time != 0.0 else 1.0
                self.animations[index].interpolate(subalpha)
            if current_time >= self.anims_with_timings[index][2]:
                self.animations[index].finish()
                self.active_index += 1
            flag = 0
            if index < len(self.animations)-1:
                index += 1
                if current_time >= self.anims_with_timings[index][1]:
                    self.active_animation = self.animations[self.active_index]
                    if not self.pre_init:
                        self.animations[index].begin()
                        self.pre_init = True
                    flag = 1


class LaggedStart(AnimationGroup):
    CONFIG = {
        "lag_ratio": DEFAULT_LAGGED_START_LAG_RATIO,
    }


class OneByOne(AnimationGroup):
    CONFIG = {
        "lag_ratio": 1,
    }


class LaggedStartMap(LaggedStart):
    CONFIG = {
        "run_time": 2,
    }

    def __init__(self, AnimationClass, mobject, arg_creator=None, **kwargs):
        args_list = []
        for submob in mobject:
            if arg_creator:
                args_list.append(arg_creator(submob))
            else:
                args_list.append((submob,))
        anim_kwargs = dict(kwargs)
        if "lag_ratio" in anim_kwargs:
            anim_kwargs.pop("lag_ratio")
        animations = [
            AnimationClass(*args, **anim_kwargs)
            for args in args_list
        ]
        super().__init__(*animations, **kwargs)
