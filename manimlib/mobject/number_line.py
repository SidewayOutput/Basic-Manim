from manimlib.basic.basic_geometry import GeomLine
from manimlib.basic.basic_math import baseceil, basefloor, exp10, funcceil, funcfloor, linear, log10, np
from manimlib.constants import DOWN, FRAME_X_RADIUS, LEFT, LIGHT_GREY, MED_SMALL_BUFF, RIGHT, UP
from manimlib.mobject.numbers import DecimalNumber
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.utils.bezier import interpolate
from manimlib.utils.config_ops import digest_config, merge_dicts_recursively 
from manimlib.utils.simple_functions import fdiv
from manimlib.utils.space_ops import normalize


class NumberLine(GeomLine):
    '''x_range=None, **kwargs\n
    [x_range;real line range with step=[-FRAME_X_RADIUS, FRAME_X_RADIUS, 1]]-->default
    '''
    def ICONFIG():
        return {
            "color": LIGHT_GREY,  # new GREY_B
            "stroke_width": 2,
            "unit_size": 1,  # unit_size=width/|x_range|
            "width": None,  # length
            "line_func": linear,
            "line_inv_func": linear,
            "include_tip": False,

            # min, max, step-->line_min,line_max,tick_step
            "x_range": [-FRAME_X_RADIUS, FRAME_X_RADIUS, 1],
            "tick_frequency": None,#x_step???
            "subdivision": 2,
            "leftmost_tick": None,  # specify num_tick>default x_min
            "leftmost_outer": True,  # show outer subdivision tick
            "leftmost_number": None,  # specity num>num_tick
            "rightmost_tick": None,  # specify num_tick<default x_max
            "rightmost_outer": True,  # show outer subdivision tick
            "rightmost_number": None,  # specity num<num_tick
            "tip_head_tick":False,
            "tip_head_number":False,

            "include_ticks": True,
            "tick_size": 0.1,
            "longer_tick_multiple": 2,  # new 1.5
            "longer_tick_size": None,  # numbers_with_shortened_ticks
            "shorter_tick_multiple": 0.7,
            "shorter_tick_size": None,
            "tick_offset": 0,   #???

            "include_numbers": False,
            "include_subnumbers": False,
            "numbers_with_elongated_ticks": [0],
            "numbers_with_shortened_ticks": [],
            "numbers_to_show": None,
            "number_at_center": 0,
            "line_to_number_direction": list(DOWN),
            "number_scale_val": 0.75,
            "line_to_number_buff": MED_SMALL_BUFF,
            "subnumbers_to_show": None,
            "subnumber_scale_val": 0.6,
            "decimal_number_config": {
                "num_decimal_places": 0,
                # "font_size": 36,
            },
            "numbers_to_exclude": None,
            "exclude_zero_from_default_numbers": False,

            # Change name
            # "label_direction": DOWN,
            # "tip_config": {"width": 0.25,"length": 0.25,},
            # "tip_width": 0.25,
            # "tip_height": 0.25,
            "ticks_pos":[],
            "ticks_size":[],
            "ticks":VGroup(),
            "nums_pos":[],
            "nums":VGroup(),
            "accuracy": 8,
        }
    CONFIG = ICONFIG()

    def __init__(self, x_range=None, **kwargs):
        self.init_cvars(NumberLine.ICONFIG(), kwargs)
        digest_config(self, kwargs)
        self.init_x_range(x_range, **kwargs)
        super().__init__(self.x_min * RIGHT, self.x_max * RIGHT, **kwargs)
        if self.width:
            self.unit_size = self.width / (self.x_max - self.x_min)
        self.scale(self.unit_size).center()
        self.longer_tick_size = self.longer_tick_size or self.tick_size * \
            self.longer_tick_multiple
        self.shorter_tick_size = self.shorter_tick_size or self.tick_size * \
            self.shorter_tick_multiple
        if self.include_tip:
            self.add_tip()
            self.tip.set_stroke(*self.get_stroke())
        if self.include_ticks or self.include_numbers:
            self.init_ticks_nums_pos()
            if self.include_ticks:
                #self.longer_tick_size = self.longer_tick_size or self.tick_size * \
                #    self.longer_tick_multiple
                #self.shorter_tick_size = self.shorter_tick_size or self.tick_size * \
                #    self.shorter_tick_multiple
                self.add(self.get_ticks())
            if self.include_numbers:
                self.line_to_number_direction = kwargs.get(
                    "label_direction", self.line_to_number_direction)
                #self.add_numbers(excluding=self.numbers_to_exclude)
                self.add_numbers(excluding=self.numbers_to_exclude)

    def init_x_range(self, x_range, **kwargs):
        """init line and step"""
        self.x_step = self.tick_frequency or 1
        if x_range is None or len(x_range) > 3:
            x_min, x_max, x_step = self.x_range
        elif isinstance(x_range, (int, float)):
            x_min, x_max, x_step = -x_range, x_range, self.x_step
        elif len(x_range) == 1:
            x_min, x_max, x_step = -x_range[0], x_range[0], self.x_step
        elif len(x_range) == 2:
            x_min, x_max, x_step = [*x_range, self.x_step]
        else:
            x_min, x_max, x_step = x_range
        # A lot of old scenes pass in x_min or x_max explicitly,
        # so this is just here to keep those workin
        self.x_min = kwargs.get("x_min", x_min)
        self.x_max = kwargs.get("x_max", x_max)
        self.x_step = kwargs.get("x_step", x_step or self.x_step)

    def next_x_step(self, x):
        """next x"""
        return round(x+self.x_step, self.accuracy)

    def prev_x_step(self, x):
        """prev x"""
        return round(x-self.x_step, self.accuracy)

    def x_ceil(self, x):
        return baseceil(x, self.x_step)

    def x_floor(self, x):
        return basefloor(x, self.x_step)

    def x_round(self, x):
        return baseround(x, self.x_step)

    def init_x_limits(self):
        '''init major limits'''
        x_min = self.x_ceil(self.x_min)
        x_max = self.x_floor(self.x_max)
        return [x_min, x_max]

    def init_ticks_nums_pos(self):
        '''generate tick and number ranges'''
        x_min, x_max = self.init_x_limits()
        if self.leftmost_tick is not None:
            x_min = max(x_min, self.x_ceil(self.leftmost_tick))
        else:
            self.leftmost_tick=x_min
        if self.leftmost_outer:
            tick_min = self.x_min
            x = self.prev_x_step(x_min)
        else:
            tick_min = x_min
            x = x_min
        if self.leftmost_number is not None:
            num_min = max(x_min, self.x_ceil(self.leftmost_number))
        else:
            num_min = x_min
        if self.include_tip:
            tip_end = self.p2n(self.n2p(self.x_max) -
                               self.get_tip().get_length())
        else:
            tip_end = self.x_max
        if self.rightmost_tick is not None:
            x_max = min(x_max, self.x_floor(self.rightmost_tick))

        if self.tip_head_tick:
            tip_end = self.x_max
        if self.rightmost_outer:
            tick_max = tip_end
        else:
            tick_max = x_max
        if self.tip_head_number:
            num_max = x_max
        else:
            num_max = min(x_max, tip_end)
        if self.rightmost_number is not None:
            num_max = min(num_max, self.x_floor(self.rightmost_number))
        if self.subdivision is None or self.subdivision < 1:
            self.subdivision = 1
        #self.nums_pos = []
        #self.ticks_pos = []
        while self.x_max > x:
            tmp = x
            x = self.next_x_step(x)
            subdivision = list(np.round(np.linspace(
                tmp, x, self.subdivision+1), self.accuracy))
            if subdivision[-1] > tick_max:
                subdivision = [
                    each for each in subdivision if each <= tick_max]
                self.numbers_with_shortened_ticks += subdivision[1:]
            elif subdivision[0] < tick_min:
                subdivision = [
                    each for each in subdivision if each >= tick_min]
                self.numbers_with_shortened_ticks += subdivision[:-1]
                self.ticks_pos += subdivision[:1]
            else:
                self.numbers_with_shortened_ticks += subdivision[1:-1]
            self.ticks_pos += subdivision[1:]
            if x >= num_min and x <= num_max:
                self.nums_pos.append(x)
        return [self.ticks_pos, self.nums_pos]

    def init_ticks(self):
        '''init all mobj ticks as one VGroup'''
        for x in self.get_ticks_pos():
            if x in self.numbers_with_elongated_ticks:
                self.ticks_size += [self.longer_tick_size]
            elif x in self.numbers_with_shortened_ticks:
                self.ticks_size += [self.shorter_tick_size]
            else:
                self.ticks_size += [self.tick_size]
            self.ticks.add(self.get_tick(x, self.ticks_size[-1]))
        return self.ticks

    def get_ticks(self):
        '''return ticks'''
        if not self.ticks:
            self.init_ticks()
        return self.ticks

    def get_tick(self, x, size=None):
        if size is None:
            size = self.tick_size
        result = GeomLine(size * DOWN, size * UP)
        result.rotate(self.get_angle())
        result.move_to(self.number_to_point(x))
        result.match_style(self)
        return result

    def get_ticks_pos(self):
        '''return ticks_pos'''
        if not self.ticks_pos:
            self.init_ticks_nums_pos()
        return self.ticks_pos

    def get_ticks_size(self):
        '''return ticks_size'''
        if not self.ticks_size:
            self.init_ticks()
        return self.ticks_size

    def add_numbers(self, *numbers, excluding=None, font_size=24, x_values=None, **kwargs):
        if x_values is None:
            if numbers is not None:
                if len(numbers) == 1 and isinstance(numbers[0], list):
                    x_values = (numbers[0])
                if len(numbers) == 1 and numbers[0] is None:
                    x_values = self.nums_pos
                elif len(numbers) > 0 and not isinstance(numbers[0], list):
                    x_values = list(numbers)
                else:
                    x_values = self.nums_pos
            else:
                x_values = self.nums_pos
        kwargs["font_size"] = font_size
        for x in x_values:
            if self.numbers_to_exclude is not None and x in self.numbers_to_exclude:
                continue
            if excluding is not None and x in excluding:
                continue
            if x in self.numbers_with_shortened_ticks:
                kwargs["scale_val"] = self.subnumber_scale_val
            else:
                kwargs["scale_val"] = self.number_scale_val
            self.nums.add(self.get_number_mobject(x, **kwargs))
        self.add(self.nums)
        return self.nums

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

    def get_unit_size(self):
        return self.unit_size

    def number_to_point(self, number):

        alpha = float(self.line_func(number) - self.line_func(self.x_min)) / \
            (self.line_func(self.x_max) - self.line_func(self.x_min))
        return interpolate(
            self.get_start(), self.get_end(), alpha
        )

    def n2p(self, number):
        """number_to_point"""
        return self.number_to_point(number)

    def point_to_number(self, point):
        start, end = self.get_start_and_end()
        unit_vect = normalize(end - start)
        proportion = fdiv(
            np.dot(point - start, unit_vect),
            np.dot(end - start, unit_vect),
        )
        return self.line_inv_func(interpolate(self.line_func(self.x_min), self.line_func(self.x_max), proportion))

    def p2n(self, point):
        """Abbreviation for point_to_number"""
        return self.point_to_number(point)

    def init_leftmost_tick(self):
        if self.leftmost_tick is None:
            self.leftmost_tick = op.mul(
                self.tick_frequency,
                np.ceil(self.x_min / self.tick_frequency)
            )

    def add_tick_marks(self):
        tick_size = self.tick_size
        self.tick_marks = VGroup(*[
            self.get_tick(x, tick_size)
            for x in self.get_tick_numbers()
        ])
        #big_tick_size = tick_size * self.longer_tick_multiple
        self.big_tick_marks = VGroup(*[
            self.get_tick(x, self.longer_tick_size)
            for x in self.numbers_with_elongated_ticks
        ])
        self.add(
            self.tick_marks,
            self.big_tick_marks,
        )

    def get_tick_numbers(self):
        u = -1 if self.include_tip else 1
        return np.arange(
            self.leftmost_tick,
            self.x_max + u * self.tick_frequency / 2,
            self.tick_frequency
        )

    def get_tick_marks(self):
        try:
            return self.ticks
        except:
            return VGroup(
                *self.tick_marks,
                *self.big_tick_marks,
            )


