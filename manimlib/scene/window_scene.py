import inspect
import time
import platform
import random as rrandom
import warnings

from numpy import arange, array, max, ndarray, random
from tqdm import tqdm as ProgressDisplay
import manimlib.constants
from manimlib.animation.animation import Animation,  prepare_animation, _AnimationBuilder
from manimlib.animation.composition import AnimationGroup,AnimByAnim
from manimlib.animation.creation import ShowCreation, ShowSubmobjectsOneByOne, Write
from manimlib.animation.fading import FadeIn, FadeOut
from manimlib.animation.growing import DiminishToCenter, GrowFromCenter,DiminishToPoint
from manimlib.animation.transform import ApplyMethod, MoveToTarget,ApplyFunction,ShrinkToCenter
from manimlib.basic.basic_mobject import GroupedMobject, MobjectOrChars, ListedMobject,ImageMobjectGroup
from manimlib.basic.basic_animation import DFadeOut,Display
from manimlib.camera.camera import Camera  # , CameraFrame
from manimlib.camera.moving_camera import MovingCamera
from manimlib.constants import DEFAULT_WAIT_TIME, FRAME_HEIGHT, FRAME_WIDTH, UP
from manimlib.container.container import Container
from manimlib.mobject.mobject import Group, Mobject
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.mobject.types.vectorized_mobject import VGroup,VMobject
from manimlib.scene.scene_file_writer import SceneFileWriter
from manimlib.utils.iterables import list_update
from manimlib.camera.cam import Cam
from manimlib.mobject.frame import ScreenRectangle, CameraFrame
from manimlib.utils.config_ops import digest_config
from manimlib.mobject.value_tracker import ValueTracker

