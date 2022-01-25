import numpy as np
from manimlib.basic.basic_function import to_get_offset_lists, to_get_offsets
from manimlib.constants import BLUE, DARK_GRAY,DOWN, DEGREES, DL, DR, LEFT,  ORIGIN, OUT, RED, RIGHT, UL, UR, WHITE, UP, GRAY, PI, TAU, DEFAULT_STROKE_WIDTH,DEFAULT_ARROW_TIP_LENGTH,GOLD
from manimlib.mobject.geometry import Line, Polygon, Arc, ArrowTip, CurveLine, Triangle,TipableVMobject, Circle, Ellipse
from manimlib.mobject.mobject import Mobject, Location
from manimlib.mobject.types.vectorized_mobject import VGroup, VMobject
from manimlib.utils.config_ops import digest_config, generate_args, generate_args_kwargs, merge_config_kwargs
from manimlib.utils.space_ops import compass_directions, rotate_vector, normalize, angle_of_vector, line_intersection, spaceangle_between
from manimlib.utils.space_ops import get_norm

class GeomPoint(VMobject):
    '''
    [mobject_or_point], {from_offset},      {to_offset} -->default
    {length},           [mobject_or_point]
    '''
    CONFIG = {
        "color": BLUE,
        "stroke_width": 2,
    }

    def __init__(self, *args, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.add_element(*args, **kwargs)

    def add_element(self, *args, **kwargs):
        if not args or isinstance(args[0], (Mobject, list)) or not isinstance(args[0], (int, float, tuple)):
            self.mobject_or_point, self.from_offset, self.to_offset, kwargs = \
                generate_args_kwargs(self, args, kwargs,
                                     ["mobject_or_point", "from_offset", "to_offset"],
                                     [ORIGIN, -0.1, 0.1]
                                     )
        elif isinstance(args[0], (int, float, tuple)):
            self.length, self.mobject_or_point = \
                generate_args(self, args,
                              [0.2, ORIGIN])
            if isinstance(self.length, tuple):
                self.length = list(self.length)
            self.from_offset, self.to_offset = to_get_offsets(self.length, 2)
            kwargs = merge_config_kwargs(self, kwargs,
                                         ["length", "mobject_or_point"]
                                         )
        else:
            self.mobject_or_point, self.from_offset, self.to_offset, kwargs = \
                generate_args_kwargs(self, (), kwargs,
                                     ["mobject_or_point", "from_offset", "to_offset"],
                                     [ORIGIN, -0.5, 0.5]
                                     )
        return self.add_points_as_subpaths(np.transpose(
            to_get_offset_lists(
                self.mobject_or_point,
                [self.from_offset, self.to_offset])
               ,(1,0,2)) )
        '''
        return [self.add_points_as_subpaths(each) for each in np.transpose(
            to_get_offset_lists(
                self.mobject_or_point,
                [self.from_offset, self.to_offset])
               ,(1,0,2)) ]
        return [self.add_points_as_subpaths(each) for each in list(zip(
            *to_get_offset_lists(
                self.mobject_or_point,
                [self.from_offset, self.to_offset])
                ))]
        '''


class GeomMark(GeomPoint):
    '''Bold Red GeomPoint'''
    CONFIG = {
        "color": RED,
        "stroke_width": 4,
    }

    def __zinit__(self, mobject_or_point, color=RED, stroke_width=4, **kwargs):
        super().__init__(self, mobject_or_point, color=color,
                         stroke_width=stroke_width, **kwargs)


class GeomPosition(GeomPoint):
    '''1e-8 GeomPoint'''
    def __init__(self, mobject_or_point=ORIGIN, **kwargs):
        GeomPoint.__init__(self, mobject_or_point, 1e-8, 1e-8, **kwargs)


class GeomLine(Line):
    '''
    xx length,     [point]
    [point],    [point] -->default
    [point],    (displacement)
    [point],    slope,              length
    [point],    [directioncosine],  length
    [point],    (directionvector),  length
    '''
    CONFIG = {
        "buff": 0,
        "path_arc": None,
    }

    def __init__(self, *args, **kwargs):
        self.normal_vector = OUT
        digest_config(self, kwargs)
        self.start = LEFT
        self.end = RIGHT
        args = list(args)
        for i in range(len(args)):
            if isinstance(args[i], (Mobject, VMobject)):
                args[i] = list(args[i].get_center())
        if len(args) == 2:
            try:
                isinstance(args[0], (list))
            except:
                try:
                    isinstance(args[0], (int, float))
                except:
                    raise Exception("Not Supported")

            else:
                try:
                    isinstance(args[1], (list, tuple))
                except:
                    raise Exception(
                        "not form of two points or point displacement")
                else:
                    if isinstance(args[1], (list,np.ndarray)):
                        self.start, self.end = args
                        
                    if isinstance(args[1], (tuple)):
                        self.start, self.end = args[0], np.sum(
                            args, 0)
        elif len(args) == 3:
            try:
                isinstance(args[0], (list))
            except:
                raise Exception("args[0]!=point")
            else:
                try:
                    isinstance(args[1], (int, float, list, tuple)) and isinstance(
                        args[2], (int, float))
                except:
                    raise Exception(
                        "not form of point slope length or point direction length")
                else:
                    if (isinstance(args[1], (int, float)) and isinstance(args[2], (int, float))):
                        hypotenuse = (1.+args[1]**2.)**0.5

                        self.start, self.end = args[0], args[0]+args[2]*np.array(
                            [1/hypotenuse, args[1]/hypotenuse, 0])

                    if isinstance(args[1], (list)):
                        direction = 1
                        for each in args[1]:
                            direction -= each**2
                        direction = args[1]+[0, direction, 0][len(args[1]):]
                        self.start, self.end = args[0], args[0] + \
                            args[2]*np.array(direction)
                    if isinstance(args[1], (tuple)):
                        self.start, self.end = args[0], args[0] + \
                            np.multiply(args[1], args[2]/get_norm(args[1]))
        Line.__init__(self, self.start, self.end, **kwargs)


class GeomPolyline(Polygon):
    CONFIG = {
        "color": WHITE,
        "mark_paths_closed": False,
        "close_new_points": False,
    }

    def __init__(self, *vertices, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.set_points_as_corners(
            [*vertices]
        )


class zGeomCurves(TipableVMobject):
    CONFIG = {
        "color": WHITE,
        "mark_paths_closed": False,
        "close_new_points": False,
    }

    def __init__(self, *verticepairs, **kwargs):
        VMobject.__init__(self, **kwargs)
        for each in verticepairs:
            n = len(each)
            if isinstance(each, VMobject):
                self.append_vectorized_mobject(each)
            elif n == 1:
                if len(self.points) == 0:
                    self.start_new_path(each)
                else:
                    self.add_line_to(point, **kwargs)
            elif n == 2:
                self.append_vectorized_mobject(Line(*each, **kwargs))
            elif n == 3:
                self.add_cubic_bezier_curve_to(*each, **kwargs)
            elif n == 4:
                self.add_cubic_bezier_curve(*each, **kwargs)
            elif n % 4 == 0:
                self.append_points(*each, **kwargs)


class GeomPolygon(Polygon):
    CONFIG = {
        "color": BLUE,
    }

    def __init__(self, *vertices, **kwargs):

        self.mobject_or_point = None
        VMobject.__init__(self, **kwargs)
        self.set_points_as_corners(
            [*vertices, vertices[0]]
        )
        if self.mobject_or_point != None:
            self.move_to(Location(self.mobject_or_point))


class GeomRegularPolygon(GeomPolygon):
    '''
    {number},start_angle,radius,[center],"point/edge",[normal_vector]
    '''
    CONFIG = {
        "start_angle": None,
    }

    def __init__(self, n=6, *args, **kwargs):
        self.args_name = \
            ["mobject_or_point", "radius", "start_angle", "element", "normal_vector"]
        self.args = \
            [ORIGIN, 1, None, "point", "OUT"]
        self.mobject_or_point, self.radius, self.start_angle, self.element, self.normal_vector = \
            generate_args(self, args, self.args)
        kwargs = merge_config_kwargs(self, kwargs, self.args_name)

        self.mobject_or_point = Location(self.mobject_or_point)
        if self.element == "point":
            if self.start_angle is None:
                if n % 2 == 0:
                    self.start_angle = 0
                else:
                    self.start_angle = 90 * DEGREES
            start_vect = rotate_vector(self.radius*RIGHT, self.start_angle)
        vertices = np.add(compass_directions(n, start_vect),
                          np.repeat([self.mobject_or_point], n, axis=0))
        GeomPolygon.__init__(self, *vertices, **kwargs)


class GeomTriangle(GeomRegularPolygon):
    def __init__(self, **kwargs):
        GeomRegularPolygon.__init__(self, n=3, **kwargs)


class GeomArrowTip(GeomPolyline):
    CONFIG = {
        "fill_opacity": 1,
        "stroke_width": 0,
        "length": DEFAULT_ARROW_TIP_LENGTH,
        "width":None,
        "start_angle": PI,
    }

    def __init__(self, **kwargs):
        GeomPolyline.__init__(self, ORIGIN, DOWN,LEFT,UP,ORIGIN, **kwargs)
        self.set_width(self.length)
        self.set_height((self.width or self.length), stretch=True)

    def get_base(self):
        return self.point_from_proportion(0.5)

    def get_tip_point(self):
        return self.points[0]

    def get_vector(self):
        return self.get_tip_point() - self.get_base()

    def get_angle(self):
        return angle_of_vector(self.get_vector())

    def get_length(self):
        return get_norm(self.get_vector())


class GeomRectangle(GeomPolygon):
    '''
    {height,width},[center],start_angle,"edge/point",[normal_vector]
    '''
    CONFIG = {
        "color": WHITE,
        "mark_paths_closed": True,
        "close_new_points": True,
    }

    def __init__(self, *args, **kwargs):
        self.args_name = \
            ["height", "width", "mobject_or_point",
                "start_angle", "element", "normal_vector"]
        self.args = \
            [2, 4, ORIGIN, None, "edge", "IN"]
        [self.height, self.width, self.mobject_or_point, self.start_angle, self.element, self.normal_vector] = \
            generate_args(self, args, self.args)
        kwargs = merge_config_kwargs(self, kwargs, self.args_name)
        self.mobject_or_point = Location(self.mobject_or_point)
        ul, ur, dr, dl = np.add(np.multiply(
            (UL, UR, DR, DL), [self.width/2, self.height/2, 0]), self.mobject_or_point)
        GeomPolygon.__init__(self, ul, ur, dr, dl, **kwargs)


class GeomSquare(GeomRectangle):
    '''
    {side_length},[center],start_angle,"edge/point",[normal_vector]
    '''

    def __init__(self, *args, **kwargs):
        self.args_name = \
            ["side_length", "mobject_or_point",
                "start_angle", "element", "normal_vector"]
        self.args = \
            [2, ORIGIN,  None, "edge", "IN"]
        [self.side_length, self.mobject_or_point, self.start_angle, self.element, self.normal_vector] = \
            generate_args(self, args, self.args)
        kwargs = merge_config_kwargs(self, kwargs, self.args_name)

        GeomRectangle.__init__(
            self,
            self.side_length,
            self.side_length,
            *args[1:],
            **kwargs
        )


class GeomElbow(VMobject):
    CONFIG = {
        "width": 0.2,
        "angle": 0,
    }

    def __init__(self, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.set_points_as_corners([UP, UP + RIGHT, RIGHT])
        self.set_width(self.width, about_point=ORIGIN)
        self.rotate(self.angle, about_point=ORIGIN)


class GeomArrow(GeomLine):
    CONFIG = {
        "stroke_width": 6,
        "buff": 0,
        "max_tip_length_to_length_ratio": 0.25,
        "max_stroke_width_to_length_ratio": 5,
        "preserve_tip_size_when_scaling": True,
    }

    def __init__(self, *args, **kwargs):
        GeomLine.__init__(self, *args, **kwargs)
        self.max_tip_length_to_length_ratio = vars(
            self)['max_tip_length_to_length_ratio']
        self.tip_length = vars(self)['tip_length']
        self.max_stroke_width_to_length_ratio = vars(
            self)['max_stroke_width_to_length_ratio']
        # TODO, should this be affected when
        # Arrow.set_stroke is called?
        self.initial_stroke_width = self.stroke_width
        self.add_tip(**kwargs)
        self.set_stroke_width_from_length()

    def scale(self, factor, **kwargs):
        if self.get_length() == 0:
            return self

        has_tip = self.has_tip()
        has_start_tip = self.has_start_tip()
        if has_tip or has_start_tip:
            old_tips = self.pop_tips()

        VMobject.scale(self, factor, **kwargs)
        self.set_stroke_width_from_length()

        # So horribly confusing, must redo
        if has_tip:
            self.add_tip()
            old_tips[0].points[:, :] = self.tip.points
            self.remove(self.tip)
            self.tip = old_tips[0]
            self.add(self.tip)
        if has_start_tip:
            self.add_tip(at_start=True)
            old_tips[1].points[:, :] = self.start_tip.points
            self.remove(self.start_tip)
            self.start_tip = old_tips[1]
            self.add(self.start_tip)
        return self

    def get_normal_vector(self):
        p0, p1, p2 = self.tip.get_start_anchors()[:3]
        return normalize(np.cross(p2 - p1, p1 - p0))

    def reset_normal_vector(self):
        self.normal_vector = self.get_normal_vector()
        return self

    def get_default_tip_length(self):
        max_ratio = self.max_tip_length_to_length_ratio
        return min(
            self.tip_length,
            max_ratio * self.get_length(),
        )

    def set_stroke_width_from_length(self):
        max_ratio = self.max_stroke_width_to_length_ratio
        self.set_stroke(
            width=min(
                self.initial_stroke_width,
                max_ratio * self.get_length(),
            ),
            family=False,
        )
        return self

    # TODO, should this be the default for everything?
    def copy(self):
        return self.deepcopy()


class GeomArc(VMobject):
    '''start_angle=0, angle=TAU / 4, arc_center=None, ccw=1, quad=1, **kwargs\n
    Parameter: start_angle; angle, arc_center\n
    VMobject, VMobject, None-->arc_center=intersection
    VMobject; angle, (int, float)-->arc_center=start_angle.point_from_proportion
    start_angle; angle, arc_center-->arc_center
    -'''
    CONFIG = {
        "radius": 1.0,
        "num_components": 9,
        "anchors_span_full_range": True,
        #"arc_center": ORIGIN,
    }
    def __init__(self, start_angle=0, angle=TAU / 4, arc_center=None, quad=1,ccw=1,  **kwargs):
        digest_config(self, kwargs)
        self.init_parameters(start_angle=start_angle, angle=angle, arc_center=arc_center, quad=quad, ccw=ccw, **kwargs)
        VMobject.__init__(self, **kwargs)

    def init_parameters(self,start_angle, angle, arc_center, quad, ccw, **kwargs):
        if arc_center is None:
            if isinstance(start_angle, VMobject) and isinstance(angle, VMobject):
                self.tmp_center = line_intersection([start_angle.pts(0), start_angle.pts(-1)], [angle.pts(0), angle.pts(-1)])
            else:
                self.tmp_center = ORIGIN
        elif isinstance(arc_center, (int, float)):
            if isinstance(start_angle, VMobject):
                self.tmp_center = start_angle.point_from_proportion(arc_center)
            else:
                raise Exception(
                    "Invalid arc_center"
                )           
        else:
            self.tmp_center=arc_center
        if isinstance(start_angle, (VMobject)):
            start_angle = start_angle.get_direction()
            if quad==2 or quad==3:
                start_angle = (PI+start_angle)%TAU
        if isinstance(angle, (VMobject)):
            angle = angle.get_direction()
            if quad==3 or quad==4:
                angle = (PI+angle)%TAU
            if angle <= start_angle:
                angle = TAU+angle
            angle = angle-start_angle
        if not ccw:
            angle = -angle
        self.start_angle = start_angle
        self.angle = angle

    def generate_points(self):
        self.init_pre_positioned_points().scale(self.radius, about_point=ORIGIN).shift(self.tmp_center)
        return self

    def init_pre_positioned_points(self):
        '''points of 2D arc with unit radius and center at ORIGIN'''
        self.set_points(self.theta_pts(self.start_angle,self.angle,self.num_components))
        return self

    def zget_arc_center(self):
        """
        Looks at the normals to the first two
        anchors, and finds their intersection points
        """
        # First two anchors and handles
        a1, h1, h2, a2 = self.points[:4]
        # Tangent vectors
        t1 = h1 - a1
        t2 = h2 - a2
        # Normals
        n1 = rotate_vector(t1, TAU / 4)
        n2 = rotate_vector(t2, TAU / 4)
        try:
            return line_intersection(
                line1=(a1, a1 + n1),
                line2=(a2, a2 + n2),
            )
        except Exception:
            warnings.warn("Can't find Arc center, using ORIGIN instead")
            return np.array(ORIGIN)

    def move_arc_center_to(self, point):
        self.shift(point - self.get_arc_center())
        return self

    def stop_angle(self):
        return angle_of_vector(
            self.points[-1] - self.get_arc_center()
        ) % TAU



class GeomCircle(Circle):
    pass


class GeomSemiCircle(VMobject):
    def __init__(self, radius=1, **kwargs):
        super().__init__(**kwargs)
        self.append_vectorized_mobject(Line())
        self.append_vectorized_mobject(Arc(angle=PI))
        self.scale(radius)


class GeomEllipse(Ellipse):
    pass


class DimAngle(VMobject):
    '''A dimentional angle symbol
    {v1;angle=PI/4}-->default
    [v1;angle vector]
    [v1;start vector], [v2:end vector]
    {start;angle of start vector:None>start vector; num>angle=0-->default }'''
    CONFIG = {
        "width": 0.35,
        "theta": PI/4
    }

    def __init__(self, v1=None, v2=None, start=0, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.set_points_as_corners([RIGHT, ORIGIN,  self.get_point(v1, v2)])
        self.set_width(self.width, about_point=ORIGIN)
        if start is None and v2 is not None:
            self.rotate(angle_of_vector(v1), about_point=ORIGIN)
        elif start!=0:
            self.rotate(start, about_point=ORIGIN)
        
    def get_point(self, v1, v2):
        if v1 is not None and v2 is None:
            if isinstance(v1, (int, float)):
                self.theta = v1
            elif isinstance(v1, (list)):
                self.theta = angle_of_vector(v1)
        elif v1 is not None and v2 is not None:
            self.theta = spaceangle_between(v1, v2)
        return [np.cos(self.theta), np.sin(self.theta), 0]

    def get_theta(self):
        return self.theta

    def ratio(self, p=TAU):
        return self.theta/p

    def ratio_r(self, p=TAU):
        return (p-self.theta)/p


class DimRadian(DimAngle):
    '''A 1e-8 DimAngle'''
    CONFIG = {
        "width": 1e-8,
    }


class DimArc(GeomArc):
    CONFIG = {
        "color": GOLD,
        "stroke_color": GOLD,
        "stroke_opacity": 0.8,
        "stroke_width": 4,#DEFAULT_STROKE_WIDTH,
        "radius":0.25,
    }

    def __init__(self, start_angle=0, angle=TAU/4, arc_center=None, radius=None, color=None,tip_length=None, tip_start=True, tip_end=True, quad=1, ccw=1, **kwargs):
        digest_config(self, kwargs)
        GeomArc.__init__(self,  start_angle=start_angle, angle=angle, arc_center=arc_center, radius=radius or self.radius,tip_length=tip_length, tip_start=tip_start, tip_end= tip_end, quad=quad, ccw=ccw,**kwargs)
        arc_length=self.radius*self.angle
        tip_length=tip_length or min(0.1,max(0.06,0.1*arc_length))
        tip = GeomArrowTip(length=tip_length,width=self.stroke_width/100*3)
        if self.angle != 0:
            ratio = tip_length/arc_length
        else:
            ratio = tip_length/(radius*(self.start_angle))
        if tip_start:
            tips = tip.copy().move_to(self.point_from_proportion(0)
                                      ).shift([tip.get_width()/2, 0, 0])
            angle = angle_of_vector(self.point_from_proportion(
                ratio)-self.point_from_proportion(0))
            self.add(tips.rotate(angle, about_point=self.point_from_proportion(0)))
        if tip_end:
            tips = tip.copy().move_to(self.point_from_proportion(1)
                                      ).shift([tip.get_width()/2, 0, 0])
            angle = angle_of_vector(self.point_from_proportion(
                1-ratio)-self.point_from_proportion(1))
            self.add(tips.rotate(angle, about_point=self.point_from_proportion(1)))
        self.set_color(color or self.color)
        #self.shift(self.arc_center)

    def add_tip():
        pass
        

class zDimArc(Arc):
    CONFIG = {
        "stroke_color": BLUE,
        # "stroke_opacity": 1.0,
        # "stroke_width": DEFAULT_STROKE_WIDTH,
        "radius":0.4,
        #"dimhash": GeomArc,
    }
    def __init__(self, start_angle=0, angle=TAU/4, arc_center=None, ccw=1, color=GRAY, tip_length=0.1, tip_start=True, tip_end=True, reverse=False, reverse2=False, stroke_width=4, *args, **kwargs):
        # arc_center=ORIGIN
        Arc.__init__(self, **kwargs)
        tip = ArrowTip(length=tip_length,stroke_color=color)
        if angle != 0:
            ratio = tip_length/(self.radius*(angle))
        else:
            ratio = tip_length/(self.radius*(start_angle))
        if tip_start:
            tips = tip.copy().move_to(self.point_from_proportion(0)
                                      ).shift([tip.get_width()/2, 0, 0])
            angle = angle_of_vector(self.point_from_proportion(
                ratio)-self.point_from_proportion(0))
            self.add(tips.rotate(angle, about_point=self.point_from_proportion(0)))
        if tip_end:
            tips = tip.copy().move_to(self.point_from_proportion(1)
                                      ).shift([tip.get_width()/2, 0, 0])
            angle = angle_of_vector(self.point_from_proportion(
                1-ratio)-self.point_from_proportion(1))
            self.add(tips.rotate(angle, about_point=self.point_from_proportion(1)))
        #self.set_color(color).copy()
        

class DimHashArc(VMobject):
    CONFIG = {
        "color": GOLD,
        "stroke_color": GOLD,
        "stroke_opacity": 0.8,
        "stroke_width": 4,#DEFAULT_STROKE_WIDTH,
        "radius":0.25,
        "dimhash": GeomArc,
    }
    def __init__(self, start_angle=0, angle=TAU/4, arc_center=None, radius=0.25, count=1, space=0.1, quad=1, ccw=1,  *args, **kwargs):
        VMobject.__init__(self, **kwargs)
        hash = VMobject()
        for i in range(count):
            hash.append_vectorized_mobject(GeomArc(start_angle=start_angle, angle=angle, arc_center=arc_center, radius=self.radius+i*space,  quad=quad,ccw=ccw,  *args, **kwargs))
        self.append_vectorized_mobject(hash)
        #self.set_stroke(self.stroke_color,self.stroke_width,self.stroke_opacity)



class DimHashElbow(VGroup):
    '''line, line_or_ratio=0, width=0.2, ccw=1, stroke_color=GRAY, reverse=False, *args, **kwargs
    '''

    def __init__(self, line, line_or_ratio=0, width=0.2, ccw=1, stroke_color=GRAY, reverse=False, *args, **kwargs):
        VGroup.__init__(self, **kwargs)
        if not isinstance(line, VGroup):
            angle = -ccw*PI/2
            if reverse:
                width = -width
            if isinstance(line_or_ratio, (int, float)):
                pt0 = line.point_from_proportion(line_or_ratio)
            elif isinstance(line_or_ratio, (Mobject)):
                pt0 = line_intersection(line, line_or_ratio)
            else:
                pt0 = line_or_ratio
            self.add(SymElbow(line.get_line(1, pt0),
                              width, ccw).set_color(stroke_color))


class SymElbow(VMobject):
    '''line, width, ccw=1, angle=PI/2, **kwargs\n
    ccw=1=counterclockwise
    -'''

    def __init__(self, line, width, ccw=1, angle=PI/2, **kwargs):
        VMobject.__init__(self, **kwargs)
        if int(ccw) >= 1:
            ccw = 1
        else:
            ccw = 0
        angle = (-1)**ccw*angle
        line = line.get_line(width, 0)
        hash = line.rotate(angle, about_point=line.pts(-1)).reverse_points()
        hash.append_vectorized_mobject(hash.copy().rotate(
            angle, about_point=hash.pts(-1)).reverse_points())
        self.append_vectorized_mobject(hash)


class SymHash(VMobject):
    '''line, length, **kwargs\n
    
    -'''

    def __init__(self, line, length, **kwargs):
        VMobject.__init__(self, **kwargs)
        hash = line.get_line(length).rotate(PI/2)
        self.append_vectorized_mobject(hash)


class SymHashV(VMobject):
    def __init__(self, line, length, FW=1, angle=PI/4, **kwargs):
        VMobject.__init__(self, **kwargs)
        line = line.get_line(length/2/np.sin(angle))
        pt = line.pts(-1)
        hash = line.copy().rotate(angle, about_point=pt)
        hash.append_vectorized_mobject(
            line.copy().rotate(-angle, about_point=pt).reverse_points())
        self.append_vectorized_mobject(hash)


class Hash(VMobject):
    '''     '''
    CONFIG = {
        "stroke_color": GOLD,
        "stroke_opacity": 0.8,
        "stroke_width": 4,
        "dimhash": SymHash,
    }

    def __init__(self, line, count=1, posratio=0.5, length=0.3, space=0.1, **kwargs):
        VMobject.__init__(self, **kwargs)
        if not isinstance(line, VGroup):
            if line.get_length() <= length*5:
                length = min(max(0.15, line.get_length()/5), 0.3)
            hash = self.dimhash(line, length)
            hashmark = VMobject()
            for i in range(count):
                hashmark.append_vectorized_mobject(hash.copy().move_to(
                    i*space*line.get_unit_vector()
                ))
            self.append_vectorized_mobject(hashmark.move_to(
                line.point_from_proportion(posratio)))
        else:
            kwargs["dimhash"] = self.dimhash
            self.add(Hashs(line, count=count, posratio=posratio,
                           length=length, space=space, **kwargs))


class Hashs(VGroup):
    CONFIG = {
        "dimhash": SymHash,
    }

    def __init__(self, mobject, count=1, posratio=0.5, width=4, length=0.3, color=GOLD, opacity=1, space=0.07, *args, **kwargs):
        VGroup.__init__(self, **kwargs)
        if isinstance(mobject, VGroup):
            numofcurves = len(mobject.submobjects)

            def func(i):
                return mobject.submobjects[i]
        else:
            numofcurves = mobject.get_num_curves()

            def func(i):
                return CurveLine(mobject, i)
        if isinstance(count, int):
            def number(i):
                return count
        elif callable(count):
            def number(i):
                return count(i)+1
        kwargs["dimhash"] = self.dimhash
        [self.add(Hash(func(i), number(i), posratio=posratio, length=length,
                       space=space,  *args, **kwargs)) for i in range(numofcurves)]


class HashV(Hash):
    CONFIG = {
        "dimhash": SymHashV,
    }


class HashVs(Hashs):
    CONFIG = {
        "dimhash": SymHashV,
    }
