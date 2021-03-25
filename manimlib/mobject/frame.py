from manimlib.constants import *
from manimlib.mobject.geometry import Rectangle
from manimlib.mobject.mobject import Mobject
from manimlib.utils.config_ops import digest_config
from manimlib.container.container import Container
from manimlib.utils.space_ops import angle_of_vector
from manimlib.utils.space_ops import rotation_matrix_transpose_from_quaternion
from manimlib.utils.space_ops import rotation_matrix_transpose
from manimlib.utils.space_ops import quaternion_from_angle_axis
from manimlib.utils.space_ops import quaternion_mult

class ScreenRectangle(Rectangle):
    CONFIG = {
        "aspect_ratio": 16.0 / 9.0,
        "height": 4
    }

    def __init__(self, **kwargs):
        Rectangle.__init__(self, **kwargs)
        self.set_width(
            self.aspect_ratio * self.get_height(),
            stretch=True
        )


class FullScreenRectangle(ScreenRectangle):
    CONFIG = {
        "height": FRAME_HEIGHT,
    }


class FullScreenFadeRectangle(FullScreenRectangle):
    CONFIG = {
        "stroke_width": 0,
        "fill_color": BLACK,
        "fill_opacity": 0.7,
    }


class PictureInPictureFrame(Rectangle):
    CONFIG = {
        "height": 3,
        "aspect_ratio": 16.0 / 9.0
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        Rectangle.__init__(
            self,
            width=self.aspect_ratio * self.height,
            height=self.height,
            **kwargs
        )

class zDatumFrame(Mobject):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.init_frame(*args)
    def init_frame(self,*args):
        self.frame_width = args

        #self.frame_height = args[1]
        return self

class CameraFrame(ScreenRectangle):
    CONFIG = {
        "frame_shape": (FRAME_WIDTH, FRAME_HEIGHT),
        "center_point": ORIGIN,
        # Theta, phi, gamma
        "euler_angles": [0, 0, 0],
        "focal_distance": 2,

        "fixed_dimension": 0,  # width
        "default_frame_stroke_color": WHITE,
        "default_frame_stroke_width": 0,
        #"frame":None,
        "frame_height":FRAME_HEIGHT,

    }

    def __init__(self,**kwargs):
        digest_config(self, kwargs)
        ScreenRectangle.__init__(self,height=self.frame_height)
        self.set_stroke(
            self.default_frame_stroke_color,
            self.default_frame_stroke_width,
        )
        self.data["euler_angles"] = np.array(self.euler_angles, dtype=float)
        self.refresh_rotation_matrix()

    '''
    def init_data(self):
        super().init_data()
        self.data["euler_angles"] = np.array(self.euler_angles, dtype=float)
        self.refresh_rotation_matrix()

    def init_points(self):
        self.set_points([ORIGIN, LEFT, RIGHT, DOWN, UP])
        self.set_width(self.frame_shape[0], stretch=True)
        self.set_height(self.frame_shape[1], stretch=True)
        self.move_to(self.center_point)

    def to_default_state(self):
        self.center()
        self.set_height(FRAME_HEIGHT)
        self.set_width(FRAME_WIDTH)
        self.set_euler_angles(0, 0, 0)
        return self
    '''
    def get_euler_angles(self):
        return self.data["euler_angles"]
    
    def get_inverse_camera_rotation_matrix(self):
        return self.inverse_camera_rotation_matrix

    def refresh_rotation_matrix(self):
        # Rotate based on camera orientation
        theta, phi, gamma = self.get_euler_angles()
        quat = quaternion_mult(
            quaternion_from_angle_axis(theta, OUT, axis_normalized=True),
            quaternion_from_angle_axis(phi, RIGHT, axis_normalized=True),
            quaternion_from_angle_axis(gamma, OUT, axis_normalized=True),
        )
        self.inverse_camera_rotation_matrix = rotation_matrix_transpose_from_quaternion(quat)
    
    def rotate(self, angle, axis=OUT, **kwargs):
        curr_rot_T = self.get_inverse_camera_rotation_matrix()
        added_rot_T = rotation_matrix_transpose(angle, axis)
        new_rot_T = np.dot(curr_rot_T, added_rot_T)
        Fz = new_rot_T[2]
        phi = np.arccos(Fz[2])
        theta = angle_of_vector(Fz[:2]) + PI / 2
        partial_rot_T = np.dot(
            rotation_matrix_transpose(phi, RIGHT),
            rotation_matrix_transpose(theta, OUT),
        )
        gamma = angle_of_vector(np.dot(partial_rot_T, new_rot_T.T)[:, 0])
        self.set_euler_angles(theta, phi, gamma)
        return self
    
    def set_euler_angles(self, theta=None, phi=None, gamma=None):
        if theta is not None:
            self.data["euler_angles"][0] = theta
        if phi is not None:
            self.data["euler_angles"][1] = phi
        if gamma is not None:
            self.data["euler_angles"][2] = gamma
        self.refresh_rotation_matrix()
        return self
    '''
    def set_theta(self, theta):
        return self.set_euler_angles(theta=theta)

    def set_phi(self, phi):
        return self.set_euler_angles(phi=phi)

    def set_gamma(self, gamma):
        return self.set_euler_angles(gamma=gamma)

    def increment_theta(self, dtheta):
        self.data["euler_angles"][0] += dtheta
        self.refresh_rotation_matrix()
        return self

    def increment_phi(self, dphi):
        phi = self.data["euler_angles"][1]
        new_phi = clip(phi + dphi, 0, PI)
        self.data["euler_angles"][1] = new_phi
        self.refresh_rotation_matrix()
        return self

    def increment_gamma(self, dgamma):
        self.data["euler_angles"][2] += dgamma
        self.refresh_rotation_matrix()
        return self

    def get_shape(self):
        return (self.get_width(), self.get_height())

    def get_center(self):
        # Assumes first point is at the center
        return self.get_points()[0]

    def get_width(self):
        points = self.get_points()
        return points[2, 0] - points[1, 0]

    def get_height(self):
        points = self.get_points()
        return points[4, 1] - points[3, 1]

    def get_focal_distance(self):
        return self.focal_distance * self.get_height()

    def interpolate(self, *args, **kwargs):
        super().interpolate(*args, **kwargs)
        self.refresh_rotation_matrix()
    '''