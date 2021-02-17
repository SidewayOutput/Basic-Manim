# folder/file: tutorial/basicmanim/basicmanim_transform_001a.py


from manimlib.animation.composition import AnimationGroup
from manimlib.animation.creation import ShowCreation, Write
from manimlib.animation.fading import FadeIn
from manimlib.animation.growing import GrowFromCenter
from manimlib.animation.transform import ApplyMethod, ClockwiseTransform, CounterclockwiseTransform, MoveToTarget, ReplacementTransform, Transform, TransformFromCopy
from manimlib.basic.basic_complex import StartScreens01, EndScreen01
from manimlib.basic.basic_function import axes_point, coord_grid
from manimlib.mobject.geometry import Circle, Dot, Line, Square
from manimlib.mobject.mobject import Group
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.scene.scene import Scene


class basicmanim_transform_001a(Scene):

    def construct(self):
        if 1 == 1:
            try:
                self.add_sound(
                    "sidewayoutput\\basicmanim\\transform001a_01_01_01_01_01.wav", time_offset=18)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\transform001a_01_01_01_02_01.wav", time_offset=93)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\transform001a_01_01_01_03_01.wav", time_offset=135)
            except:
                pass
            self.play(StartScreens01(
                [], [],
                [[r"\textbf{\textit{Basic-Manim from }\{Sideway\}}"],
                 [r"\textbf{\textit{Transform}}\\{{Part\ \textspA{I}a}"],
                 [r"\tiny{\textrm{basic-manim.210200551v0\_transform001a}}"],
                 [],
                 [r"\scriptsize{\textbf{Warning:\ The\ content\ may\ contain\ errors,\ mistakes\ and\ inaccuracies.\ Information\ must\ be\ verified\ and\ evaluated\ before\ use.}}"]],))
        if 1 == 1:
            self.play(GrowFromCenter(TextMobject(
                r"\textit{\textbf{\underline{Transform}}}").shift([0, 3.6, 0])))
            squarea = Square()
            squareb = Square(side_length=4).shift([4, 0, 0])
            circlea = Circle()
            circleb = Circle(radius=2).shift([-4, 0, 0])
            linea = Line([-4, 3, 0], [4, 3, 0])
            lineb = Line([-3, -3, 0], [3, -3, 0])
            texta = TextMobject("AB").shift([0, -2.5, 0])
            textb = TextMobject("HI").shift([0, 2.5, 0])
            self.play(ShowCreation(Group(squarea, circlea, squareb, circleb, linea, lineb),
                                   lag_ratio=1, run_time=12))
            self.play(Write(VGroup(texta, textb), lag_ratio=1, run_time=10))
            self.play(Transform(circlea, squarea, run_time=5))
            self.play(Transform(circlea, squareb, path_arc=3, run_time=5))
            self.play(Transform(squarea, circleb, path_arc=3, run_time=5))
            self.play(Transform(linea, lineb, path_arc=3, run_time=5))
            self.play(Transform(linea, circleb, path_arc=3, run_time=5))
            self.play(Transform(squareb, lineb, path_arc=3, run_time=5))
            self.play(Transform(texta, textb, path_arc=3, run_time=5))
            self.play(Transform(texta, circleb, path_arc=3, run_time=5))
            self.play(Transform(squareb, textb, path_arc=3, run_time=5))
            self.fadeout()
        if 1 == 1:
            self.play(GrowFromCenter(TextMobject(
                r"\textit{\textbf{\underline{Paths\ of\ Transform}}}").shift([0, 3.6, 0])))
            rows, cols = (7, 5)
            x0, y0 = axes_point([0, 2, cols-1, -4], [2.3, -1, rows-1, 3])
            txtx = ["loc 1", "loc 2", "m1", "m2"]
            txty = ["ClockwiseTransform", "Transform",
                    "CounterclockwiseTransform"]
            a1 = Group()
            a2 = Group()
            a3 = Group()
            a4 = Group()
            for j in range(1, rows):
                a1.add(Circle().scale(0.2).move_to([x0[1], y0[j], 0]))
                a2.add(Square().scale(0.2).move_to([x0[2], y0[j], 0]))
                a3.add(Dot([x0[3], y0[j], 0]).add_updater(
                    lambda mob, obj=a1[j-1], x=x0[3], y=y0[j]: mob.become(obj.copy().move_to([x, y, 0]))).suspend_updating())
                a4.add(Dot([x0[4], y0[j], 0]).add_updater(
                    lambda mob, obj=a2[j-1], x=x0[4], y=y0[j]: mob.become(obj.copy().move_to([x, y, 0]))).suspend_updating())
            self.play(FadeIn(Group(
                *[TextMobject(txtx[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[1:], y0[0:1]))],
                *[TextMobject(txty[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0[1::2]))],
                *[Dot(each) for each in coord_grid(x0[1:3], y0[1:])],
                TextMobject(r"$\rightarrow$").move_to(
                    ([(x0[1]+x0[2])/2, y0[0], 0])),
                a1[::2],
                a2[::2],
                a3,
                a4,
                *[Square(stroke_width=2, color="#FFFF00", fill_opacity=0.3).add_updater(
                    lambda mob, obj=obj:mob.surround(obj, stretch=True, buff=0.2)) for obj in a1],
                *[Square(stroke_width=2, color="#DC75CD").add_updater
                        (lambda mob, obj=obj:mob.surround(obj, stretch=True, buff=0.3)) for obj in a2]
            )), run_time=5)
            self.wait(2)
            self.play(AnimationGroup(
                ClockwiseTransform(a2[0], a1[0]),
                ClockwiseTransform(a1[1], a2[1]),
                Transform(a1[2], a2[2]),
                Transform(a2[3], a1[3]),
                CounterclockwiseTransform(a1[4], a2[4]),
                CounterclockwiseTransform(a2[5], a1[5]),
            ), run_time=25)
            self.wait(3)
            a1.shift([0.3, 0, 0]).set_color("#11FF00")
            self.wait(3)
            self.play(ApplyMethod(
                a1.shift, ([0.3, 0, 0])), run_time=3)
            self.fadeout()
        if 1 == 1:
            self.play(GrowFromCenter(TextMobject(
                r"\textit{\textbf{\underline{Methods\ of\ Transform}}}").shift([0, 3.6, 0])))
            rows, cols = (9, 5)
            x0, y0 = axes_point([0, 2, cols-1, -4], [2.3, -0.8, rows-1, 3])
            txtx = ["loc 1", "loc 2", "m1", "m2"]
            txty = ["Transform", "ReplacementTransform",
                    "TransformFromCopy", "MoveToTarget"]
            a1 = Group()
            a2 = Group()
            a3 = Group()
            a4 = Group()
            for j in range(1, rows):
                a1.add(Circle().scale(0.2).move_to([x0[1], y0[j], 0]))
                a2.add(Square().scale(0.2).move_to([x0[2], y0[j], 0]))
                a3.add(Dot().move_to([x0[3], y0[j], 0]).add_updater(
                    lambda mob, obj=a1[j-1], x=x0[3], y=y0[j]: mob.become(obj.copy().move_to([x, y, 0]))).suspend_updating())
                a4.add(Dot().move_to([x0[4], y0[j], 0]).add_updater(
                    lambda mob, obj=a2[j-1], x=x0[4], y=y0[j]: mob.become(obj.copy().move_to([x, y, 0]))).suspend_updating())
            a1[6].target = a2[6]
            a1[7].target = a2[7]
            self.play(FadeIn(Group(
                *[TextMobject(txtx[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[1:], y0[0:1]))],
                *[TextMobject(txty[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0[1::2]))],
                *[Dot(each) for each in coord_grid(x0[1:3], y0[1:])],
                TextMobject(r"$\rightarrow$").move_to(
                    ([(x0[1]+x0[2])/2, y0[0], 0])),
                a1[::2],
                a2[::2],
                a3,
                a4,
                Group(*[Square(stroke_width=2, color="#FFFF00", fill_opacity=0.3).add_updater(
                    lambda mob, obj=obj:mob.surround(obj, stretch=True, buff=0.2)) for obj in a1]),
                Group(*[Square(stroke_width=2, color="#DC75CD").add_updater
                        (lambda mob, obj=obj:mob.surround(obj, stretch=True, buff=0.3)) for obj in a2])
            )), run_time=5)
            self.wait(2)
            self.play(AnimationGroup(
                Transform(a1[0], a2[0]),
                Transform(a1[1], a2[1]),
                ReplacementTransform(a1[2], a2[2]),
                ReplacementTransform(a1[3], a2[3]),
                TransformFromCopy(a1[4], a2[4]),
                TransformFromCopy(a1[5], a2[5]),
                MoveToTarget(a1[6]),
                MoveToTarget(a1[7])
            ), run_time=40)
            self.wait(3)
            a1.shift([0.3, 0, 0]).set_color("#11FF00")
            self.wait(10)
            self.play(ApplyMethod(
                a1.shift, ([0.3, 0, 0])), run_time=5)
            self.fadeout()
        if 1 == 1:
            self.play(EndScreen01())
        self.wait(5)
