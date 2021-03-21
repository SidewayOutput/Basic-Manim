import numpy as np

from manimlib.constants import RH, FRAME_WIDTH, FRAME_HEIGHT, ORIGIN, OUT, LEFT, RIGHT, DOWN, UP
from manimlib.utils.config_ops import digest_config

# Currently, this is only used by both Scene and Mobject.
# Still, we abstract its functionality here, albeit purely nominally.
# All actual implementation has to be handled by derived classes for now.

# TODO: Move the "remove" functionality of Scene to this class


class Container(object):
    CONFIG = {
        "datum_origin": [0, 0, 0],
        "datum_coord": RH,
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        self.init_datum(datum_origin=Container.CONFIG['datum_origin'],
                        datum_coord=Container.CONFIG['datum_coord'])

    def init_datum(self, **kwargs):
        self.datum_origin = kwargs['datum_origin']
        self.datum_coord = kwargs['datum_coord']

    def init_frame(self, **kwargs):
        self.frame_width = kwargs['frame_width']
        self.frame_height = kwargs['frame_height']
        self.frame_center=kwargs['frame_center']

    def add(self, *items):
        raise Exception(
            "Container.add is not implemented; it is up to derived classes to implement")

    def remove(self, *items):
        raise Exception(
            "Container.remove is not implemented; it is up to derived classes to implement")
