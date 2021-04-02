import operator as op

from manimlib.constants import *
from manimlib.mobject.geometry import Line
from manimlib.mobject.numbers import DecimalNumber
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.utils.bezier import interpolate
from manimlib.utils.config_ops import digest_config
from manimlib.utils.config_ops import merge_dicts_recursively
from manimlib.utils.iterables import list_difference_update
from manimlib.utils.simple_functions import fdiv
from manimlib.utils.space_ops import normalize


class NumberLine(Line):
    CONFIG = {
        "color": LIGHT_GREY,  # new GREY_B
        "stroke_width": 2,
        # List of 2 or 3 elements, x_min, x_max, step_size
        "x_range": [-FRAME_X_RADIUS, FRAME_X_RADIUS, 1],
        "x_min": -FRAME_X_RADIUS,
        "x_max": FRAME_X_RADIUS,
        # How big is one one unit of this number line in terms of absolute spacial distance
        "unit_size": 1,
        "width": None,
        "include_ticks": True,
        "tick_size": 0.1,
        "longer_tick_multiple": 2,  # new 1.5
        "tick_offset": 0,
        "tick_frequency": 1,
        # Defaults to value near x_min s.t. 0 is a tick
        # TODO, rename this
        "leftmost_tick": None,
        # Change name
        "numbers_with_elongated_ticks": [0],  # new no 0
        "include_numbers": False,
        "line_to_number_direction": DOWN,
        "numbers_to_show": None,
        "number_at_center": 0,
        "number_scale_val": 0.75,
        "label_direction": DOWN,
        "line_to_number_buff": MED_SMALL_BUFF,
        "include_tip": False,
        # "tip_config": {"width": 0.25,"length": 0.25,},
        # "tip_width": 0.25,
        # "tip_height": 0.25,
        "decimal_number_config": {
            "num_decimal_places": 0,
            "font_size": 36,
        },
        "numbers_to_exclude": None,
        "exclude_zero_from_default_numbers": False,
    }

    def __init__(self, x_range=None, **kwargs):
        digest_config(self, kwargs)
        self.line_to_number_direction = kwargs.get(
            "label_direction", self.line_to_number_direction)
        if x_range is None:
            x_range = self.x_range
        if len(x_range) == 2:
            x_range = [*x_range, 1]

        x_min, x_max, x_step = x_range
        # A lot of old scenes pass in x_min or x_max explicitly,
        # so this is just here to keep those workin
        self.x_min = kwargs.get("x_min", x_min)
        self.x_max = kwargs.get("x_max", x_max)
        self.x_step = kwargs.get("x_step", x_step or 1)
        super().__init__(self.x_min * RIGHT, self.x_max * RIGHT, **kwargs)
        #start = self.unit_size * self.x_min * RIGHT
        #end = self.unit_size * self.x_max * RIGHT
        #Line.__init__(self, start, end, **kwargs)
        # self.shift(-self.number_to_point(self.number_at_center))
        # self.init_leftmost_tick()
        if self.width:
            self.set_width(self.width)
            self.unit_size = self.get_unit_size()
        else:
            self.scale(self.unit_size)
        self.center()

        if self.include_tip:
            self.add_tip()
            self.tip.set_stroke(
                self.stroke_color,
                self.stroke_width,
            )
        if self.include_ticks:
            self.add_ticks()
            # self.add_tick_marks()
        if self.include_numbers:
            self.add_numbers(excluding=self.numbers_to_exclude)

    def get_tick_range(self):
        if self.x_min==-FRAME_X_RADIUS and self.x_max==FRAME_X_RADIUS:
           x_min=int(self.x_min)
           x_max=int(self.x_max)
        else:
           x_min=self.x_min
           x_max=self.x_max
        if not self.include_tip:
            x_max = x_max + self.x_step
        return np.arange(x_min,x_max,self.x_step)


    def add_ticks(self):
        ticks = VGroup()
        for x in self.get_tick_range():
            size = self.tick_size
            if x in self.numbers_with_elongated_ticks:
                size *= self.longer_tick_multiple
            ticks.add(self.get_tick(x, size))
        self.add(ticks)
        self.ticks = ticks

    def get_tick(self, x, size=None):
        if size is None:
            size = self.tick_size
        result = Line(size * DOWN, size * UP)
        result.rotate(self.get_angle())
        result.move_to(self.number_to_point(x))
        result.match_style(self)
        return result

    def get_tick_marks(self):
        try:
            return self.ticks
        except:
            return VGroup(
                *self.tick_marks,
                *self.big_tick_marks,
            )

    def number_to_point(self, number):
        alpha = float(number - self.x_min) / (self.x_max - self.x_min)
        return interpolate(
            self.get_start(), self.get_end(), alpha
        )

    def point_to_number(self, point):
        start, end = self.get_start_and_end()
        unit_vect = normalize(end - start)
        proportion = fdiv(
            np.dot(point - start, unit_vect),
            np.dot(end - start, unit_vect),
        )
        return interpolate(self.x_min, self.x_max, proportion)

    def n2p(self, number):
        """Abbreviation for number_to_point"""
        return self.number_to_point(number)

    def p2n(self, point):
        """Abbreviation for point_to_number"""
        return self.point_to_number(point)

    def get_unit_size(self):
        return self.get_length() / (self.x_max - self.x_min)
        # return (self.x_max - self.x_min) / self.get_length()

    def get_number_mobject(self, x,
                           direction=None,
                           buff=None,
                           scale_val=None,
                           # number_config=None,
                           **number_config):
        number_config = merge_dicts_recursively(
            self.decimal_number_config,
            number_config or {},
        )
        if scale_val is None:
            scale_val = self.number_scale_val
        if direction is None:
            direction = self.line_to_number_direction
            #direction = self.label_direction
        if buff is None:
            buff = self.line_to_number_buff
        #buff = buff or self.line_to_number_buff

        num_mob = DecimalNumber(x, **number_config)
        num_mob.scale(scale_val)
        num_mob.next_to(
            self.number_to_point(x),
            direction=direction,
            buff=buff
        )
        if x < 0 and self.line_to_number_direction[0] == 0:
            # Align without the minus sign
            num_mob.shift(num_mob[0].get_width() * LEFT / 2)
        return num_mob

    def add_numbers(self, *numbers, excluding=None, font_size=24, x_values=None, **kwargs):
        if x_values is None:
            if len(numbers) == 1 and isinstance(numbers[0], list):
                x_values = (numbers[0])
            elif len(numbers) > 0 and not isinstance(numbers[0], list):
                x_values = list(numbers)
            else:
                x_values = self.get_tick_range()

        kwargs["font_size"] = font_size

        numbers = VGroup()
        for x in x_values:
            if self.numbers_to_exclude is not None and x in self.numbers_to_exclude:
                continue
            if excluding is not None and x in excluding:
                continue
            numbers.add(self.get_number_mobject(x, **kwargs))
        self.add(numbers)
        self.numbers = numbers
        return numbers
        '''
        self.numbers = self.get_number_mobjects(
            *numbers, **kwargs
        )
        self.add(self.numbers)
        return self
        '''

    def init_leftmost_tick(self):
        if self.leftmost_tick is None:
            self.leftmost_tick = op.mul(
                self.tick_frequency,
                np.ceil(self.x_min / self.tick_frequency)
            )

    def get_tick_numbers(self):
        u = -1 if self.include_tip else 1
        return np.arange(
            self.leftmost_tick,
            self.x_max + u * self.tick_frequency / 2,
            self.tick_frequency
        )

    def add_tick_marks(self):
        tick_size = self.tick_size
        self.tick_marks = VGroup(*[
            self.get_tick(x, tick_size)
            for x in self.get_tick_numbers()
        ])
        big_tick_size = tick_size * self.longer_tick_multiple
        self.big_tick_marks = VGroup(*[
            self.get_tick(x, big_tick_size)
            for x in self.numbers_with_elongated_ticks
        ])
        self.add(
            self.tick_marks,
            self.big_tick_marks,
        )

    def default_numbers_to_display(self):
        if self.numbers_to_show is not None:
            return self.numbers_to_show
        numbers = np.arange(
            np.floor(self.leftmost_tick),
            np.ceil(self.x_max),
        )
        if self.exclude_zero_from_default_numbers:
            numbers = numbers[numbers != 0]
        return numbers

    def get_number_mobjects(self, *numbers, **kwargs):
        if len(numbers) == 0:
            numbers = self.default_numbers_to_display()
        return VGroup(*[
            self.get_number_mobject(number, **kwargs)
            for number in numbers
        ])

    def get_labels(self):
        return self.get_number_mobjects()


class UnitInterval(NumberLine):
    CONFIG = {
        "x_range": [0, 1, 0.1],
        "x_min": 0,
        "x_max": 1,
        "unit_size": 6,  # new 10
        "tick_frequency": 0.1,
        "numbers_with_elongated_ticks": [0, 1],
        "number_at_center": 0.5,
        "decimal_number_config": {
            "num_decimal_places": 1,
        }
    }