class Log10Line(NumberLine):
    '''x_range=None, **kwargs\n
    [x_range;real log line range with step=[0.1, 1000, 1]]-->default
    '''
    CONFIG = {
        "x_range": [0.1, 10000, 1],
        "leftmost_tick": None,
        "line_func": log10,
        "line_inv_func": exp10,
        "subdivision": 9,
        "width": 12,
        "decimal_number_config": {
            "num_decimal_places": None,
        },
        "include_tip": True,
        "step": 10,
    }

    def init_x_range(self, x_range, **kwargs):
        super().init_x_range(x_range, **kwargs)
        self.x_min = self.x_floor(self.x_min)
        self.x_max = self.x_ceil(self.x_max)
        if self.x_step <= 0:
            self.x_step = 1
        self.step = self.line_inv_func(self.x_step)

    def next_x_step(self, x):
        return x*self.step

    def prev_x_step(self, x):
        return x/self.step

    def x_ceil(self, x):
        return funcceil(x, self.line_func, self.line_inv_func)

    def x_floor(self, x):
        return funcfloor(x, self.line_func, self.line_inv_func)

    def x_round(self, x):
        return funcround(x, self.line_func, self.line_inv_func)

    def init_x_limits(self):
        return [self.x_min, self.x_max]


class UnitInterval(NumberLine):
    '''x_range=None, **kwargs\n
    [x_range;real line range with step=[0, 1, 0.1]]-->default
    '''
    CONFIG = {
        "x_range": [0, 1, 0.1],
        "unit_size": 6,  # new 10
        "tick_frequency": 0.1,
        "numbers_with_elongated_ticks": [0, 1],
        # "numbers_with_shortened_ticks": [],
        # "number_at_center": 0.5,
        "decimal_number_config": {
            "num_decimal_places": 1,
        }
    }
