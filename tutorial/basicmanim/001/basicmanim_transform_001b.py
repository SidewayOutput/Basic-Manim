# folder/file: tutorial/basicmanim/basicmanim_transform_001b.py

import numpy as np

from manimlib.constants import RED
from manimlib.animation.composition import AnimationGroup
from manimlib.animation.creation import ShowCreation
from manimlib.animation.growing import GrowFromCenter
from manimlib.animation.transform import ApplyComplexFunction, ApplyFunction, ApplyMatrix, ApplyMethod, ApplyPointwiseFunction, CyclicReplace, FadeToColor, ScaleInPlace, ShrinkToCenter, Swap, Transform, Restore
from manimlib.basic.basic_animation import IndicateThenFadeOut
from manimlib.basic.basic_complex import EndScreen01, StartScreens01
from manimlib.basic.basic_function import axes_point, coord_grid, to_get_zlist
from manimlib.basic.basic_geometry import GeomLine, GeomPoint, GeomRegularPolygon, GeomSquare
from manimlib.basic.basic_mobject import MobjectOrChars
from manimlib.mobject.geometry import Circle
from manimlib.mobject.mobject import Group
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.scene.scene import Scene


class basicmanim_transform_001b(Scene):

    def construct(self):
        if 1 == 1:
            try:
                self.add_sound(
                    "sidewayoutput\\basicmanim\\transform001b_01_01_02_01_01.wav", time_offset=18)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\transform001b_01_01_02_02_01.wav", time_offset=48)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\transform001b_01_01_02_02_02.wav", time_offset=93)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\transform001b_01_01_02_03_01.wav", time_offset=148)
            except:
                pass
            self.play(StartScreens01(
                [], [],
                [[r"\textbf{\textit{Basic-Manim from }\{Sideway\}}"],
                 [r"\textbf{\textit{Transform}}\\{Part\ \textspA{I}b}"],
                 [r"\tiny{\textrm{basic-manim.210201951v0\_transform001b}}"],
                 [],
                 [r"\scriptsize{\textbf{Warning:\ The\ content\ may\ contain\ errors,\ mistakes\ and\ inaccuracies.\ Information\ must\ be\ verified\ and\ evaluated\ before\ use.}}"]],))
        if 1 == 1:
            self.play(GrowFromCenter(TextMobject(
                r"\textit{\textbf{\underline{Apply\ Transform}}}").shift([0, 3.6, 0])))
            rows, cols = (7, 3)
            x = 5.
            x0, y0 = axes_point([-2.5, x, cols-1, -5], [2., -1.1, rows-1, 3])
            txtx = ["\\underline{state 1}", "\\underline{state 2}"]
            txty = ["Method", "ApplyMethod", "ApplyFunction"]

            a1 = ["\\normalsize{sq[0]}",
                  "\\normalsize{sq[1]}", "\\normalsize{sq[2]}"]
            a2 = [r"\normalsize{sq[0]\\.shift(["+str(x)+r",\,0,\,0])}", r"\normalsize{ApplyMethod(\\sq[1].shift,\,["+str(
                x)+r",\,0,\,0])}", r"\normalsize{ApplyFunction(\\lambda\,mob:\,mob.shift(["+str(x)+r",\,0,\,0]),\,sq[2])}"]
            sq = [GeomSquare(0.75) for i in range(3)]

            self.fadein(
                *[TextMobject(txtx[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[1:], y0[0:1]))],
                *[TextMobject(txty[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0[1::2]))],
                *[GeomPoint(each)
                  for each in coord_grid(x0[1:3], y0[2::2])],
                *[MobjectOrChars(np.ravel(list(zip(a1, a2)))[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[1:3], y0[1::2]))],
                *[sq[i].move_to(each)
                  for i, each in enumerate(coord_grid(x0[1:2], y0[2::2]))],
                run_time=5)
            self.play(AnimationGroup(ShowCreation(sq[0].shift([x, 0, 0]), run_time=0), ApplyMethod(sq[1].shift, [x, 0, 0]), ApplyFunction(lambda mob: mob.shift([x, 0, 0]), sq[2])),
                      run_time=15)
            self.fadeout()
        if 1 == 1:
            self.play(GrowFromCenter(TextMobject(
                r"\textit{\textbf{\underline{Apply Method}}}").shift([0, 3.6, 0]).add_as_foreground(self)))
            rows, cols = (8, 2)
            x0, y0 = axes_point([-1.5, 6, cols], [3, -0.9, rows])
            txty = [MobjectOrChars(each) for each in
                    [r"FadeToColor(sq[0],\,RED)", r"ScaleInPlace(sq[1],\,0.5))", "ShrinkToCenter(sq[2])", "Restore(sq[3])"]]
            a1 = [MobjectOrChars(
                "\\normalsize{sq["+str(i)+"]}") for i in range(4)]
            sq = [GeomSquare(0.75) for i in range(4)]
            self.fadein(
                *[to_get_zlist(a1, sq)[i].move_to(each)
                  for i, each in enumerate(coord_grid(x0[1:2], y0))],
                *[GeomPoint(each)
                  for each in coord_grid(x0[1:2], y0[1::2])],
            )
            self.wait()
            sq[3].save_state()
            self.play(AnimationGroup(
                IndicateThenFadeOut(TextMobject(
                    r"Transform(sq[3], Circle().scale(0.375).\\move\_to(sq[3]).shift([1, 0, 0])))").
                    move_to([x0[0], y0[7], 0]), scale_factor=1, ratio_array=[1, 0]),
                Transform(sq[3], Circle().scale(0.375).move_to(sq[3]).shift([1, 0, 0]))),
                run_time=5)
            self.wait()
            self.fadein(
                *[txty[i].move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0[1::2]))],
            )
            self.play(AnimationGroup(
                FadeToColor(sq[0], RED),
                ScaleInPlace(sq[1], 0.5),
                ShrinkToCenter(sq[2]),
                Restore(sq[3]),
            ), run_time=35)
            self.fadeout(exclude_mobjs="foreground")
        if 1 == 1:
            rows, cols = (6, 2)
            x0, y0 = axes_point([-1.5, 6, cols], [3, -0.9, rows])
            txty = [MobjectOrChars(each) for each in
                    [r"ApplyPointwiseFunction(\\lambda\,pointarray:\,pointarray\,+\,[1,\,0,\,0],\,sq[0])",
                     r"ApplyMatrix([[1.23,\,0.9],\,[0,\,1]],\,sq[1])",
                     r"ApplyComplexFunction(lambda pointarray:\\pointarray\,+\,np.complex(1,\,0),\,sq[2])",
                     ]]
            a1 = [MobjectOrChars(
                "\\normalsize{sq["+str(i)+"]}") for i in range(4)]
            sq = [GeomSquare(0.75) for i in range(4)]
            self.fadein(
                *[to_get_zlist(a1, sq)[i].move_to(each)
                  for i, each in enumerate(coord_grid(x0[1:2], y0))],
                *[GeomPoint(each)
                  for each in coord_grid(x0[1:2], y0[1::2])],
            )
            self.wait()
            self.fadein(
                *[txty[i].move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0[1::2]))],
            )
            self.play(AnimationGroup(
                ApplyPointwiseFunction(
                    lambda pointarray: pointarray + [1, 0, 0], sq[0]),
                ApplyMatrix([[1.23, 0.9], [0, 1]], sq[1]),
                ApplyComplexFunction(
                    lambda pointarray: pointarray + np.complex(1, 0), sq[2]),
            ), run_time=45)
            self.fadeout()
        if 1 == 1:
            self.play(GrowFromCenter(TextMobject(
                r"\textit{\textbf{\underline{Swap Method}}}").shift([0, 3.6, 0])))
            rows, cols = (2, 2)
            count = m, n = [2, 6]
            x0, y0 = axes_point([-3.5, 6, cols], [2.4, -3.7, rows])
            geometrys = [GeomLine(), GeomRegularPolygon(n, radius=2)]
            txty = [MobjectOrChars(each) for each in
                    [r"Swap(*sqs)\\ \tiny{(same as CyclicReplace)}",
                     r"CyclicReplace(*sqs)",
                     ]]
            titles = [[MobjectOrChars("\\normalsize{sq["+str(i)+"]}")
                       for i in range(m)],
                      [MobjectOrChars("\\normalsize{sq["+str(i)+"]}")
                       for i in range(n)],
                      ]
            sqs = [[GeomSquare(1.) for i in range(m)],
                   [GeomSquare(1.) for i in range(n)],
                   ]
            [[sq.add(title).add(GeomPoint()) for sq, title in zip(
                sqs[i], titles[i])] for i in range(len(count))]
            self.fadein(
                *[geometrys[i].move_to(each)
                  for i, each in enumerate(coord_grid(x0[1:], y0[0:]))])
            self.fadein(
                *[Group(
                    *[sqs[j][i].move_to(each)
                      for i, each in enumerate(geometrys[j].get_counting_points())])
                  for j in range(2)
                  ])
            self.fadein(
                *[txty[i].move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0[0:]))],)
            self.play(AnimationGroup(
                Swap(*sqs[0]),
                CyclicReplace(*sqs[1]),
            ), run_time=35)
            self.fadeout()
        if 1 == 1:
            self.play(EndScreen01())
        self.wait(5)
