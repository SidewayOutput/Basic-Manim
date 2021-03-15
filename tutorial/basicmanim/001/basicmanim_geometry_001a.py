# folder/file: tutorial/basicmanim/001/basicmanim_geometry_001a.py

from manimlib.animation.growing import GrowFromCenter
from manimlib.basic.basic_complex import StartScreens01, EndScreen01
from manimlib.basic.basic_function import axes_point, coord_grid
from manimlib.basic.basic_geometry import GeomPoint
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.mobject.geometry import TipableVMobject, Arc, ArcBetweenPoints, CurvedArrow, CurvedDoubleArrow, Circle, Dot, SmallDot, Ellipse, Annulus, AnnularSector, Sector, Line, DashedLine, TangentLine, Arrow, Vector, DoubleArrow, Elbow, CubicBezier, Polygon, RegularPolygon, Triangle, ArrowTip, Rectangle, Square, RoundedRectangle, TipableVMobject, TipableVMobject, TipableVMobject
from manimlib.scene.scene import Scene
from manimlib.constants import LO, RO, RU, LU


class basicmanim_geometry_001a(Scene):
    def construct(self):
        if 1 == 1:
            try:
                self.add_sound(
                    "sidewayoutput\\basicmanim\\geometry001a_01_01_01_01_01.wav", time_offset=20)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\geometry001a_01_01_01_02_01.wav", time_offset=68)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\geometry001a_01_01_01_02_02.wav", time_offset=87)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\geometry001a_01_01_01_02_03.wav", time_offset=100)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\geometry001a_01_01_01_03_01.wav", time_offset=115)
                self.add_sound(
                    "sidewayoutput\\basicmanim\\geometry001a_01_01_01_03_02.wav", time_offset=131)
            except:
                pass
            self.play(StartScreens01(
                [], [],
                [[r"\textbf{\textit{Basic-Manim from }\{Sideway\}}"],
                 [r"\textbf{\textit{Geometry}}\\{{Part\ \textspA{I}a}"],
                 [r"\tiny{\textrm{basic-manim.210301551v0\_geometry001a}}"],
                 [],
                 [r"\scriptsize{\textbf{Warning:\ The\ content\ may\ contain\ errors,\ mistakes\ and\ inaccuracies.\ Information\ must\ be\ verified\ and\ evaluated\ before\ use.}}"]],))
        if 1 == 1:
            self.grow(r"\titleA{Geometry}", shift=[0, 3.6, 0])
            rows, cols = (10, 6)
            x0, y0 = axes_point([-5.5, 2.3, cols], [3, -0.7, rows])
            txty = ["TipableVMobject()", "Arc(radius=0.5)", "ArcBetweenPoints(LO,RO)", "CurvedArrow(LO,RO)", "CurvedDoubleArrow(LO,RO)", "Circle(radius=0.5)", "Dot()", "SmallDot()", "Ellipse()", "Annulus(inner_radius=0.25,outer_radius=0.5)", "AnnularSector(inner_radius=0.25,outer_radius=0.5)", "Sector(outer_radius=0.5)", "Line()", "DashedLine()", "TangentLine(Circle(),0)","Arrow()", "Vector()", "DoubleArrow()", "Elbow()", "CubicBezier([RO,RU/2,LU/2,LO])", "Polygon(RO,RU/2,LU/2,LO)", "RegularPolygon().scale(0.5)", "Triangle().scale_about_point(0.5,[0,0,0])", "ArrowTip()", "Rectangle().scale(0.5)", "Square().scale(0.5)", "RoundedRectangle().scale(0.5)", "TipableVMobject()", "TipableVMobject()", "TipableVMobject()"]
            strs = txty
            self.grow(
                *[GeomPoint().move_to(each)
                  for i, each in enumerate(coord_grid(x0[:], y0[1::2])[:-3])],
            )
            txty = ["TextMobject('"+txty[i].split('(', 1)[0]+"').scale(0.55).move_to(["+','.join(map(str, each))+"])"
                    for i, each in enumerate(coord_grid(x0[:], y0[0::2]))]
            strs = [strs[i]+".shift(["+','.join(map(str, each))+"])" for i,
                    each in enumerate(coord_grid(x0[:], y0[1::2]))]
            strs = [j for i in zip(txty, strs) for j in i][:-6]
            exec("self.create(" +
                 ','.join(strs) +
                 ", run_time=42, lag_ratio=1)")
            self.fadeout()
        if 1 == 1:
            self.play(GrowFromCenter(TextMobject(
                r"\titleA{TipableVMobject(VMobject)}").shift([0, 3.6, 0]).add_as_foreground(self)))
            rows, cols = (5, 3)
            x0, y0 = axes_point([1.1, 4.5, cols-1, -4.5], [2.5, -1.2, rows])
            txty = ["TipableVMobject()", "Arc(radius = 0.5)", "ArcBetweenPoints(LO,RO)",
                    "CurvedArrow(LO,RO)", r"\parbox{25em}{CurvedDoubleArrow(\bR{LO,RO)"]
            strs = txty
            self.fadein(
                *[TextMobject(txty[i].split('(', 1)[0]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0))],
                run_time=5)
            self.grow(*[TextMobject(strs[i]).move_to(each)
                        for i, each in enumerate(coord_grid(x0[1:2], y0))],
                      *[GeomPoint().move_to(each)
                        for i, each in enumerate(coord_grid(x0[2:3], y0))],
                      )
            strs = [strs[i].replace("\\bR{", "").replace("\\parbox{25em}{", "").replace("\\", "")+".shift(["+','.join(
                map(str, each))+"])" for i, each in enumerate(coord_grid(x0[2:3], y0))]
            exec("self.create(" +
                 ','.join(strs) +
                 ", run_time=10, lag_ratio=0)")
            self.fadeout(exclude_mobjs="foreground")
        if 1 == 1:
            rows, cols = (7, 3)
            x0, y0 = axes_point([1.1, 4.5, cols-1, -4.5], [3, -1.1, rows])
            txty = ["Circle(radius = 0.5)", "Dot()", "SmallDot()", "Ellipse()", r"\parbox{25em}{Annulus(inner\_radius = 0.25, \bR{outer\_radius = 0.5)",
                    r"\parbox{25em}{AnnularSector(inner\_radius\bR{= 0.25, outer\_radius = 0.5)", r"Sector(outer\_radius = 0.5)"]
            strs = txty
            self.fadein(
                *[TextMobject(txty[i].split('(', 1)[0]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0))],
                run_time=5)
            self.grow(*[TextMobject(strs[i]).move_to(each)
                        for i, each in enumerate(coord_grid(x0[1:2], y0))],
                      *[GeomPoint().move_to(each)
                        for i, each in enumerate(coord_grid(x0[2:3], y0))],
                      )
            strs = [strs[i].replace("\\bR{", "").replace("\\parbox{25em}{", "").replace(
                "\\", "")+".shift(["+','.join(map(str, each))+"])" for i, each in enumerate(coord_grid(x0[2:3], y0))]
            exec("self.create(" +
                 ','.join(strs) +
                 ", run_time=6, lag_ratio=0)")
            self.fadeout(exclude_mobjs="foreground")
        if 1 == 1:
            rows, cols = (6, 3)
            x0, y0 = axes_point([1.1, 4.5, cols-1, -4.5], [3, -1.1, rows])
            txty = ["Line()", "DashedLine()", "TangentLine(Circle(), 0)",
                    "Arrow()", "Vector()", "DoubleArrow()"]
            strs = txty
            self.fadein(
                *[TextMobject(txty[i].split('(', 1)[0]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0))],
                run_time=5)
            self.grow(*[TextMobject(strs[i]).move_to(each)
                        for i, each in enumerate(coord_grid(x0[1:2], y0))],
                      *[GeomPoint().move_to(each)
                        for i, each in enumerate(coord_grid(x0[2:3], y0))],
                      )
            strs = [strs[i].replace("\\bR{", "").replace("\\parbox{25em}{", "").replace(
                "\\", "")+".shift(["+','.join(map(str, each))+"])" for i, each in enumerate(coord_grid(x0[2:3], y0))]
            exec("self.create(" +
                 ','.join(strs) +
                 ", run_time=5, lag_ratio=0)")
            self.fadeout()
        if 1 == 1:
            self.play(GrowFromCenter(TextMobject(
                r"\titleA{VMobject}").shift([0, 3.6, 0]).add_as_foreground(self)))
            rows, cols = (3, 3)
            x0, y0 = axes_point([1.1, 4.5, cols-1, -4.5], [3, -1.1, rows])
            txty = ["Elbow()", r"\parbox{25em}{CubicBezier(\bR{[RO, RU/2, LU/2, LO])",
                    r"\parbox{25em}{Polygon(\bR{RO, RU/2, LU/2, LO)"]
            strs = txty
            self.fadein(
                *[TextMobject(txty[i].split('(', 1)[0]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0))],
                run_time=5)
            self.grow(*[TextMobject(strs[i]).move_to(each)
                        for i, each in enumerate(coord_grid(x0[1:2], y0))],
                      *[GeomPoint().move_to(each)
                        for i, each in enumerate(coord_grid(x0[2:3], y0))],
                      )
            strs = [strs[i].replace("\\bR{", "").replace("\\parbox{25em}{", "").replace(
                "\\", "")+".shift(["+','.join(map(str, each))+"])" for i, each in enumerate(coord_grid(x0[2:3], y0))]
            exec("self.create(" +
                 ','.join(strs) +
                 ", run_time=7, lag_ratio=0)")
            self.fadeout(exclude_mobjs="foreground")
        if 1 == 1:
            rows, cols = (6, 3)
            x0, y0 = axes_point([1.1, 4.5, cols-1, -4.5], [3, -1.1, rows])
            txty = ["RegularPolygon().scale(0.5)", r"\parbox{25em}{Triangle().scale\_about\_point(\bR{0.5, [0, 0, 0])",
                    "ArrowTip()", "Rectangle().scale(0.5)", "Square().scale(0.5)", r"\parbox{25em}{RoundedRectangle()\bR{.scale(0.5)"]
            strs = txty
            self.fadein(
                *[TextMobject(txty[i].split('(', 1)[0]).move_to(each)
                  for i, each in enumerate(coord_grid(x0[0:1], y0))],
                run_time=5)
            self.grow(*[TextMobject(strs[i]).move_to(each)
                        for i, each in enumerate(coord_grid(x0[1:2], y0))],
                      *[GeomPoint().move_to(each)
                        for i, each in enumerate(coord_grid(x0[2:3], y0))],
                      )
            strs = [strs[i].replace("\\bR{", "").replace("\\parbox{25em}{", "").replace(
                "\\", "")+".shift(["+','.join(map(str, each))+"])" for i, each in enumerate(coord_grid(x0[2:3], y0))]
            exec("self.create(" +
                 ','.join(strs) +
                 ", run_time=9, lag_ratio=0)")
            self.fadeout()
        if 1 == 1:
            self.play(EndScreen01())
        self.wait(5)
