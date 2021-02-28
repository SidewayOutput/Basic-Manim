# folder/file: tutorial/basicmanim/001/basicmanim_growing_001a.py

from manimlib.animation.growing import DiminishArrow, DiminishToCenter, DiminishToPoint, DiminishToEdge, DiminishToSide, ExpandArrow, GrowArrow, GrowFromCenter, GrowFromPoint, GrowFromEdge, GrowFromSide, RetractArrow, SpinInFromNothing, SpinInFrom, SpinInTo, SpinOutFrom, SpinOutTo
from manimlib.basic.basic_complex import StartScreens01, EndScreen01
from manimlib.basic.basic_function import axes_point, coord_grid, to_get_zlist
from manimlib.basic.basic_geometry import GeomArrow, GeomPoint, GeomRectangle, GeomSquare, GeomRegularPolygon
from manimlib.mobject.mobject import Group
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.scene.scene import Scene
from manimlib.constants import ORIGIN, UP


class basicmanim_growing_001a(Scene):
    def construct(self):
        if 1 == 1:
            try:
                self.add_sound(
                    "sidewayoutput\\basicmanim\\growing001a_01_01_01_01_01.wav", time_offset=19)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\growing001a_01_01_01_02_01.wav", time_offset=43)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\growing001a_01_01_01_03_01.wav", time_offset=89)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\growing001a_01_01_01_04_01.wav", time_offset=136)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\growing001a_01_01_01_05_01.wav", time_offset=180)
            except:
                pass
            self.play(StartScreens01(
                [], [],
                [[r"\textbf{\textit{Basic-Manim from }\{Sideway\}}"],
                 [r"\textbf{\textit{Growing}}\\{{Part\ \textspA{I}a}"],
                 [r"\tiny{\textrm{basic-manim.210300151v0\_growing001a}}"],
                 [],
                 [r"\scriptsize{\textbf{Warning:\ The\ content\ may\ contain\ errors,\ mistakes\ and\ inaccuracies.\ Information\ must\ be\ verified\ and\ evaluated\ before\ use.}}"]],))
        if 1 == 1:
            self.grow(r"\titleA{Growing}", shift=[0, 3.6, 0])
            rows, cols = (4, 3)
            x0, y0 = axes_point([1, 4, cols-1, -4.5], [2.5, -1.9, rows])
            txty = ["Growing", " Diminishing", "One Direction", "Spin"]
            strs = [each+"(sqs["+str(i)+"])" for i, each in
                    enumerate(["GrowFromCenter",
                               "DiminishToCenter",
                               "GrowArrow",
                               "SpinInFromNothing"])]
            sqs = [GeomSquare(1.2) for i in range(rows)]
            self.fadein(
                *[TextMobject(txty[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0))],
                *[Group(GeomPoint(), TextMobject("sqs["+str(i)+"]"), sqs[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[2:3], y0))],
                run_time=5)
            self.grow(*[TextMobject(strs[i]).move_to(each)
                          for i, each in enumerate(coord_grid(x0[1:2], y0))])
            exec("self.play(" +
                 ','.join(strs) + "," +
                 "run_time=15)")
            self.fadeout()
        if 1 == 1:
            self.grow(r"\titleA{GrowFrom}", shift=[0, 3.6, 0])
            rows, cols = (4, 3)
            x0, y0 = axes_point([1, 4, cols-1, -4.5], [2.5, -1.9, rows])
            txty = ["GrowFromPoint", "GrowFromCenter",
                    "GrowFromEdge", "GrowFromSide"]
            strs = [txty[i]+"(sqs["+str(i)+"]"+each+")" for i, each in
                    enumerate([",UP",
                               "",
                               ",UP",
                               ",UP"])]
            sqs = [GeomSquare(1.2) for i in range(rows)]
            self.fadein(
                *[TextMobject(txty[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0))],
                *[Group(GeomPoint(), TextMobject("sqs["+str(i)+"]"), sqs[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[2:3], y0))],
                run_time=5)
            self.grow(*[TextMobject(strs[i]).move_to(each)
                          for i, each in enumerate(coord_grid(x0[1:2], y0))])
            exec("self.play(" +
                 ','.join(strs) + "," +
                 "run_time=35)")
            self.fadeout()
        if 1 == 1:
            self.grow(r"\titleA{DiminishTo}", shift=[0, 3.6, 0])
            rows, cols = (4, 3)
            x0, y0 = axes_point([1, 4, cols-1, -4.5], [2.5, -1.9, rows])
            txty = ["DiminishToPoint", "DiminishToCenter",
                    "DiminishToEdge", "DiminishToSide"]
            strs = [txty[i]+"(sqs["+str(i)+"]"+each+")" for i, each in
                    enumerate([",UP",
                               "",
                               ",UP",
                               ",UP"])]
            sqs = [GeomSquare(1.2) for i in range(rows)]
            self.fadein(
                *[TextMobject(txty[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0))],
                *[Group(GeomPoint(), TextMobject("sqs["+str(i)+"]"), sqs[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[2:3], y0))],
                run_time=5)
            self.grow(*[TextMobject(strs[i]).move_to(each)
                          for i, each in enumerate(coord_grid(x0[1:2], y0))])
            exec("self.play(" +
                 ','.join(strs) + "," +
                 "run_time=38)")
            self.fadeout()
        if 1 == 1:
            self.grow(r"\titleA{One Direction}", shift=[0, 3.6, 0])
            rows, cols = (8, 3)
            x0, y0 = axes_point([1, 4, cols-1, -4.5], [2.8, -0.9, rows])
            txty = to_get_zlist(
                ["GrowArrow", "ExpandArrow", "DiminishArrow", "RetractArrow"], n=2)
            strs = [txty[i]+"(sqs["+str(i)+"])" for i in range(rows)]
            sqs = to_get_zlist([GeomRectangle(0.6, 1.2), GeomArrow()], n=(4,))
            self.fadein(
                *[TextMobject(txty[i*2]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0[:-1:2]))],
                *[Group(GeomPoint(), TextMobject("sqs["+str(i)+"]"), sqs[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[2:3], y0))],
                run_time=5)
            self.fadein(*[TextMobject(strs[i]).move_to(each)
                          for i, each in enumerate(coord_grid(x0[1:2], y0))])
            exec("self.play(" +
                 ','.join(strs) + "," +
                 "run_time=35)")
            self.fadeout()
        if 1 == 1:
            self.grow(r"\titleA{Spin}", shift=[0, 3.6, 0])
            rows, cols = (5, 3)
            x0, y0 = axes_point([1.8, 4, cols-1, -4.2], [3, -1.5, rows])
            txty = ["SpinInFromNothing", "SpinInFrom", "SpinOutFrom",
                    "SpinInTo", "SpinOutTo"]
            strs = [txty[i]+"(sqs["+str(i)+"]"+each+")" for i, each in
                    enumerate(["", "", "", "", ""])]
            sqs = [GeomRegularPolygon(5, ORIGIN, 0.8).add(
                GeomArrow([0, 0.07, 0], [0, 0.8, 0])) for i in range(rows)]
            self.fadein(
                *[TextMobject(txty[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0))],
                *[Group(GeomPoint(), TextMobject("sqs["+str(i)+"]"), sqs[i]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[2:3], y0))],
                run_time=5)
            self.grow(*[TextMobject(strs[i]).move_to(each)
                          for i, each in enumerate(coord_grid(x0[1:2], y0))])
            exec("self.play(" +
                 ','.join(strs) + "," +
                 "run_time=50)")
            self.fadeout()
        if 1 == 1:
            self.play(EndScreen01())
        self.wait(5)
