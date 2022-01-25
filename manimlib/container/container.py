import inspect
import numpy as np
import manimlib.constants
from manimlib.constants import RH, FRAME_WIDTH, FRAME_HEIGHT, ORIGIN, OUT, LEFT, RIGHT, DOWN, UP, STRAIGHT_PATH_THRESHOLD,TAU
from manimlib.utils.config_ops import digest_config
from manimlib.utils.space_ops import rotation_matrix
from manimlib.utils.space_ops import get_norm
from manimlib.utils.simple_functions import sigmoid
from manimlib.utils.bezier import bezier
# Currently, this is only used by both Scene and Mobject.
# Still, we abstract its functionality here, albeit purely nominally.
# All actual implementation has to be handled by derived classes for now.

# TODO: Move the "remove" functionality of Scene to this class


class BasicManim(object):
    '''Basic Manim Object'''
    CONFIG = {"test":'test'}

    def init_name(self):
        if self.name is None:
            self.name = self.__class__.__name__

    def be(self, name=None,module=None):
        #??if name in vars(manimlib.constants):
        #    raise Warning("Duplicate Variable")
        if module is None:
            exec('manimlib.constants.'+name+'=self')
        else:
            #x=f'{module=}'.split('=')[0] 
            #exec(x+'=module')
            #exec(x+'.'+name+'=self',globals(),locals())
            exec("module"+'.'+name+'=self',globals(),locals())
        return self

    def zinit_cvars(self, kwargs={}):
        '''initial vars from self.CONFIG or kwargs 
        '''
        if hasattr(super(), 'CONFIG'):
            par_config=super().CONFIG
        else:
            par_config={}
        for each in self.CONFIG.keys():
            vars(self)[each]=self.CONFIG.get(each, None) or kwargs.get(each, par_config.get(each,None))
            #exec("self."+each+"=self.CONFIG.get(each, None) or kwargs.get(each, par_config.get(each,None))")
            #self.x=self.CONFIG.get('x', None) or kwargs.get('x', super().CONFIG.get('x',None))
        return self

    def init_cvars(self,*dicts):
        '''init config variables with ICONFIG'''
        if hasattr(self, 'CONFIG'):
            config=self.CONFIG
        else:
            config={}
        kwargs={}
        for each in dicts:
            kwargs.update(each)
        for each in list(dicts[0].keys())[:]:
            exec("self."+each+"=config.get(each, None) or kwargs.get(each, None)") 

    def get_vars(self,kwargs={},dict=None):
        #for each in super().CONFIG.keys():
        #    kwargs[each]=vars(self)[each]
        if dict is None:
            dict=self.CONFIG
        for each in dict.keys():
            kwargs[each]=vars(self)[each]        
        return kwargs

    def print(self,mobj=None):
        print(self,id(self))
        if mobj is not None:
            return mobj
        else:
            return self

    def prtV(self,arg=None):
        from manimlib.mobject.types.vectorized_mobject import VMobject
        if arg is None:
            print(self)
        else:
            print(arg)
        return VMobject()

    #matarry manipulation
    def validity_of_shape_input(self, matarry, test=None, length=None, dim=None):
        if length is None:
            length=2#?>=2
        if dim is None:
            dim=vars(self).get('dim',3)
        arry=np.array(matarry)
        shape=arry.shape
        if arry.dtype==np.dtype('O') or len(shape)>length or shape[-1]!=dim:
            #pass
            raise Exception("wrong structure") 
        if test=='path' or test=='addpath' or  test=='joinpath' or test=='appdpath' or test=='newpath':
            nppcc = vars(self).get('n_points_per_cubic_curve',None)
            if nppcc is None:
                raise Exception("self not paths")
            if (test=='path' or test=='addpath' ) and len(arry) % nppcc != 0 :
                raise Exception("Not paths")
            if (test=='addpath' or test=='newpath') and len(self.points) % nppcc != 0  :
                raise Exception("Self not paths")
            if test=='joinpath':
                if len(arry) % nppcc != nppcc-1 :
                    raise Exception("Not joinpaths")
                if len(self.points) % 4 == 0  :
                    arry=np.append([self.points[-1]],arry,axis=0)
                elif len(self.points) % 4 != 1  :
                    raise Exception("Self has no start point")
            if test=='appdpath':
                if len(arry) % 4 == 0:
                    self.validity_of_shape_input(arry, test='addpath')
                elif len(arry) % 4 == nppcc-1:
                    arry=self.validity_of_shape_input(arry, test='joinpath')
                elif len(arry) % 4 == 1:
                    self.validity_of_shape_input(arry, test='newpath')
                else:
                    raise Exception("Not")
        return arry
        
    def swap01(self, matarry):
        '''(j,i,...)<--(i,j,...)'''
        return np.swapaxes(matarry,0,1)
    
    def joinmn(self, matarry, m,n):
        '''(...,m*...*n,...)<--(...,m,...,n,...)'''
        shape=matarry.shape
        if n==-1 or n==len(shape)-1:
            h=()
        else:
            h=shape[n+1:]
        return matarry.reshape(shape[:m]+(-1,)+h)

    def join01(self, matarry):
        '''(i*j,...)<--(i,j,...)'''
        return matarry.reshape((-1,)+matarry.shape[2:])
        #return np.array([list(item) for submatarry in matarry for item in submatarry])
    
    def join32(self, matarry, m=-3,n=-2):
        '''(...,m*...*n,...)<--(...,m,...,n,...)'''
        return self.joinmn(matarry, m,n)

    def xpan(self, start, end, count, first=0,last=1):
        '''return(i,j,...m,x,n)=((end(i,j,...,m,n)-start(i,j,...,m,n))Xcount(x)'''
        return np.moveaxis(np.multiply.outer(end-start,np.linspace(first,last,count).T),-1,-2)

    def xpanadd(self, start, end, count, first=0,last=1,add=1):
        '''return(i,j,...m,x,n)=((end(i,j,...,m,n)-start(i,j,...,m,n))Xcount(x)+start'''
        return self.xpan(start, end, count, first,last)+start*add

    #linear nx4 xpan
    def alpha_xpan(self,points, count=None, first=0,last=1,length=None,dim=None):
        '''points(h,i,j,...,m,n); point.shape>=(2,), count(s)
        (h-1,i,j,...,m,n,s)<--multiply_outer((h-1,i,j,...,m,n)(s))'''
        points=self.validity_of_shape_input(points,length=length,dim=dim)#,length=len(np.array(points).shape)
        if count==None :
            count=vars(self).get('n_points_per_cubic_curve',4)
        interslice=np.linspace(first,last,count)
        return np.multiply.outer(points[:-1],1-interslice)+np.multiply.outer(points[1:],interslice)

    def paths_xpan(self,points, count=None, first=0,last=1,length=None,dim=None):
        '''<alpha_xpan> of points in paths format [[*points],...]'''
        arry=np.moveaxis(points,-2,0)
        shape=arry.shape
        return np.moveaxis(self.alpha_xpan(arry,length=len(shape),dim=shape[-1]),0,-3)

    def alpha_ctrls(self,points, count=None, first=0,last=1,length=None):
        '''points(h+1,i,j,...,m,n); point.shape>=(2,)
        (s,h,i,j,...m,n)=((end(h,i,j,...,m,n)-start(h,i,j,...,m,n))Xcount(s)+start
        return ctrls(ctrl1s,ctrl2s,...)'''
        return np.moveaxis(self.alpha_xpan(points,count,first,last,length),-1,0)

    def alpha_paths(self,points, count=None, first=0,last=1,length=None,dim=None):
        '''points(h+1,i,j,...,m,n); point.shape>=(2,)
        (h,i,j,...m,s,n)=((end(h,i,j,...,m,n)-start(h,i,j,...,m,n))Xcount(s)+start
        return paths(path1,path2,...)'''
        return np.moveaxis(self.alpha_xpan(points,count,first,last,length,dim),-1,-2)

    def alpha_pts(self,points, count=None, first=0,last=1,length=None,dim=None):
        '''points(h+1,i,j,...,m,n); point.shape>=(2,)
        (h*i,j,...m,s,n)=((end(h,i,j,...,m,n)-start(h,i,j,...,m,n))Xcount(s)+start
        return pts(*path1,*path2,...)'''
        return self.join01(self.alpha_paths(points,count,first,last,length,dim))

    #angular 1*24 xpan
    def theta_xpan(self,start, angle, anchor=9):
        '''(m,n,p=anchor-1,d=3,s=nppcc)<--(s=nppcc,m,n,p=anchor-1,d=3)'''
        return np.moveaxis(self.theta_ctrls(start, angle, anchor),0,-1)

    def theta_ctrls(self,start, angle, anchor=9):
        '''ctrls of a unit circle,(s=nppcc,m,n,p=anchor-1,d=3)'''
        anchors= self.unit_circular_points(start, angle, anchor)
        nppcc=vars(self).get('n_points_per_cubic_curve',4)
        d_lengths=  np.tan(angle / (anchor-1)  / (nppcc-1)) * anchors
        d_lengths[:,0],d_lengths[:,1]=-d_lengths[:,1],d_lengths[:,0].copy()
        handles_p,handles_n=anchors+np.multiply.outer(np.array([1,-1]),d_lengths)
        return np.array([anchors[:-1],handles_p[:-1],handles_n[1:],anchors[1:]])

    def theta_paths(self,start, angle, anchor=9):
        '''(m,n,p=anchor-1,s=nppcc,d=3)<--(s=nppcc,m,n,p=anchor-1,d=3)'''
        return np.moveaxis(self.theta_ctrls(start, angle, anchor),0,-2)

    def theta_pts(self,start, angle, anchor=9):
        '''(m,n,p=anchor-1,s=nppcc,d=3)<--(s=nppcc,m,n,p=anchor-1,d=3)'''
        return self.join32(self.theta_paths(start, angle, anchor))

    #pts_fm_ctrls
    def pts_fm_4ctrls(self, ctrl1s, ctrl2s, ctrl3s, ctrl4s):
        '''(m,n,...,p*s,d)<--(m,n,...,p,s,d)<--(s,m,n,...,p,d)<--s*(m,n,...,p,d)'''
        assert(len(ctrl1s) == len(ctrl2s) == len(ctrl3s) == len(ctrl4s))
        return self.join32(np.moveaxis([ctrl1s, ctrl2s, ctrl3s, ctrl4s],0,-2))

    def unit_circular_points(self,start=0, angle=TAU, anchor=13,nolastpt=False):
        anchors=np.vstack(np.vectorize(lambda a:[np.cos(a),np.sin(a),0], otypes=[object])( np.linspace(start,start + angle,anchor,))).astype(np.float)
        if nolastpt:
            anchors=anchors[:-1]
        return anchors

    def rotate_vector(self, angle):
        # source: 
        # https://datascience.stackexchange.com/questions/57226/how-to-rotate-the-plot-and-find-minimum-point    
        # make rotation matrix
        theta = np.radians(angle)
        co = np.cos(theta)
        si = np.sin(theta)
        rotation_matrix = np.array(((co, -si,0), (si, co,0), (0, 0,0)))
        # rotate data vector
        rotated_vector = np.dot(self.points,rotation_matrix)
        return rotated_vector

    #object validation
    def validity_of_method_input(self, method):
        from manimlib.mobject.mobject import Mobject
        if not inspect.ismethod(method):
            raise Exception(
                #"Whoops, looks like you accidentally invoked "
                #"the method you want to animate"
                "Not a Method"
            )
        assert(isinstance(method.__self__, Mobject))

    def validity_of_decimal_mob_input(self, decimal_mob):
        from manimlib.mobject.numbers import DecimalNumber
        if not isinstance(decimal_mob, DecimalNumber):
            raise Exception(
                #"ChangingDecimal can only take "
                #"in a DecimalNumber"
                "Not a DecimalNumber"
            )

    def validity_of_vmobject_input(self, vmobject):
        from manimlib.mobject.types.vectorized_mobject import VMobject
        if not isinstance(vmobject, VMobject):
            raise Exception(
                #"DrawBorderThenFill only works for VMobjects"
                "Not a VMobject"
            )

    def validity_of_attr_input(self, mobject, attribute):
        if not hasattr(mobject, attribute):
            raise Exception(
                #"MoveToTarget called on mobject"
                "without attribute "+attribute
            )

    def validity_of_target_input(self, mobject,attribute="target"):
        self.validity_of_attr_input(mobject, attribute)
        '''
        if not hasattr(mobject, "target"):
            raise Exception(
                #"MoveToTarget called on mobject"
                "without attribute 'target'"
            )
        '''

    #paths
    if 1==2:
        def straight_path(self, start_points, end_points, alpha):
            """
            Same function as interpolate, but renamed to reflect
            intent of being used to determine how a set of points move
            to another set.  For instance, it should be a specific case
            of path_along_arc
            """
            return BasicManim.interpolate(start_points, end_points, alpha)


        def path_along_arc(self, arc_angle, axis=OUT):
            """
            If vect is vector from start to end, [vect[:,1], -vect[:,0]] is
            perpendicular to vect in the left direction.
            """
            if abs(arc_angle) < STRAIGHT_PATH_THRESHOLD:
                return straight_path
            if get_norm(axis) == 0:
                axis = OUT
            unit_axis = axis / get_norm(axis)

            def path(start_points, end_points, alpha):
                vects = end_points - start_points
                centers = start_points + 0.5 * vects
                if arc_angle != np.pi:
                    centers += np.cross(unit_axis, vects / 2.0) / np.tan(arc_angle / 2)
                rot_matrix = rotation_matrix(alpha * arc_angle, unit_axis)
                return centers + np.dot(start_points - centers, rot_matrix.T)
            return path


        def clockwise_path(self):
            return path_along_arc(-np.pi)


        def counterclockwise_path(self):
            return path_along_arc(np.pi)
  
    #interpolate
    if 1==2:
        def interpolate(start, end, alpha):
            return (1 - alpha) * start + alpha * end





class Manim(BasicManim):
    '''Manim Object container
    Animation, CoordinateSystem
    '''

    #rate_functions: use method as function #by using self as parameter t
    if 1==2:
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


class Container(BasicManim):
    '''Manim Mobject container
    Mobject, WindowScene
    '''
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
