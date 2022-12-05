import numpy as np
from manimlib.utils.bezier import bezier
from manimlib.utils.simple_functions import sigmoid


def linear(t,k=0,a=0):
    #1 - np.exp(-t / half_life)
    if a==0:
        return t+k
    elif a>0:
        return t**a+k
    else:
        return 1-abs(1-t)**(abs(a))+k


def linear_with_pause(t, pause_timing=2./3, pause_duration=1.0/5, funx=linear, **kwargs):
    '''
    t, pause_timing=2./3, pause_duration=1.0/5, func=linear,
    '''
    new_t =funx(t)
    ratio = 1/(1-pause_duration)
    pause_actual_timing = (1-pause_duration)*pause_timing
    if new_t <= pause_actual_timing:
        #print(" y",pause_actual_timing, new_t,new_t*ratio)
        return new_t*ratio
    elif new_t > pause_actual_timing+pause_duration:
        #print(" z",pause_actual_timing+pause_duration,new_t,(new_t-pause_duration)*ratio)
        return (new_t-pause_duration)*ratio
    else:
        #print(" X",new_t,pause_actual_timing*ratio)
        return pause_actual_timing*ratio


def pause(t, pause=2./3):
    return linear_with_pause(t, pause_timing=pause)


def linear_with_pauses(t, pause_timing=[1./3,1.5/3,2./3], pause_duration=0.5/5, funx=linear, **kwargs):
    '''
    t, pause_timing=[1./3,1.5/3,2./3], pause_duration=0.5/5, func=linear,
    '''
    new_t =funx(t)
    d=pause_duration
    q=pause_timing    
    if isinstance(q,(int,float)):
        q=[q]
    p=pause_actual_timing = (1-len(q)*d)*np.array(q)
    t1=np.concatenate([[-0.1],list(np.array(p)+d),[1.1],[1.1],[1.1]])
    t2=np.concatenate([p,[1.1],[1.1],[1.1],[1.1]])
    c=np.concatenate(list(zip(t1,t2)))
    ratio = 1/(1-len(q)*d)
    for i in range(1,len(c),2):
        x=int((i+1)/2-1)#123
        if c[i-1]< new_t and (new_t) <= c[i]+x*d:

            return (new_t-x*d)*ratio# new_t*ratio
        elif c[i]+x*d< new_t and new_t <= c[i+1]+x*d:
            return c[i]*ratio
    '''
    print(t1,t2)
    for i in range(len(q)):
        if t1[i]< new_t and (new_t) <= t2[i]+i*d:

            return (new_t-i*d)*ratio# new_t*ratio
        elif t2[i]+i*d< new_t and new_t <= t1[i+1]+i*d:
            return t2[i]*ratio
    '''


def pauses(t, pause=[1./3,1.5/3,2./3], duration=0.5/5):
    return linear_with_pauses(t, pause_timing=pause, pause_duration=duration)


def pause_count(t, count=5, ratio=0.2,slice=slice(1,None)):
    pause=np.linspace(0,1,count+1)[slice]
    duration=1/count*ratio
    return linear_with_pauses(t, pause_timing=pause, pause_duration=duration)

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


def linear_pulse(t, timing=1./5, transition=1.0/5, duration=1.0/5,transition2=1.0/5,pulse=1,stop=1, start=0.,end=0., **kwargs):
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
        return pulse
    elif t >t1 and t< t2:
        #return abs(start-(t-t1)/transition)
        return (t-t1)/transition-start
    else:
        return pulse-(t-t3)/transition2
        
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
    #return linear_with_pause(t/shortened, pause_timing=1, pause_duration=0, **kwargs)


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


