import inspect
import platform
import random as rrandom
import warnings

from numpy import arange, array, max, ndarray, random
from tqdm import tqdm as ProgressDisplay

from manimlib.animation.animation import Animation,  prepare_animation,_AnimationBuilder
from manimlib.animation.creation import ShowCreation, ShowSubmobjectsOneByOne, Write
from manimlib.animation.fading import FadeIn, FadeOut
from manimlib.animation.growing import DiminishToCenter, GrowFromCenter  # ,
from manimlib.animation.transform import ApplyMethod, MoveToTarget
from manimlib.basic.basic_mobject import GroupedMobject, MobjectOrChars
from manimlib.camera.camera import Camera
from manimlib.camera.moving_camera import MovingCamera
from manimlib.scene.window_scene import WindowScene
from manimlib.constants import DEFAULT_WAIT_TIME, FRAME_HEIGHT, FRAME_WIDTH, UP
from manimlib.container.container import Container
from manimlib.mobject.mobject import Group, Mobject
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.scene.scene_file_writer import SceneFileWriter
from manimlib.utils.iterables import list_update


class Scene(WindowScene):
    '''
    CONFIG = {
        "camera_class": MovingCamera
    }

    def setup(self):
        WindowScene.setup(self)
        assert(isinstance(self.camera, MovingCamera))
        self.camera_frame = self.camera.frame
        # Hmm, this currently relies on the fact that MovingCamera
        # willd default to a full-sized frame.  Is that okay?
        return self
    '''
    def get_moving_mobjects(self, *animations):
        moving_mobjects = WindowScene.get_moving_mobjects(self, *animations)
        all_moving_mobjects = self.camera.extract_mobject_family_members(
            moving_mobjects
        )
        movement_indicators = self.camera.get_mobjects_indicating_movement()
        for movement_indicator in movement_indicators:
            if movement_indicator in all_moving_mobjects:
                # When one of these is moving, the camera should
                # consider all mobjects to be moving
                return list_update(self.mobjects, moving_mobjects)
        return moving_mobjects
    #pass
    

class EndSceneEarlyException(Exception):
    pass
