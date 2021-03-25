import inspect
import platform
import random as rrandom
import warnings

from numpy import arange, array, max, ndarray, random
from tqdm import tqdm as ProgressDisplay

from manimlib.animation.animation import Animation,  prepare_animation, _AnimationBuilder
from manimlib.animation.creation import ShowCreation, ShowSubmobjectsOneByOne, Write
from manimlib.animation.fading import FadeIn, FadeOut
from manimlib.animation.growing import DiminishToCenter, GrowFromCenter  # ,
from manimlib.animation.transform import ApplyMethod, MoveToTarget
from manimlib.basic.basic_mobject import GroupedMobject, MobjectOrChars
from manimlib.camera.camera import Camera
from manimlib.camera.three_d_camera import ThreeDCamera
from manimlib.camera.moving_camera import MovingCamera
from manimlib.scene.window_scene import WindowScene
from manimlib.constants import DEFAULT_WAIT_TIME, FRAME_HEIGHT, FRAME_WIDTH, UP, DEGREES
from manimlib.container.container import Container
from manimlib.mobject.mobject import Group, Mobject
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.scene.scene_file_writer import SceneFileWriter
from manimlib.utils.iterables import list_update
from manimlib.utils.config_ops import digest_config


class Scene(WindowScene):
    CONFIG = {
        "camera_class": Camera,
        # Camera3D
        "ambient_camera_rotation": None,
        "default_camera_orientation_kwargs": {
            "phi": 70 * DEGREES,
            "theta": -110 * DEGREES,
            # "phi": 90 * DEGREES,
            # "theta": 90 * DEGREES,
            # "gamma ": 0 * DEGREES,
        },
        "default_angled_camera_orientation_kwargs": {
            "phi": 70 * DEGREES,
            "theta": -135 * DEGREES,
        }
    }

    def __init__(self, **kwargs):

        digest_config(self, kwargs)
        self.init_config()
        super().__init__(**kwargs)

    def init_config(self):

        self.default_angled_camera_orientation_kwargs = vars(
            self)['default_angled_camera_orientation_kwargs']
        self.default_camera_orientation_kwargs = vars(
            self)['default_camera_orientation_kwargs']

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
        # camera3d
        if self.camera_class == ThreeDCamera:
            camera_mobjects = self.camera.get_value_trackers()
            if any([cm in moving_mobjects for cm in camera_mobjects]):
                return self.mobjects
        # camera3d
        return moving_mobjects

    # Camera3D

    def set_camera_orientation(self, phi=None, theta=None, distance=None, gamma=None):
        if phi is not None:
            self.camera.set_phi(phi)
        if theta is not None:
            self.camera.set_theta(theta)
        if distance is not None:
            self.camera.set_distance(distance)
        if gamma is not None:
            self.camera.set_gamma(gamma)

    def begin_ambient_camera_rotation(self, rate=0.02):
        # TODO, use a ValueTracker for rate, so that it
        # can begin and end smoothly
        self.camera.theta_tracker.add_updater(
            lambda m, dt: m.increment_value(rate * dt)
        )
        self.add(self.camera.theta_tracker)

    def stop_ambient_camera_rotation(self):
        self.camera.theta_tracker.clear_updaters()
        self.remove(self.camera.theta_tracker)

    def move_camera(self,
                    phi=None,
                    theta=None,
                    distance=None,
                    gamma=None,
                    frame_center=None,
                    added_anims=[],
                    **kwargs):
        anims = []
        value_tracker_pairs = [
            (phi, self.camera.phi_tracker),
            (theta, self.camera.theta_tracker),
            (distance, self.camera.distance_tracker),
            (gamma, self.camera.gamma_tracker),
        ]
        for value, tracker in value_tracker_pairs:
            if value is not None:
                anims.append(
                    ApplyMethod(tracker.set_value, value, **kwargs)
                )
        if frame_center is not None:
            anims.append(ApplyMethod(
                self.camera.frame_center.move_to,
                frame_center
            ))

        self.play(*anims + added_anims)

    def add_fixed_orientation_mobjects(self, *mobjects, **kwargs):
        self.add(*mobjects)
        self.camera.add_fixed_orientation_mobjects(*mobjects, **kwargs)

    def add_fixed_in_frame_mobjects(self, *mobjects):
        self.add(*mobjects)
        self.camera.add_fixed_in_frame_mobjects(*mobjects)

    def remove_fixed_orientation_mobjects(self, *mobjects):
        self.camera.remove_fixed_orientation_mobjects(*mobjects)

    def remove_fixed_in_frame_mobjects(self, *mobjects):
        self.camera.remove_fixed_in_frame_mobjects(*mobjects)

    ##
    def set_to_default_angled_camera_orientation(self, **kwargs):
        config = dict(self.default_camera_orientation_kwargs)
        config.update(kwargs)
        self.set_camera_orientation(**config)


class zScene(WindowScene):
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


class EndSceneEarlyException(Exception):
    pass
