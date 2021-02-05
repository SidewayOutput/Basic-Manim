from manimlib.mobject.mobject import Group, Mobject
from manimlib.mobject.numbers import DecimalNumber, Integer
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.mobject.types.image_mobject import ImageMobject


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


class ImageMobjectGroup(Group):
    def __init__(self, strarray, prefix="", suffix=""):
        Group.__init__(self)
        mobject = Group(*[ImageMobject(prefix+each+suffix)
                          for each in strarray])
        self.add(*mobject)
        self.name = mobject.name
        self.__class__ = mobject.__class__
