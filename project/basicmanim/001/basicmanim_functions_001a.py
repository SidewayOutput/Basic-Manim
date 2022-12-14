# folder/file: tutorial/basicmanim/001/basicmanim_functions_001a.py

from manimlib.basic.basic_complex import StartScreens01, EndScreen01
from manimlib.basic.basic_function import axes_point, coord_grid
from manimlib.basic.basic_geometry import GeomPoint, GeomSquare
from manimlib.mobject.functions import FunctionGraph, FunctionsGraph, ParametricCurve, ParametricFunction
from manimlib.mobject.svg.tex_mobject import TextMobject
from manimlib.scene.three_d_scene import Scene


class basicmanim_functions_001a(Scene):
    def construct(self):
        if 1 == 1:
            try:
                self.add_sound(
                    "sidewayoutput\\basicmanim\\functions001a_01_01_01_01_01.wav", time_offset=19)
            except:
                pass
            self.play(StartScreens01(
                [], [],
                [[r"\textbf{\textit{Basic-Manim from }\{Sideway\}}"],
                 [r"\textbf{\textit{Functions}}\\{{Part\ \textspA{I}a}"],
                 [r"\tiny{\textrm{basic-manim.210300151v0\_functions001a}}"],
                 [],
                 [r"\scriptsize{\textbf{Warning:\ The\ content\ may\ contain\ errors,\ mistakes\ and\ inaccuracies.\ Information\ must\ be\ verified\ and\ evaluated\ before\ use.}}"]],))
        if 1 == 1:
            self.grow(r"\titleA{Functions}", shift=[0, 3.6, 0])
            rows, cols = (4, 3)
            x0, y0 = axes_point([1.1, 4.5, cols-1, -4.2], [2.5, -1.8, rows])
            txty = [r"ParametricCurve \\\tiny(replacing ParametricFunction)",
                    "ParametricFunction", "FunctionGraph", "FunctionsGraph"]
            strs = ["\\parbox{25em}{"+txty[i].split(" ", 1)[0]+"("+each+")" for i, each in
                    enumerate([r"\bR{lambda t:[t,t**2,0],\bR{(-1,1,0.01)",
                               r"\bR{lambda t:[t,t**2,0],\bR{t\_min=-1, t\_max=1",
                               r"\bR{lambda t:t**2,\bR{(-1,1,0.01)",
                               r"\bR{'lambda t:t, (-1,0,0.01)',\bR{'lambda t:0, (0,1,0.01)'"])]
            self.fadein(
                *[TextMobject(txty[i]).move_to(each)
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
                 ", run_time=48, lag_ratio=0)")
            self.fadeout()
        if 1 == 1:
            self.play(EndScreen01())
        self.wait(5)
