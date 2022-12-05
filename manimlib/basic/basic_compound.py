from manimlib.constants import TAU,BLUE,YELLOW
from manimlib.animation.animation import Animation, AGroup
from manimlib.animation.composition import AnimationGroup, Succession,OneByOne, AnimByAnim
from manimlib.animation.creation import ShowSubmobjectsOneByOne,ShowCreation,Show
from manimlib.animation.fading import FadeOut,FadeIn
from manimlib.animation.indication import Highlight,ShowPassingFlash
from manimlib.animation.rotation import Rotating
from manimlib.animation.transform import ApplyMethod,Transform,TransformFromCopy,ReplacementTransform
from manimlib.basic.basic_animation import FadeInThenIndicateThenFadeOut,ShowCreationThenFadeOut,FadeInThenFadeOut,FadeinSuccession,AnimateStroke,FadeoutSuccession,ShowCreations,Shows,Add
from manimlib.mobject.mobject import Mobject,Group
from manimlib.mobject.types.vectorized_mobject import VMobject,VGroup
from manimlib.utils.config_ops import merge_config_kwargs
from manimlib.utils.color import invert_color
from manimlib.utils.rate_functions import linear
from manimlib.utils.rate_functions import linear, linear_with_pause, there_and_back_with_pause, linear_with_delay, there_and_back, delay, pause, step,linear_pulse,jump_up


class ShowSubmobjectsOneByOneAndFadeInThenIndicateThenFadeOut(AnimationGroup):
    CONFIG = {
        "scale_factor": 1.2,
    }

    def __init__(self, *mobjects, **kwargs):
        self.show_rate_func = linear
        kwargs = merge_config_kwargs(self, kwargs)
        super().__init__(
            ShowSubmobjectsOneByOne(mobjects[0].add(
                Mobject()), rate_func=self.show_rate_func, **kwargs),
            FadeInThenIndicateThenFadeOut(
                mobjects[1],   **kwargs),
            fix_time=2,**kwargs)


class zShowRotatingAndCreation(OneByOne):
    '''*mobjects, run_time=1, rate_func=linear, copy=0, angle=TAU, color=None, width=None, opactiy=0.5, remover=False, lag_ratio=0, anims=[],fix_time=None,\n
    bool:copy; num:run_time; callable:rate_func
    -'''
    CONFIG = {
        #"rate_func": linear,
    }
    def __init__(self, *mobjects, run_time=1, rate_func=linear, copy=0, angle=TAU, color=None, width=None, opactiy=0.5, remover=False, lag_ratio=0, anims=[],fix_time=None,**kwargs):
        while not isinstance(mobjects[-1],(Mobject,Group,VMobject,VGroup)):
            if isinstance(mobjects[-1], (int, float,bool)):
                if isinstance(mobjects[-1],bool):
                    if int(mobjects[-1])==1:
                        copy=True
                        mobjects=mobjects[:-1]
                elif isinstance(mobjects[-1],(int,float)):
                    run_time=mobjects[-1]
                    mobjects=mobjects[:-1]
            elif callable(mobjects[-1]):
                rate_func=mobjects[-1]
                mobjects=mobjects[:-1]
        animations=AGroup(
            *anims,
            )
        if copy:
            mobject=mobjects[0].copy().set_stroke(color,width,opactiy)
            if remover:
                animations.add(FadeOut(mobjects[0],run_time=0.001))
            remover=True
                
            
        else:
            mobject=mobjects[0]
        if isinstance(mobjects[1],(int,float)):
            center=mobjects[0].point_from_proportion(mobjects[1])
        elif isinstance(mobjects[1],(Mobject)):
            center=mobjects[1].get_center()
        else:
            center=mobjects[1]
        if fix_time is None:
            fix_time=run_time
            #run_time=None#??
        animations.add(
            AnimationGroup(
                Rotating(mobject,about_point=center,radians=angle, remover=remover,rate_func=rate_func,**kwargs),
                Show(VGroup(*mobjects[2]),rate_func=rate_func, **kwargs)))
            
        super().__init__(
            *animations,
            fix_time=fix_time,**kwargs)
        #Animation(mobjects[0])