class WindowScene(Container):
    
    CONFIG = {
        "scene_shape": None,#(FRAME_WIDTH, FRAME_HEIGHT),
        "scene_center": [0, 0, 0],
        "camera_class": Camera,
        "always_update_mobjects": False,
        "random_seed": 0,
        #"camera_config": {},######
        #"file_writer_config": {},#####
        # "skip_animations": False,
        # "start_at_animation_number": None,
        # "end_at_animation_number": None,
        # "leave_progress_bars": False,
    }
    
    def __init__(self, **kwargs):
        #V.scene=self
        self.be("scene")
        digest_config(self, kwargs)
        # self.init_vars()
        #print("pixel",self.camera_config["pixel_width"],self.camera_config["pixel_height"],)
        if WindowScene.CONFIG['scene_shape'] is None:
            WindowScene.CONFIG['scene_shape']=(manimlib.constants.FRAME_WIDTH,manimlib.constants.FRAME_HEIGHT)
            #self.cam.cairo_line_width_multiple=self.cam.cairo_line_width_multiple*16*9
        self.init_frame(frame_width=WindowScene.CONFIG['scene_shape'][0],
                        frame_height=WindowScene.CONFIG['scene_shape'][1],
                        frame_center=WindowScene.CONFIG['scene_center'])
        super().__init__(**kwargs)
        self.camera_config['frame_width'] = self.frame_width
        self.camera_config['frame_height'] = self.frame_height
        self.camera_config['frame_center'] = self.frame_center
        self.init_camera_frame(**self.camera_config)
        self.file_writer = SceneFileWriter(self, **self.file_writer_config,)
        print("frame",self.camera_config["frame_width"],self.camera_config["frame_height"],)        
        FRAME_WIDTH=self.camera_config["frame_width"]
        FRAME_HEIGHT=self.camera_config["frame_height"] 
        self.mobjects = []
        # TODO, remove need for foreground mobjects
        self.foreground_mobjects = []
        self.num_plays = 0
        self.time = 0
        self.original_skipping_status = self.skip_animations
        if self.random_seed is not None:
            rrandom.seed(self.random_seed)
            random.seed(self.random_seed)

        self.setup()
        try:
            # if self.camera.scene_frame:
            #    self.play(self.camera.scene_frame.animate.shift([1,1,0]),run_time=3)
            self.construct()
        except EndSceneEarlyException:
            pass
        self.tear_down()
        self.file_writer.finish()
        self.print_end_message()

    def init_vars(self):
        
        self.camera_class = vars(self)['camera_class']
        self.always_update_mobjects = vars(self)['always_update_mobjects']
        self.random_seed = vars(self)['random_seed']
        self.camera_config = vars(self)['camera_config']
        self.file_writer_config = vars(self)['file_writer_config']
        self.start_at_animation_number = vars(
            self)['start_at_animation_number']
        self.end_at_animation_number = vars(self)['end_at_animation_number']
        self.leave_progress_bars = vars(self)['leave_progress_bars']
        self.preview=vars(self)['preview']
        self.stop_skipping=vars(self)['stop_skipping']
        self.interact=vars(self)['interact']

    def init_camera_frame(self, **kwargs):
        
        self.camera = self.camera_class(**kwargs)

    def run(self):
        self.virtual_animation_start_time = 0
        self.real_animation_start_time = time.time()
        self.file_writer.begin()

        self.setup()
        try:
            self.construct()
        except EndSceneEarlyException:
            pass
        self.tear_down()

    def setup(self):
        """
        This is meant to be implement by any scenes which
        are comonly subclassed, and have some common setup
        involved before the construct method is called.
        """
        pass

    def construct(self):
        self.add(TextMobject("Hello, World!\\\\Welcome to Basic-Manim."))
        self.wait(5)
        #pass  # To be implemented in subclasses
    # Mobjects

    def embed(self):
        if not self.preview:
            # If the scene is just being
            # written, ignore embed calls
            return
        self.stop_skipping()
        self.linger_after_completion = False
        self.update_frame()

        from IPython.terminal.embed import InteractiveShellEmbed
        shell = InteractiveShellEmbed()
        # Have the frame update after each command
        shell.events.register('post_run_cell', lambda *a, **kw: self.update_frame())
        # Use the locals of the caller as the local namespace
        # once embeded, and add a few custom shortcuts
        local_ns = inspect.currentframe().f_back.f_locals
        local_ns["touch"] = self.interact
        for term in ("play", "wait", "add", "remove", "clear", "save_state", "restore"):
            local_ns[term] = getattr(self, term)
        shell(local_ns=local_ns, stack_depth=2)
        # End scene when exiting an embed.
        raise EndSceneEarlyException()

    def add(self, *mobjects):
        
        """
        Mobjects will be displayed, from background to
        foreground in the order with which they are added.
        """
        mobjects = [*mobjects, *self.foreground_mobjects]
        self.restructure_mobjects(to_remove=mobjects)
        self.mobjects += mobjects
        return self


    def remove(self, *mobjects):
        
        for list_name in "mobjects", "foreground_mobjects":
            self.restructure_mobjects(mobjects, list_name, False)
        return self

    def restructure_mobjects(self, to_remove,
                             mobject_list_name="mobjects",
                             extract_families=True):
        
        """
        In cases where the scene contains a group, e.g. Group(m1, m2, m3), but one
        of its submobjects is removed, e.g. scene.remove(m1), the list of mobjects
        will be editing to contain other submobjects, but not m1, e.g. it will now
        insert m2 and m3 to where the group once was.
        """
        if extract_families:
            to_remove = self.camera.extract_mobject_family_members(to_remove)
        _list = getattr(self, mobject_list_name)
        new_list = self.get_restructured_mobject_list(_list, to_remove)
        setattr(self, mobject_list_name, new_list)
        return self

    def get_displayed(self,mobjects):
        mobjs=self.get_restructured_mobject_list(mobjects,self.get_restructured_mobject_list(mobjects,self.mobjects))
        if mobjs:
            return VGroup(*mobjs)
        else:
            return VMobject()

    def get_restructured_mobject_list(self, mobjects, to_remove):
        
        new_mobjects = []

        def add_safe_mobjects_from_list(list_to_examine, set_to_remove):
            for mob in list_to_examine:
                if mob in set_to_remove:
                    continue
                intersect = set_to_remove.intersection(mob.get_family())
                if intersect:
                    add_safe_mobjects_from_list(mob.submobjects, intersect)
                else:
                    new_mobjects.append(mob)
        add_safe_mobjects_from_list(mobjects, set(to_remove))
        return new_mobjects
    # Frame

    def wait(self, duration=DEFAULT_WAIT_TIME, stop_condition=None):
        
        self.handle_scene(self.handle_wait, duration=duration,
                          stop_condition=stop_condition)

    def play(self, *args, **kwargs):
        self.handle_scene(self.handle_play, *args, **kwargs)

    def display(self, *args, run_time=0.07, **kwargs):
        if isinstance(args[-1],(int,float)):
            run_time=args[-1]
            args=args[:-1]
        try:
            self.play(AnimationGroup(*args), run_time=run_time, **kwargs)
        except:
            try:
                self.play(AnimationGroup(*args), run_time=run_time*4, **kwargs)
            except:
                try:
                    self.play(AnimationGroup(*args), run_time=run_time*2, **kwargs)
                except:
                    self.play(AnimationGroup(*args), run_time=1, **kwargs)
    
    def exec(self, animationgroup):
        for each in animationgroup.animations:
            try:
                if each.xaction=="display":
                    self.display(each,**vars(each))
                elif each.xaction=="post":
                    self.post(each,**vars(each))
                elif each.xaction=="sound":
                    try:
                        each.time_offset
                    except:
                        each.time_offset=0
                    try:
                        self.add_sound(each.sound,time_offset=each.time_offset)
                    except:
                        pass
                elif each.xaction=="fadeout":
                    try:
                        each.exclude_mobjs
                    except:
                        each.exclude_mobjs="foreground"
                    self.fadeout(exclude_mobjs=each.exclude_mobjs)
            except:
                self.play(each,**vars(each))

    def handle_scene(self, func, *args, **kwargs):
        
        self.update_skipping_status()
        allow_write = not self.skip_animations
        self.file_writer.begin_animation(allow_write)
        func(self, *args, **kwargs)
        self.file_writer.end_animation(allow_write)
        self.num_plays += 1

    def update_skipping_status(self):
        
        if self.start_at_animation_number:
            if self.num_plays == self.start_at_animation_number:
                self.skip_animations = False
        if self.end_at_animation_number:
            if self.num_plays >= self.end_at_animation_number:
                self.skip_animations = True
                raise EndSceneEarlyException()

    def handle_wait(self, *args, **kwargs):
        
        duration = kwargs['duration']
        stop_condition = kwargs['stop_condition']
        self.update_mobjects(dt=0)  # Any problems with this?
        if self.should_update_mobjects():
            time_progression = self.get_wait_time_progression(
                duration, stop_condition)
            # TODO, be smart about setting a static image
            # the same way Scene.play does
            last_t = 0
            for t in time_progression:
                dt = t - last_t
                last_t = t
                self.update_mobjects(dt)
                self.update_frame()
                self.add_frames(self.get_frame())
                if stop_condition is not None and stop_condition():
                    time_progression.close()
                    break
        elif self.skip_animations:
            # Do nothing
            return self
        else:
            self.update_frame()
            dt = 1 / self.camera.frame_rate
            n_frames = int(duration / dt)
            frame = self.get_frame()
            self.add_frames(*[frame] * n_frames)
        return self

    def handle_play(self, *args, **kwargs):
        
        args = args[1:]
        if len(args) == 0:
            warnings.warn("Called Scene.play with no animations")
            return
        '''
        animations = self.compile_play_args_to_animation_list(
            *args, **kwargs
        )
        '''
        if not isinstance(args[0], _AnimationBuilder):
            animations = self.compile_play_args_to_animation_list(
                *args, **kwargs)
        else:
            animations = self.compile_animations(*args, **kwargs)

        self.begin_animations(animations)
        self.progress_through_animations(animations)
        self.finish_animations(animations)

    def update_mobjects(self, dt):
        
        for mobject in self.mobjects:
            mobject.update(dt)

    def should_update_mobjects(self):
        
        return self.always_update_mobjects or any([
            mob.has_time_based_updater()
            for mob in self.get_mobject_family_members()
        ])

    def get_wait_time_progression(self, duration, stop_condition):
        
        if stop_condition is not None:
            time_progression = self.get_time_progression(
                duration,
                n_iterations=-1,  # So it doesn't show % progress
                override_skip_animations=True
            )
            time_progression.set_description(
                "Waiting for {}".format(stop_condition.__name__)
            )
        else:
            time_progression = self.get_time_progression(duration)
            time_progression.set_description(
                "Waiting {}".format(self.num_plays)
            )
        return time_progression

    def compile_play_args_to_animation_list(self, *args, **kwargs):
        
        """
        Each arg can either be an animation, or a mobject method
        followed by that methods arguments (and potentially follow
        by a dict of kwargs for that method).
        This animation list is built by going through the args list,
        and each animation is simply added, but when a mobject method
        s hit, a MoveToTarget animation is built using the args that
        follow up until either another animation is hit, another method
        is hit, or the args list runs out.
        """
        animations = []
        state = {
            "curr_method": None,
            "last_method": None,
            "method_args": [],
        }

        def compile_method(state):
            if state["curr_method"] is None:
                return
            mobject = state["curr_method"].__self__
            if state["last_method"] and state["last_method"].__self__ is mobject:
                animations.pop()
                # method should already have target then.
            else:
                mobject.generate_target()
            #
            if len(state["method_args"]) > 0 and isinstance(state["method_args"][-1], dict):
                method_kwargs = state["method_args"].pop()
            else:
                method_kwargs = {}
            state["curr_method"].__func__(
                mobject.target,
                *state["method_args"],
                **method_kwargs
            )
            animations.append(MoveToTarget(mobject))
            state["last_method"] = state["curr_method"]
            state["curr_method"] = None
            state["method_args"] = []

        for arg in args:
            #if isinstance(arg, Animation):
            #    compile_method(state)
            #    animations.append(arg)
            if inspect.ismethod(arg):
                compile_method(state)
                state["curr_method"] = arg
            elif state["curr_method"] is not None:
                state["method_args"].append(arg)
            elif isinstance(arg, Mobject):
                raise Exception("""
                    I think you may have invoked a method
                    you meant to pass in as a Scene.play argument
                """)
            else:
                #raise Exception("Invalid play arguments")
                try:
                    anim = prepare_animation(arg)
                except TypeError:
                    raise TypeError(f"Unexpected argument {arg} passed to Scene.play()")

                compile_method(state)
                animations.append(anim)

        compile_method(state)

        for animation in animations:
            # This is where kwargs to play like run_time and rate_func
            # get applied to all animations
            animation.update_config(**kwargs)

        return animations

    def compile_animations(self, *args, **kwargs):
        
        """
        Creates _MethodAnimations from any _AnimationBuilders and updates animation
        kwargs with kwargs passed to play().
        Parameters
        ----------
        *args : Tuple[:class:`Animation`]
            Animations to be played.
        **kwargs
            Configuration for the call to play().
        Returns
        -------
        Tuple[:class:`Animation`]
            Animations to be played.
        """
        animations = []
        for arg in args:
            try:
                animations.append(prepare_animation(arg))
            except TypeError:
                if inspect.ismethod(arg):
                    raise TypeError(
                        "Passing Mobject methods to Scene.play is no longer"
                        " supported. Use Mobject.animate instead."
                    )
                else:
                    raise TypeError(
                        f"Unexpected argument {arg} passed to Scene.play()."
                    )

        for animation in animations:
            for k, v in kwargs.items():
                setattr(animation, k, v)

        return animations

    def begin_animations(self, animations):
        
        curr_mobjects = self.get_mobject_family_members()
        for animation in animations:
            # Begin animation
            #animation.begin()
            animation.start()
            # Anything animated that's not already in the
            # scene gets added to the scene
            mob = animation.mobject
            if mob not in curr_mobjects:
                self.add(mob)
                curr_mobjects += mob.get_family()

    def get_moving_mobjects(self, *animations):
        
        # Go through mobjects from start to end, and
        # as soon as there's one that needs updating of
        # some kind per frame, return the list from that
        # point forward.
        animation_mobjects = [anim.mobject for anim in animations]
        mobjects = self.get_mobject_family_members()
        for i, mob in enumerate(mobjects):

            update_possibilities = [
                mob in animation_mobjects,
                len(mob.get_family_updaters()) > 0,
                mob in self.foreground_mobjects
            ]
            if any(update_possibilities):
                return mobjects[i:]
        return []

    def get_mobject_family_members(self):
        
        return self.camera.extract_mobject_family_members(self.mobjects)

    def progress_through_animations(self, animations):
        
        # Paint all non-moving objects onto the screen, so they don't
        # have to be rendered every frame
        moving_mobjects = self.get_moving_mobjects(*animations)
        self.update_frame(excluded_mobjects=moving_mobjects)
        static_image = self.get_frame()
        last_t = 0
        for t in self.get_animation_time_progression(animations):
            dt = t - last_t
            last_t = t
            for animation in animations:
                animation.update_mobjects(dt)
                alpha = t / animation.run_time
                animation.interpolate(alpha)
            self.update_mobjects(dt)
            self.update_frame(moving_mobjects, static_image)
            self.add_frames(self.get_frame())

    def update_frame(
            self,
            mobjects=None,
            background=None,
            include_submobjects=True,
            ignore_skipping=True,
            **kwargs):
        
        if self.skip_animations and not ignore_skipping:
            return
        if mobjects is None:
            mobjects = list_update(
                self.mobjects,
                self.foreground_mobjects,
            )
        if background is not None:
            self.set_camera_pixel_array(background)
        else:
            self.reset_camera()

        kwargs["include_submobjects"] = include_submobjects
        self.capture_mobjects_in_camera(mobjects, **kwargs)

    def get_frame(self):
        
        return array(self.camera.get_pixel_array())

    def add_frames(self, *frames):
        
        dt = 1 / self.camera.frame_rate
        self.increment_time(len(frames) * dt)
        if self.skip_animations:
            return
        for frame in frames:
            self.file_writer.write_frame(frame)
    
    def increment_time(self, d_time):
        
        self.time += d_time

    def get_animation_time_progression(self, animations):
        
        run_time = self.get_run_time(animations)
        time_progression = self.get_time_progression(run_time)
        time_progression.set_description("".join([
            "Animation {}: ".format(self.num_plays),
            str(animations[0]),
            (", etc." if len(animations) > 1 else ""),
        ]))
        return time_progression

    def get_run_time(self, animations):
        
        return max([animation.run_time for animation in animations])

    def get_time_progression(self, run_time, n_iterations=None, override_skip_animations=False):
        
        if self.skip_animations and not override_skip_animations:
            times = [run_time]
        else:
            step = 1 / self.camera.frame_rate
            times = arange(0, run_time, step)
        time_progression = ProgressDisplay(
            times, total=n_iterations,
            leave=self.leave_progress_bars,
            ascii=False if platform.system() != 'Windows' else True
        )
        return time_progression

    def set_camera_pixel_array(self, pixel_array):
        
        self.camera.set_pixel_array(pixel_array)

    def finish_animations(self, animations):
        
        for animation in animations:
            animation.finish()
            animation.clean_up_from_scene(self)
        self.mobjects_from_last_animation = [
            anim.mobject for anim in animations
        ]
        if self.skip_animations:
            # TODO, run this call in for each animation?
            self.update_mobjects(self.get_run_time(animations))
        else:
            self.update_mobjects(0)

    def reset_camera(self):
        
        self.camera.reset()

    def capture_mobjects_in_camera(self, mobjects, **kwargs):
        
        self.camera.capture_mobjects(mobjects, **kwargs)

    def add_sound(self, sound_file, time_offset=0, gain=None, **kwargs):
        
        if self.skip_animations:
            return
        time = self.get_time() + time_offset
        self.file_writer.add_sound(sound_file, time, gain, **kwargs)

    def get_time(self):
        
        return self.time

    def tear_down(self):
        
        pass

    def get_image(self):
        
        return self.camera.get_image()

    def print_end_message(self):
        
        print("Played {} animations".format(self.num_plays))

    def z__str__(self):
        
        return self.__class__.__name__
    # TODO, remove this, and calls to this ZoomedScene

    def add_foreground_mobjects(self, *mobjects):
        
        self.foreground_mobjects = list_update(
            self.foreground_mobjects,
            mobjects
        )
        self.add(*mobjects)
        return self

    def add_foreground_mobject(self, mobject):
        
        return self.add_foreground_mobjects(mobject)

    def remove_foreground_mobjects(self, *to_remove):
        
        self.restructure_mobjects(to_remove, "foreground_mobjects")
        return self

    def remove_foreground_mobject(self, mobject):
        
        return self.remove_foreground_mobjects(mobject)

    # Only these methods should touch the camera
    def freeze_background(self):
        
        self.update_frame()
        self.set_camera(Cam(self.get_frame()))
        self.clear()

    def set_camera(self, camera):
        
        self.camera = camera

    def clear(self):
        
        self.mobjects = []
        self.foreground_mobjects = []
        return self

    def get_top_level_mobjects(self):
        
        # Return only those which are not in the family
        # of another mobject from the scene
        mobjects = self.get_mobjects()
        families = [m.get_family() for m in mobjects]

        def is_top_level(mobject):
            num_families = sum([
                (mobject in family)
                for family in families
            ])
            return num_families == 1
        return list(filter(is_top_level, mobjects))

    def get_mobjects(self):
        
        return list(self.mobjects)

    def set_camera_background(self, background):
        
        self.camera.set_background(background)

    def add_mobjects_among(self, values):
        
        """
        This is meant mostly for quick prototyping,
        e.g. to add all mobjects defined up to a point,
        call self.add_mobjects_among(locals().values())
        """
        self.add(*filter(
            lambda m: isinstance(m, Mobject),
            values
        ))
        return self

    def fadein(self, *mobjects, run_time=1, pre_time=0.5, post_time=1):
        
        self.wait(pre_time)
        self.play(FadeIn(Group(*mobjects)))
        self.wait(post_time)
        return self

    def fadeout(self, mobjects=None, run_time=1, pre_time=0.5, post_time=0.5, exclude_mobjs=None):
        if mobjects is None:
            mobjarray = self.mobjects
            #mobjarray+=self.foreground_mobjects
        else:
            mobjarray=list(mobjects)
        if exclude_mobjs == "foreground" and self.foreground_mobjects:
            for each in self.foreground_mobjects:
                mobjarray.remove(each)
        elif isinstance(exclude_mobjs, (Mobject, Group)):
            for each in exclude_mobjs:
                mobjarray.remove(each)
            #self.foreground_mobjects.remove(exclude_mobjs)
        else:
            self.foreground_mobjects = []
        self.wait(pre_time)
        #self.play(FadeOut(Group(*[each.suspend_updating() for each in mobjarray]), run_time=run_time))
        self.play(DFadeOut(Group(*mobjarray).suspend_updating(), run_time=run_time))
        self.wait(post_time)
        return self

    def grow(self, *mobject_or_chars, run_time=1, pre_time=0.5, post_time=1, **kwargs):
        
        """
        if not isinstance(mobject_or_chars, (list,tuple,ndarray)):
            mobject_or_chars=[mobject_or_chars]
        mobject = Group(*[MobjectOrChars(each) for each in mobject_or_chars])
        """
        mobject = GroupedMobject(mobject_or_chars)
        keys = ["shift", "scale", "move_to"]
        [exec("mobject."+key+"(["+','.join(str(x) for x in kwargs.get(key))+"])",
              {"mobject": mobject}) for key in keys if key in kwargs]
        self.wait(pre_time)
        self.play(GrowFromCenter(mobject))
        self.wait(post_time)
        return self

    def diminish(self, *mobjects, run_time=1, pre_time=0.5, post_time=1, **kwargs):
        '''
        if not isinstance(mobject_or_chars, (list, tuple, ndarray)):
            mobject_or_chars = [mobject_or_chars]
        mobject = VGroup(*[MobjectOrChars(each) for each in mobject_or_chars])
        '''
        if not mobjects:
            mobjects=ListedMobject(self.mobjects)
        imobjs=Group()
        vmobjs=VGroup()
        mobjs=Group()
        for each in mobjects:
            if isinstance(each, ImageMobjectGroup):
                imobjs.add(each)
            elif isinstance(each, VMobject):
               vmobjs.add(each)
            else:
                mobjs.add(each)
        '''
        vmobjs=VGroup(*[each.remove_from_group(mobjects) for each in mobjects if isinstance(each, VMobject)])
        mobjs=Group(*[each for each in mobjects if isinstance(each, Mobject)])
        '''
        #mobject = GroupedMobject(mobjects)
        #keys = ["shift"]
        #[exec("mobject."+key+"(["+','.join(str(x) for x in kwargs.get(key))+"])",
        #      {"mobject": mobject}) for key in keys if key in kwargs]
        #self.wait(pre_time)
        self.play(AnimationGroup(DiminishToPoint(vmobjs,[0,0,0]),DFadeOut(mobjs),ShrinkToCenter(imobjs)))
        self.wait(post_time)
        return self

    def create(self, *mobject_or_chars, pre_time=0.5, post_time=1, **kwargs):
        
        if not isinstance(mobject_or_chars, (list, tuple, ndarray)):
            mobject_or_chars = [mobject_or_chars]
        mobject = Group(*[MobjectOrChars(each) for each in mobject_or_chars])
        keys = ["shift"]
        [exec("mobject."+key+"(["+','.join(str(x) for x in kwargs.get(key))+"])",
              {"mobject": mobject}) for key in keys if key in kwargs]
        self.wait(pre_time)
        self.play(ShowCreation(mobject), **kwargs)
        self.wait(post_time)
        return self

    def onebyone(self, *mobject_or_chars, run_time=1, pre_time=0.5, post_time=1, **kwargs):
        
        if not isinstance(mobject_or_chars, (list, tuple, ndarray)):
            mobject_or_chars = [mobject_or_chars]
        mobject = Group(*[MobjectOrChars(each) for each in mobject_or_chars])
        keys = ["shift"]
        [exec("mobject."+key+"(["+','.join(str(x) for x in kwargs.get(key))+"])",
              {"mobject": mobject}) for key in keys if key in kwargs]
        self.wait(pre_time)
        self.play(ShowSubmobjectsOneByOne(mobject))
        self.wait(post_time)
        return self

    def set_variables_as_attrs(self, *objects, **newly_named_objects):
        
        """
        This method is slightly hacky, making it a little easier
        for certain methods (typically subroutines of construct)
        to share local variables.
        """
        caller_locals = inspect.currentframe().f_back.f_locals
        for key, value in list(caller_locals.items()):
            for o in objects:
                if value is o:
                    setattr(self, key, value)
        for key, value in list(newly_named_objects.items()):
            setattr(self, key, value)
        return self

    def get_attrs(self, *keys):
        
        return [getattr(self, key) for key in keys]

    def bring_to_front(self, *mobjects):
        
        self.add(*mobjects)
        return self

    def bring_to_back(self, *mobjects):
        
        self.remove(*mobjects)
        self.mobjects = list(mobjects) + self.mobjects
        return self

    def pin(self, *mobjects, **kwargs):
        
        for each in mobjects:
            if isinstance(each, (Group)):
                each.add_updater(
                    lambda group: self.camera.add_fixed_orientation_mobjects(group, **kwargs))
            elif isinstance(each, (Mobject)):
                self.camera.add_fixed_orientation_mobjects(each, **kwargs)
            elif isinstance(each, Animation):
                self.camera.add_fixed_orientation_mobjects(each.mobject)
                self.play(each, **kwargs)

    def post(self, *mobjects, foreground=False, **kwargs):
        
        for each in mobjects:
            if foreground:
                if isinstance(each, (Group,Mobject)):
                    each.add_as_foreground(self)
                elif isinstance(each, Animation):
                    each.mobject.add_as_foreground(self)
            if isinstance(each, (Group)):
                each.add_updater(
                    lambda group: self.camera.add_fixed_in_frame_mobjects(group))
            elif isinstance(each, (Mobject)):
                self.camera.add_fixed_in_frame_mobjects(each)
            elif isinstance(each, Animation):
                self.camera.add_fixed_in_frame_mobjects(each.mobject)
                self.play(each, **kwargs)

    def get_mobject_copies(self):
        
        return [m.copy() for m in self.mobjects]

    # add

    def idle_stream(self):
        
        self.file_writer.idle_stream()

    def clean_up_animations(self, *animations):
        
        for animation in animations:
            animation.clean_up_from_scene(self)
        return self

    def get_mobjects_from_last_animation(self):
        
        if hasattr(self, "mobjects_from_last_animation"):
            return self.mobjects_from_last_animation
        return []

    def wait_until(self, stop_condition, max_time=60):
        
        self.wait(max_time, stop_condition=stop_condition)

    def force_skipping(self):
        
        self.original_skipping_status = self.skip_animations
        self.skip_animations = True
        return self

    def revert_to_original_skipping_status(self):
        
        if hasattr(self, "original_skipping_status"):
            self.skip_animations = self.original_skipping_status
        return self

    def show_frame(self):
        
        self.update_frame(ignore_skipping=True)
        self.get_image().show()

    # TODO, this doesn't belong in Scene, but should be
    # part of some more specialized subclass optimized
    # for livestreaming
    def tex(self, latex):
        
        eq = TextMobject(latex)
        anims = []
        anims.append(Write(eq))
        for mobject in self.mobjects:
            anims.append(ApplyMethod(mobject.shift, 2 * UP))
        self.play(*anims)


    def apply_method(self,func, *args,run_time=0.001, **kwargs):
        '''Dummy animate method
        '''
        #return ApplyMethod(func, *args,run_time=run_time, **kwargs)
        func( *args, **kwargs)
        return Animation(Mobject(),run_time=0.001)

    def animate(self, *animations,run_time=0.001, **kwargs):
        '''Dummy animate AnimByAnim
        '''
        return AnimByAnim(*animations,  fix_time=run_time,retain=True,**kwargs)

    def print(self,*args):
        print(*args)
        return Display(Mobject())


class EndSceneEarlyException(Exception):
    pass
