from numpy import ndarray, char
#from numpy import linspace, sin, arcsin, array, char
from manimlib.animation.transform import ApplyFunction, ApplyMethod, ScaleInPlace
from manimlib.basic.basic_geometry import GeomPoint, GeomMark
from manimlib.constants import DOWN, LEFT
from manimlib.mobject.mobject import Group, Mobject
from manimlib.mobject.numbers import DecimalNumber, Integer
from manimlib.mobject.svg.tex_mobject import TexMobject, TextMobject
from manimlib.mobject.types.image_mobject import ImageMobject
from manimlib.mobject.types.vectorized_mobject import VGroup, VMobject
#from manimlib.mobject.svg.mtex_mobject import *

class MobjectOrChars(TextMobject):
    def __init__(self, mobject_or_chars):
        TextMobject.__init__(self)
        if mobject_or_chars == None or (isinstance(mobject_or_chars, Mobject) and mobject_or_chars.name == "Mobject"):
            mobject = Mobject()
        elif isinstance(mobject_or_chars, (list)):
            mobject = ImageMobject(mobject_or_chars[0])
            self.add(mobject)
            self = mobject.copy()
        elif isinstance(mobject_or_chars, Mobject) and mobject_or_chars.name == "ImageMobject":
            mobject = mobject_or_chars
            self.add(mobject)
            self = mobject_or_chars[0].copy()
        else:
            if isinstance(mobject_or_chars, str):
                #mobject =MTex(mobject_or_chars)
                mobject =TextMobject(mobject_or_chars)
            elif isinstance(mobject_or_chars, int):
                mobject = Integer(mobject_or_chars)
            elif isinstance(mobject_or_chars, float):
                mobject = DecimalNumber(mobject_or_chars)
            elif isinstance(mobject_or_chars, (tuple)):
                mobject = TextMobject(*mobject_or_chars)
            else:
                mobject = mobject_or_chars
            self.become(mobject)
        self.name = mobject.name
        self.__class__ = mobject.__class__


class OrderedGroup(VGroup):
    def __init__(self, group,mobjs, 
                 direction=DOWN, alignment=LEFT, shift=[0, 0, 0], buffer=0.08,
                 width=None, height=None, scale=1, **kwargs):
        #MobjectOrChars.__init__(self, mobject_Or_chars, **kwargs)
        #[OrderedGroup(txt_line, group, width=[6.75]) for txt_line in parbs]
        VGroup.__init__(self,**kwargs)
        for mobject_Or_chars in mobjs:
            if mobject_Or_chars is not None:
                mobj = MobjectOrChars(mobject_Or_chars)
                if isinstance(mobj, (TextMobject, TexMobject)):
                    if mobject_Or_chars in ["$ $", " ", ".", "$.$"]:
                        mobj[0][0].stretch_to_fit_width(0.00000001)
                if mobject_Or_chars==".":
                    mobj.scale(1E-8)
                elif mobject_Or_chars=="/":
                    mobj.stretch_to_fit_height(1E-8)
                elif mobject_Or_chars=="-":
                    mobj.stretch_to_fit_width(1E-8)
                try:
                    if isinstance(width, Mobject):
                        width = width.get_width()
                    else:
                        if isinstance(width[0], Mobject):
                            width = width[0].get_width()
                except:
                    pass
                for i, each in enumerate([width, height]):
                    if each != None:
                        if isinstance(each, list) and mobj.length_over_dim(i) > each[0]:
                            mobj.rescale_to_fit(each[0], 0, True)
                        elif isinstance(each, tuple):
                            mobj.rescale_to_fit(
                                each[0]*mobj.length_over_dim(i), 1, True)
                        elif isinstance(each, (int, float)):
                            mobj.rescale_to_fit(each, i, False)
                mobj.add_updater(lambda mob, ref_pt=group[-1], d=direction, a=alignment,
                                s=shift, b=buffer: mob.next_to(ref_pt, d, b, a)).add_to_group(group)
        self.add(*group)


class GroupedMobject(VGroup):
    def __init__(self, mobject_or_chars):
        VMobject.__init__(self)
        if not isinstance(mobject_or_chars, (list, tuple, ndarray)):
            mobject_or_chars = [mobject_or_chars]
        mobject = Group(*[MobjectOrChars(each) for each in mobject_or_chars])
        self.add(*mobject)


class ListedVMobject(VGroup):
    '''expand all elements in <mobject> into a VGroup'''
    def __init__(self, mobject):
        VMobject.__init__(self)
        self.expand(mobject)
    def expand(self,mobject):
        if isinstance(mobject, VGroup):
            for each in mobject.submobjects:
                self.expand(each)
        else:
            for x in mobject:
                if isinstance(x, VGroup):
                    self.expand(x)
                else:
                    self.add(x)

class ListedMobject(Group):
    '''expand all elements in <mobject> into a Group'''
    def __init__(self, mobject):
        Mobject.__init__(self)
        self.expand(mobject)
    def expand(self,mobject):
        if isinstance(mobject, (Group,VGroup)):
            for each in mobject.submobjects:
                self.expand(each)
        else:
            for x in mobject:
                if isinstance(x, (Group,VGroup)):
                    self.expand(x)
                else:
                    self.add(x)


class MappedMobject(VGroup):
    def __init__(self, mobjects,indices):
        VMobject.__init__(self)
        self.add(*list(map(mobjects.__getitem__, indices)))

class SumzipMobject(VGroup):
    '''zip and expand all first level elements in mobjlists into a VGroup'''
    def __init__(self, *mobjlists):
        VMobject.__init__(self)
        self.add(*sum(zip(*mobjlists),()))
    

class ImageMobjectGroup(Group):
    def __init__(self, strarray, prefix="", suffix=""):
        Group.__init__(self)
        mobject = Group(*[ImageMobject(prefix+each+suffix)
                          for each in strarray])
        self.add(*mobject)
        self.name = mobject.name
        self.__class__ = mobject.__class__

class AnimatedGroup(Group):
    def __init__(self, mobjs=None):
        Group.__init__(self)
        if mobjs==None:
            try:
                self.add(*ImageMobjectGroup(char.mod('%01d', range(
                    0, 10)), "sidewayoutput\\sidewayoutput2020yt"))
            except:
                self.add(*ImageMobjectGroup(char.mod(
                    '%01d', range(9, -1, -1)), "001\\"))


class LocatedText(VGroup):
    def __init__(self, point, strs, offset=[0,0,0], height=None,color=None,mobj=1):
        VGroup.__init__(self)
        if isinstance(mobj, (int, float, bool)):
            if int(mobj) == 1:
                self.add(GeomPoint(point))
            else:
                self.add(GeomMark(point))
        self.add(TextMobject(strs, height=height).move_to(point, offset=offset).set_color(color))
    def ptc(self):
        return self.submobjects[0].get_center()
    
    def pnt(self):
        return self.submobjects[0]

    def txt(self):
        return self.submobjects[1]
        