class ShowRotatingAndCreation(OneByOne):
    '''*mobjects, run_time=1, rate_func=linear, copy=0, angle=TAU, color=None, width=None, opactiy=0.5, remover=False, lag_ratio=0, anims=[],fix_time=None,\n
    bool:copy; num:run_time; callable:rate_func
    -'''
    CONFIG = {
        #"rate_func": linear,
        #'r_width':None,
    }
    def __init__(self, *mobjects, run_time=1, rate_func=linear, copy=0, angle=TAU, color=None, width=None, opacity=0.5, remover=False, lag_ratio=0, anims=[],fix_time=None,r_color=None,r_width=None,r_opacity=None,r2_color=None,r2_width=None,r2_opacity=None,**kwargs):
        while not isinstance(mobjects[-1],(Mobject,Group,VMobject,VGroup)):
            if isinstance(mobjects[-1], (int, float,bool)):
                if isinstance(mobjects[-1],bool):
                    if int(mobjects[-1])==1:
                        copy=True
                        mobjects=mobjects[:-1]
                elif isinstance(mobjects[-1],(int,float)):
                    run_time=mobjects[-1]
                    mobjects=mobjects[:-1]
            elif callable(mobjects[-1]):
                rate_func=mobjects[-1]
                mobjects=mobjects[:-1]
        animation=AGroup()
        animations=AGroup(
            *anims,
            )
        #r_width=None
        #r_color=None
        #r_opacity=None
        if copy:
            def applystroke(m):
                c,w,o=m.get_stroke()
                m.set_stroke(c, w, o)
            #mobject=mobjects[0].copy().set_stroke(color,width,opacity)
            mobject=mobjects[0].copy()
            #mobject.add_updater(applystroke)
            
            if width is None:
                #print("ss")
                width=mobject.get_stroke_width()
                if width==0:
                    width=4
            r_width=width    
            r_opacity=opacity
            #mobject.set_stroke(color,width,opacity)
            #animation.add(ApplyMethod(mobject.set_stroke,color,width,opacity,run_time=0.001))
            #if remover:
            #    animations.add(FadeOut(mobjects[0],run_time=0.001))
            remover=True
                
            
        else:
            mobject=mobjects[0]
        if isinstance(mobjects[1],(int,float)):
            center=mobjects[0].point_from_proportion(mobjects[1])
        elif isinstance(mobjects[1],(Mobject)):
            center=mobjects[1].get_center()
        else:
            center=mobjects[1]
        if fix_time is None:
            fix_time=run_time
        remover=False
        animations.add(
            Rotating(mobject,about_point=center,radians=angle, remover=remover,rate_func=rate_func,r_color=r_color,r_width=r_width,r_opacity=r_opacity,**kwargs),
            Show(VGroup(*mobjects[2]),rate_func=rate_func,r_color=r2_color,r_width=r2_width,r_opacity=r2_opacity,  **kwargs))
        #if 1 or remover:
        #    animation.add(ApplyMethod(mobject.set_stroke,None,0,run_time=0.001,rate_func=jump_up)) 
        if copy:
            animation.add(ApplyMethod(mobject.set_stroke,{"width":0},run_time=0.001,rate_func=jump_up))
        animation.add(AnimationGroup(*animations,fix_time=fix_time,**kwargs))   
        super().__init__(
            *animation
            #*animations, fix_time=fix_time,**kwargs
            )

        #Animation(mobjects[0])


class ShowCreationOneByOneThenFadeOut(Succession):
    CONFIG = {
        # "rate_func": there_and_back,
        # "scale_factor": 1.2,
        # "color": YELLOW,
        "remover": False,
        "lag_ration": 0.1,

    }

    def __init__(self, *mobjects, run_time=5, ratio_array=[0.95, 0.05], **kwargs):
        super().__init__(
            ShowCreationThenFadeOut(mobjects[0], run_time=run_time*ratio_array[0], **kwargs),  # run_time *
            # ratio_array[0], **kwargs),  # 0.5
            ShowCreationThenFadeOut(mobjects[1], run_time=run_time*ratio_array[0], **kwargs),  # run_time *
            # ratio_array[0], **kwargs),  # 0.5
            FadeOut(VGroup(*mobjects), run_time=run_time * \
                    ratio_array[1], **kwargs),  # 0.03
            **kwargs
        )


