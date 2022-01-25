import numpy as np
from manimlib.utils.bezier import bezier
from manimlib.utils.simple_functions import sigmoid


def linear(t):
    return t


def linear_with_pause(t, pause_timing=2./3, pause_duration=1.0/5, funx=linear, **kwargs):
    '''
    t, pause_timing=2./3, pause_duration=1.0/5, func=linear,
    '''
    new_t =funx(t)
    ratio = 1/(1-pause_duration)
    pause_actual_timing = (1-pause_duration)*pause_timing
    if new_t <= pause_actual_timing:
        return new_t*ratio
    elif new_t > pause_actual_timing+pause_duration:
        return (new_t-pause_duration)*ratio
    else:
        return pause_actual_timing*ratio


def pause(t, pause=2./3):
    return linear_with_pause(t, pause_timing=pause)


def linear_with_delay(t, delay=5.0/10, **kwargs):
    '''
    t, delay=5.0/10,
    '''
    return linear_with_pause(t, pause_timing=0., pause_duration=delay, **kwargs)


def delay(t, delay=5.0/10):
    '''
    t, pause=5.0/10,
    '''
    return linear_with_delay(t, delay=delay)


def linear_with_wait(t, wait=5.0/10, **kwargs):
    '''
    t, wait=5.0/10,
    '''
    return linear_with_pause(t, pause_timing=1-wait, pause_duration=wait, **kwargs)


def wait(t, wait=5.0/10):
    return linear_with_wait(t, wait=wait)


def linear_pulse(t, timing=1./5, transition=1.0/5, duration=1.0/5,transition2=1.0/5,stop=1, start=0.,end=0., **kwargs):
    '''
    t, timing=2./3, transition=1.0/5,
    -
    '''
    t0=0
    t1=t0+timing
    t2=t1+transition
    t3=t2+duration
    t4=t3+transition2
    t5=stop

    if t <= t1 or t>t4 or t>t5:
        return start
    elif t >= t2 and t<=t3:
        return end
    elif t >t1 and t< t2:
        return abs(start-(t-t1)/transition)
    else:
        return abs(end-(t-t3)/transition2)
        
def pulsex(t, pulse_timing=2./3, pulse_duration=1.0/5, **kwargs):
    '''
    t, pulse_timing=2./3, pulse_duration=1.0/5,
    -
    '''
    if t <= pulse_timing:
        return 0
    elif t >= pulse_timing+pulse_duration:
        return 1
    else:
        return (t-pulse_timing)/pulse_duration


def pulse(t,pulse=2./3):
    return linear_pulse(t,timing=pulse)

def long_pulse(t,timing=0.05,pulse=0.9):
    return linear_pulse(t,timing=pulse)


def linear_pulsereject(t, timing=1./5, transition=1.0/5, duration=1.0/5,transition2=1.0/5, stop=1, start=1.,end=1., **kwargs):
    return linear_pulse(t, timing=timing, transition=transition, stop=stop, start=start,end=end, **kwargs)


def pulsereject(t, reject=2./3):
    return linear_pulsereject(t,timing=reject)


def linear_with_step(t, timing=2./3, transition=1.0/5,duration=1,transition2=1, stop=1, start=0.,end=1., **kwargs):
    '''
    t, timing=2./3, transition=1.0/5,
    -
    '''
    return linear_pulse(t, timing=timing, transition=transition,duration=duration,transition2=transition2, stop=stop, start=start,end=end, **kwargs)


def step(t, step=2./3):
    return linear_with_step(t,timing=step)

def jump_up(t, timing=1./15, transition=1.0/15,duration=1,transition2=1, stop=1, start=0.,end=1., **kwargs):
    '''
    t, timing=1./15, transition=1.0/15,
    -
    '''
    return linear_pulse(t, timing=timing, transition=transition,duration=duration,transition2=transition2, stop=stop, start=start,end=end, **kwargs)
def jump(t, timing=1./15, transition=1.0/15,duration=1,transition2=1, stop=1, start=0.,end=1., **kwargs):
    '''
    t, timing=1./15, transition=1.0/15,
    -
    '''
    return linear_pulse(t, timing=timing, transition=transition,duration=duration,transition2=transition2, stop=stop, start=start,end=end, **kwargs)

def linear_with_stepdown(t, timing=2./3, transition=1.0/5,duration=1,transition2=1, stop=1, start=1.,end=0., **kwargs):
    '''
    t, timing=2./3, transition=1.0/5,
    -
    '''
    return linear_pulse(t, timing=timing, transition=transition,transition2=transition2, stop=stop, start=start,end=end, **kwargs)

def jump_down(t, timing=1./15, transition=1.0/15,duration=1,transition2=1, stop=1, start=1.,end=0., **kwargs):
    '''
    t, timing=1./15, transition=1.0/15,
    -
    '''
    return linear_pulse(t, timing=timing, transition=transition,transition2=transition2, stop=stop, start=start,end=end, **kwargs)

def stepdown(t, step=2./3):
    return linear_with_stepdown(t,timing=step)



def zshorten(t,shorten=1.0/5, **kwargs):
    shortened=1-shorten
    return pulsex(t/shortened, pulse_timing=shortened, pulse_duration=shorten, **kwargs)


def shorten(t,shorten=1.0/5, **kwargs):
    shortened=1-shorten
    return linear_with_pause(t/shortened, timing=shortened, transition=shorten, **kwargs)


def smooth(t, inflection=10.0):
    error = sigmoid(-inflection / 2)
    return np.clip(
        (sigmoid(inflection * (t - 0.5)) - error) / (1 - 2 * error),
        0, 1,
    )


def rush_into(t, inflection=10.0):
    return 2 * smooth(t / 2.0, inflection)


def rush_from(t, inflection=10.0):
    return 2 * smooth(t / 2.0 + 0.5, inflection) - 1


def slow_into(t):
    return np.sqrt(1 - (1 - t) * (1 - t))


def double_smooth(t):
    if t < 0.5:
        return 0.5 * smooth(2 * t)
    else:
        return 0.5 * (1 + smooth(2 * t - 1))


def there_and_back(t, inflection=10.0):
    new_t = 2 * t if t < 0.5 else 2 * (1 - t)
    return smooth(new_t, inflection)


def there_and_back_with_pause(t, pause_ratio=1. / 3):
    a = 1. / pause_ratio
    if t < 0.5 - pause_ratio / 2:
        return smooth(a * t)
    elif t < 0.5 + pause_ratio / 2:
        return 1
    else:
        return smooth(a - a * t)


def running_start(t, pull_factor=-0.5):
    return bezier([0, 0, pull_factor, pull_factor, 1, 1, 1])(t)


def not_quite_there(func=smooth, proportion=0.7):
    def result(t):
        return proportion * func(t)
    return result


def wiggle(t, wiggles=2):
    return there_and_back(t) * np.sin(wiggles * np.pi * t)


def squish_rate_func(func, a=0.4, b=0.6):
    def result(t):
        if a == b:
            return a

        if t < a:
            return func(0)
        elif t > b:
            return func(1)
        else:
            return func((t - a) / (b - a))

    return result

# Stylistically, should this take parameters (with default values)?
# Ultimately, the functionality is entirely subsumed by squish_rate_func,
# but it may be useful to have a nice name for with nice default params for
# "lingering", different from squish_rate_func's default params


def lingering(t):
    return squish_rate_func(lambda t: t, 0, 0.8)(t)


def exponential_decay(t, half_life=0.1):
    # The half-life should be rather small to minimize
    # the cut-off error at the end
    return 1 - np.exp(-t / half_life)


