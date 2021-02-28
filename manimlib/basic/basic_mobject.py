from numpy import ndarray

from manimlib.constants import DOWN, LEFT
from manimlib.mobject.mobject import Group, Mobject
from manimlib.mobject.numbers import DecimalNumber, Integer
from manimlib.mobject.svg.tex_mobject import TexMobject, TextMobject
from manimlib.mobject.types.image_mobject import ImageMobject
from manimlib.mobject.types.vectorized_mobject import VGroup, VMobject
from manimlib.animation.transform import ApplyFunction, ApplyMethod, ScaleInPlace


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
                mobject = TextMobject(mobject_or_chars)
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


class OrderedMobject(MobjectOrChars):
    def __init__(self, mobject_Or_chars, group,
                 direction=DOWN, alignment=LEFT, shift=[0, 0, 0], buffer=0.08,
                 width=None, height=None, scale=1, **kwargs):
        MobjectOrChars.__init__(self, mobject_Or_chars, **kwargs)
        self = MobjectOrChars(mobject_Or_chars)
        if isinstance(self, (TextMobject, TexMobject)):
            if mobject_Or_chars in ["$ $", " ", ".", "$.$"]:
                self[0][0].stretch_to_fit_width(0.00000001)
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
                if isinstance(each, list) and self.length_over_dim(i) > each[0]:
                    self.rescale_to_fit(each[0], 0, True)
                elif isinstance(each, tuple):
                    self.rescale_to_fit(
                        each[0]*self.length_over_dim(i), 1, True)
                elif isinstance(each, (int, float)):
                    self.rescale_to_fit(each, i, False)
        self.add_updater(lambda mob, ref_pt=group[-1], d=direction, a=alignment,
                         s=shift, b=buffer: mob.next_to(ref_pt, d, b, a)).add_to_group(group)


class GroupedMobject(VGroup):
    def __init__(self, mobject_or_chars):
        VMobject.__init__(self)
        if not isinstance(mobject_or_chars, (list, tuple, ndarray)):
            mobject_or_chars = [mobject_or_chars]
        mobject = Group(*[MobjectOrChars(each) for each in mobject_or_chars])
        self.add(*mobject)


class ImageMobjectGroup(Group):
    def __init__(self, strarray, prefix="", suffix=""):
        Group.__init__(self)
        mobject = Group(*[ImageMobject(prefix+each+suffix)
                          for each in strarray])
        self.add(*mobject)
        self.name = mobject.name
        self.__class__ = mobject.__class__