class ShowPassingFlashAndCreation(OneByOne):
    '''*mobjects, run_time=1, ratio_array=[0.4,0.6], color=None, width=None, opacity=None, reverse=0,\n
    num:run_time;  color->None:yellow+inv color; 0:inv color;  width->None:stroke width*2
    -'''
    def __init__(self, *mobjects, run_time=1, ratio_array=[0.4,0.6],color=None,width=None,opacity=None,reverse=0, anim=None,**kwargs):
        if isinstance(mobjects[-1],(int,float)):
            run_time=mobjects[-1]
            mobjects=mobjects[:-1]
        
        if len(mobjects)==1 and isinstance(*mobjects, (Group,VGroup)):
            mobjects=mobjects[0].submobjects
        if color is None:
            [YELLOW,invert_color(mobjects[0].get_stroke_color())]
        elif color==0:
            color=invert_color(mobjects[0].get_stroke_color())
        if width is None:
            width=mobjects[0].get_stroke_width()*2
            
        #mobject=mobjects[0].copy().set_stroke([YELLOW,invert_color(mobjects[0].get_stroke_color())])

        mobject=mobjects[0].copy().set_stroke(color,width,opacity)
        animations=AGroup(
            ShowPassingFlash(mobject,remover=True, run_time=run_time*ratio_array[0], **kwargs),
            ShowCreations(mobjects[1], run_time=run_time*ratio_array[1], **kwargs),)   

        if reverse:
            mobject.reverse_points()
        super().__init__(
            *animations
            #ShowPassingFlash(mobject,remover=True, run_time=run_time*ratio_array[0], **kwargs),
            #ShowCreations(mobjects[1], run_time=run_time*ratio_array[1], **kwargs), 
            ###Shows(mobjects[1], run_time=run_time*ratio_array[1], **kwargs), 
        )

class ShowPassingFlashAndCreationThenFadeOut(OneByOne):
    '''*mobjects, run_time=1, ratio_array=[0.4,0.6], color=None, width=None, opacity=None, reverse=0,\n
    num:run_time;  color->None:yellow+inv color; 0:inv color;  width->None:stroke width*2
    -'''
    def __init__(self, *mobjects, run_time=1, ratio_array=[0.4,0.6],color=None,width=None,opacity=None,reverse=0, anim=None,**kwargs):
        if isinstance(mobjects[-1],(int,float)):
            run_time=mobjects[-1]
            mobjects=mobjects[:-1]
        
        if len(mobjects)==1 and isinstance(*mobjects, (Group,VGroup)):
            mobjects=mobjects[0].submobjects
        if color is None:
            [YELLOW,invert_color(mobjects[0].get_stroke_color())]
        elif color==0:
            color=invert_color(mobjects[0].get_stroke_color())
        if width is None:
            width=mobjects[0].get_stroke_width()*2
            
        #mobject=mobjects[0].copy().set_stroke([YELLOW,invert_color(mobjects[0].get_stroke_color())])

        mobject=mobjects[0].copy().set_stroke(color,width,opacity)
        animations=AGroup(
            ShowPassingFlash(mobject,remover=True, run_time=run_time*ratio_array[0], **kwargs),
            ShowCreationThenFadeOut(mobjects[1], run_time=run_time*ratio_array[1], **kwargs),)  

        if anim is not None:
            animations.add(anim)
        if reverse:
            mobject.reverse_points()
        super().__init__(
            *animations
            #ShowPassingFlash(mobject,remover=True, run_time=run_time*ratio_array[0], **kwargs),
            #ShowCreations(mobjects[1], run_time=run_time*ratio_array[1], **kwargs), 
            ###Shows(mobjects[1], run_time=run_time*ratio_array[1], **kwargs), 
        )

class FadeInAndCreation(OneByOne):
    def __init__(self, *mobjects, run_time=1, ratio_array=[0.001,0.999],color=None,width=None,opacity=None,reverse=0,c_func=linear, anim=None,**kwargs):
        if isinstance(mobjects[-1],(int,float)):
            run_time=mobjects[-1]
            mobjects=mobjects[:-1]
        
        if len(mobjects)==1 and isinstance(*mobjects, (Group,VGroup)):
            mobjects=mobjects[0].submobjects
        if color is None:
            [YELLOW,invert_color(mobjects[0].get_stroke_color())]
        elif color==0:
            color=invert_color(mobjects[0].get_stroke_color())
        #if width is None:
        #    width=mobjects[0].get_stroke_width()*2
            
        #mobject=mobjects[0].copy().set_stroke([YELLOW,invert_color(mobjects[0].get_stroke_color())])

        mobject=mobjects[0].copy().set_stroke(color,width,opacity)
        anims=AGroup(ShowCreation(mobjects[1], rate_func=c_func, **kwargs))

        if anim is not None:
            anims.add(*anim)
        animations=AGroup(
            FadeIn(mobject, run_time=run_time*ratio_array[0]),
            AnimationGroup(*anims, fix_time=run_time*ratio_array[1],**kwargs),)  

        if reverse:
            mobject.reverse_points()
        super().__init__(
            *animations
            #ShowPassingFlash(mobject,remover=True, run_time=run_time*ratio_array[0], **kwargs),
            #ShowCreations(mobjects[1], run_time=run_time*ratio_array[1], **kwargs), 
            ###Shows(mobjects[1], run_time=run_time*ratio_array[1], **kwargs), 
        )
