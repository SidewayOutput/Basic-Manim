from manimlib.camera.three_d_camera import ThreeDCamera
from manimlib.constants import DEGREES
from manimlib.constants import PRODUCTION_QUALITY_CAMERA_CONFIG
from manimlib.mobject.coordinate_systems import ThreeDAxes
from manimlib.mobject.geometry import Line
from manimlib.mobject.three_dimensions import Sphere
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VectorizedPoint
from manimlib.scene.scene import Scene
from manimlib.utils.config_ops import digest_config
from manimlib.utils.config_ops import merge_dicts_recursively


class ThreeDScene(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }


class SpecialThreeDScene(ThreeDScene):
    CONFIG = {
        "cut_axes_at_radius": True,
        "camera_config": {
            "should_apply_shading": True,
            "exponential_projection": True,
        },
        "three_d_axes_config": {
            "num_axis_pieces": 1,
            "number_line_config": {
                "unit_size": 2,
                "tick_frequency": 1,
                "numbers_with_elongated_ticks": [0, 1, 2],
                "stroke_width": 2,
            }
        },
        "sphere_config": {
            "radius": 2,
            "resolution": (24, 48),
        },
        "default_angled_camera_position": {
            "phi": 70 * DEGREES,
            "theta": -110 * DEGREES,
        },
        # When scene is extracted with -l flag, this
        # configuration will override the above configuration.
        "low_quality_config": {
            "camera_config": {
                "should_apply_shading": False,
            },
            "three_d_axes_config": {
                "num_axis_pieces": 1,
            },
            "sphere_config": {
                "resolution": (12, 24),
            }
        }
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        self.low_quality_config = vars(self)['low_quality_config']
        self.three_d_axes_config = vars(self)['three_d_axes_config']
        self.cut_axes_at_radius = vars(self)['cut_axes_at_radius']
        self.sphere_config = vars(self)['sphere_config']
        self.default_angled_camera_position = vars(self)['default_angled_camera_position']
        if self.camera_config["pixel_width"] == PRODUCTION_QUALITY_CAMERA_CONFIG["pixel_width"]:
            config = {}
        else:
            config = self.low_quality_config
        config = merge_dicts_recursively(config, kwargs)
        ThreeDScene.__init__(self, **config)

    def get_axes(self):
        axes = ThreeDAxes(**self.three_d_axes_config)
        for axis in axes:
            if self.cut_axes_at_radius:
                p0 = axis.get_start()
                p1 = axis.number_to_point(-1)
                p2 = axis.number_to_point(1)
                p3 = axis.get_end()
                new_pieces = VGroup(
                    Line(p0, p1), Line(p1, p2), Line(p2, p3),
                )
                for piece in new_pieces:
                    piece.shade_in_3d = True
                new_pieces.match_style(axis.pieces)
                axis.pieces.submobjects = new_pieces.submobjects
            for tick in axis.tick_marks:
                tick.add(VectorizedPoint(
                    1.5 * tick.get_center(),
                ))
        return axes

    def get_sphere(self, **kwargs):
        config = merge_dicts_recursively(self.sphere_config, kwargs)
        return Sphere(**config)

    def get_default_camera_position(self):
        return self.default_angled_camera_position

    def set_camera_to_default_position(self):
        self.set_camera_orientation(
            **self.default_angled_camera_position
        )
