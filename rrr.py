import pygame
from pygame.locals import *
import ode
from lark import Lark, Transformer
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from typing import List, Union
import numpy as np

_color_list = {
    'Red': QColor(172, 68, 68),
    'Green': QColor(110, 190, 30),
    'Blue': QColor(68, 120, 172),
    'Cyan': Qt.cyan,
    'Magenta': Qt.magenta,
    'Brick-Red': QColor(255, 130, 130),
    'Yellow': Qt.yellow,
    'Gray': Qt.gray,
    'Orange': QColor(225, 165, 0),
    'Pink': QColor(225, 192, 230),
    'Black': Qt.black,
    'White': Qt.white,
    'Dark-Red': Qt.darkRed,
    'Dark-Green': Qt.darkGreen,
    'Dark-Blue': Qt.darkBlue,
    'Dark-Cyan': Qt.darkCyan,
    'Dark-Magenta': Qt.darkMagenta,
    'Dark-Yellow': Qt.darkYellow,
    'Dark-Gray': Qt.darkGray,
    'Dark-Orange': QColor(225, 140, 0),
    'Dark-Pink': QColor(225, 20, 147),
}

colorNames = tuple(sorted(_color_list.keys()))
_colors = "|".join('"{}"'.format(color) for color in reversed(colorNames))

_pmks_grammar = Lark(
    #Number
    """
    DIGIT: "0".."9"
    INT: DIGIT+
    SIGNED_INT: ["+"|"-"] INT
    DECIMAL: INT "." INT? | "." INT
    _EXP: ("e"|"E") SIGNED_INT
    FLOAT: INT _EXP | DECIMAL _EXP?
    NUMBER: FLOAT | INT
    """
    #Letters
    """
    LCASE_LETTER: "a".."z"
    UCASE_LETTER: "A".."Z"
    LETTER: UCASE_LETTER | LCASE_LETTER
    CNAME: ("_"|LETTER) ("_"|LETTER|DIGIT)*
    """
    #White space and new line.
    """
    WS: /[ \\t\\f\\r\\n]/+
    CR : /\\r/
    LF : /\\n/
    NEWLINE: (CR? LF)+
    """
    #Main document.
    """
    type: JOINTTYPE+
    name: CNAME
    num : NUMBER  -> number
        | "-" num -> neg
    
    joint    : "J[" type ("," angle)? ("," color)? "," point "," link "]"
    link     : "L[" name ("," name)* "]"
    point    : "P[" num  "," num "]"
    angle    : "A[" num "]"
    colorv   : INT
    color    : "color[" (("(" colorv "," colorv "," colorv ")") | COLOR+) "]"
    mechanism: "M[" [joint ("," joint)* (",")?] "]"
    
    JOINTTYPE: "RP" | "R" | "P"
    COLOR    : """ + _colors + """
    
    %ignore WS
    %ignore NEWLINE
    COMMENT: "#" /[^\\n]/*
    %ignore COMMENT
    """, start = 'mechanism'
)

class VPoint():
    def __init__(self, links, type_int, angle, color_str, x, y):
        tmp_list = []
        links = links.replace(" ", '')
        for name in links.split(','):
            if not name:
                continue
            tmp_list.append(name)
        self.links = tuple(tmp_list)
        self.type = type_int
        self.typeSTR = ('R', 'P', 'RP')[type_int]
        self.angle = angle
        self.colorSTR = color_str
        self.x = x
        self.y = y
        self.c = np.ndarray(2, dtype=np.object)
        if (self.type == 1) or (self.type == 2):
            """Slider current coordinates.
            
            + [0]: Current node on slot.
            + [1]: Pin.
            """
            self.c[0] = (self.x, self.y)
            self.c[1] = (self.x, self.y)
        else:
            self.c[0] = (self.x, self.y)
            
    def grounded(self):
        """Return True if the joint is connect with the ground."""
        return 'ground' in self.links    
    
    @property
    def cx(self):
        """X value of frist current coordinate."""
        return self.c[0][0]
    
    @property
    def cy(self):
        """Y value of frist current coordinate."""
        return self.c[0][1]
        
    def __repr__(self):
        """Use to generate script."""
        return "VPoint({p.links}, {p.type}, {p.angle}, {p.c})".format(p=self)
    
    def __getitem__(self, i: int):
        """Get coordinate like this:
        
        x, y = VPoint(10, 20)
        """
        if self.type == 0:
            return self.c[0][i]
        else:
            return self.c[1][i]


class _PMKSParams(Transformer):
    
    """Usage: tree = parser.parse(expr)
    
    args = transformer().transform(tree)
    args: Dict[str, value]
    """
    
    name = lambda self, n: str(n[0])
    type = lambda self, n: ('R', 'P', 'RP').index(str(n[0]))
    color = lambda self, n: str(n[0]) if (len(n) == 1) else str(tuple(n))
    colorv = lambda self, n: int(n[0])
    neg = lambda self, n: -n[0]
    number = lambda self, n: float(n[0])
    point = lambda self, c: tuple(c)
    angle = number
    link = lambda self, a: tuple(a)
    
    def joint(self, args) -> VPoint:
        """Same as parent."""
        hasAngle = args[0] != 0
        x, y = args[-2]
        return VPoint(
            ','.join(args[-1]),
            args[0],
            args[1] if hasAngle else 0.,
            args[2] if hasAngle else args[1],
            x,
            y
        )
    
    mechanism = lambda self, j: j


def parse_vpoints(expr: str) -> List[List[Union[str, float]]]:
    """Using to parse the expression and return arguments."""
    return _PMKSParams().transform(_pmks_grammar.parse(expr))

if __name__ == '__main__':
    
    example, inputs = ("M[" +
        "J[R, color[Green], P[0.0, 0.0], L[ground, link_1]], " +
        "J[R, color[Green], P[12.92, 32.53], L[link_1, link_2]], " +
        "J[R, color[Green], P[33.3, 66.95], L[link_2]], " +
        "J[R, color[Green], P[73.28, 67.97], L[link_2, link_3]], " +
        "J[R, color[Green], P[90.0, 0.0], L[ground, link_3]]" +
        "]", {0: ('ground', 'link_1')})
    """
    example, inputs = ("M[" +
        "J[R, color[Green], P[0.0, 0.0], L[ground, link_1]], " +
        "J[R, color[Green], P[9.61, 11.52], L[link_1, link_2, link_4]], " +
        "J[R, color[Blue], P[-38.0, -7.8], L[ground, link_3, link_5]], " +
        "J[R, color[Green], P[-35.24, 33.61], L[link_2, link_3]], " +
        "J[R, color[Green], P[-77.75, -2.54], L[link_3, link_6]], " +
        "J[R, color[Green], P[-20.1, -42.79], L[link_4, link_5, link_7]], " +
        "J[R, color[Green], P[-56.05, -35.42], L[link_6, link_7]], " +
        "J[R, color[Green], P[-22.22, -91.74], L[link_7]]" +
        "]", {0: ('ground', 'link_1')})
    """
    vpoints = parse_vpoints(example)
    vlinks = {}
    for i, vpoint in enumerate(vpoints):
        for link in vpoint.links:
            if link in vlinks:
                vlinks[link].add(i)
            else:
                vlinks[link] = {i}
    print(vlinks)
    
    def coord(c):
        """Convert world coordinates to pixel coordinates."""
        return 320+1*c[0], 300-1*c[1]
    
    
    # Initialize pygame
    pygame.init()
    
    # Open a display
    srf = pygame.display.set_mode((640,480))
    
    # Create a world object
    world = ode.World()
    world.setGravity((0,-9.81,0))
    
    bodies = []
    
    for i, vpoint in enumerate(vpoints):
        body = ode.Body(world)
        M = ode.Mass()
        M.setSphere(250, 0.05)
        body.setMass(M)
        x, y = vpoint
        body.setPosition((x, y, 0))
        bodies.append(body)
    
    bodies[0].setGravityMode(False)
    
    joints = []
    for name, vlink in vlinks.items():
        link = list(vlink)
        print(link)
        if name == 'ground':
            for p in link:
                if p in inputs:
                    print("input:", p)
                    j = ode.HingeJoint(world)
                    print("*"*10, vlink)
                    j.attach(bodies[(vlinks[inputs[p][1]] - {p}).pop()], ode.environment)
                    #j.attach(bodies[1], ode.environment)
                    j.setAxis((0, 0, 1))
                    j.setAnchor(bodies[p].getPosition())
                    j.setParam(ode.ParamVel, 2)
                    j.setParam(ode.ParamFMax, 22000)
                else:
                    print("grounded:", p)
                    j = ode.BallJoint(world)
                    j.attach(bodies[p], ode.environment)
                    j.setAnchor(bodies[p].getPosition())
                joints.append(j)
        elif len(link) >= 2:
            print("link:", link[0], link[1])
            j = ode.BallJoint(world)
            j.attach(bodies[link[0]], bodies[link[1]])
            j.setAnchor(bodies[link[0]].getPosition())
            joints.append(j)
            for p in link[2:]:
                print("other:", p, link[0], link[1])
                for k in range(2):
                    j = ode.BallJoint(world)
                    j.attach(bodies[p], bodies[link[k]])
                joints.append(j)
    check = []
    for i in range(len(joints)):
        print(joints[i].getAnchor())
    print(check)
    print(len(joints))
    fps = 50
    dt = 1.0/fps
    loopFlag = True
    clk = pygame.time.Clock()

    while loopFlag:
        events = pygame.event.get()
        for e in events:
            if e.type==QUIT:
                loopFlag=False
            if e.type==KEYDOWN:
                loopFlag=False

        # Clear the screen
        srf.fill((255,255,255))
        
        def draw(c1, c2):
            pygame.draw.line(srf, (55,0,200), coord(c1), coord(c2), 2)
        
        for name, vlink in vlinks.items():
            if name == 'ground':
                continue
            pos = [bodies[n].getPosition() for n in vlink]
            for n in range(0, len(pos)):
                draw(pos[n-1], pos[n])

        pygame.display.flip()

        # Next simulation step
        world.step(dt)

        # Try to keep the specified framerate    
        clk.tick(fps)

"""
def coord(x,y):
    "Convert world coordinates to pixel coordinates."
    return 320+170*x, 400-170*y


# Initialize pygame
pygame.init()

# Open a display
srf = pygame.display.set_mode((640,480))

# Create a world object
world = ode.World()
world.setGravity((0,-9.81,0))

# Create two bodies
body1 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body1.setMass(M)
body1.setPosition((0,0.3,0))

body2 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body2.setMass(M)
body2.setPosition((0.8,0.6,0))

body3 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body3.setMass(M)
body3.setPosition((1,0,0))

body4 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body4.setMass(M)
body4.setPosition((0.6,0.8,0))

# Connect body1 with the static environment
j1 = ode.HingeJoint(world)
j1.attach(body1, ode.environment)
j1.setAnchor( (0.2,0,0) )
j1.setAxis( (0,0,1) )
j1.setParam(ode.ParamVel, 2)
j1.setParam(ode.ParamFMax, 22000)

# Connect body2 with body1
j2 = ode.BallJoint(world)
j2.attach(body1, body2)
#j2.setAnchor( (0,0.2,0) )

# Connect body3 with body2
j3 = ode.BallJoint(world)
j3.attach(body2, body3)
#j3.setAnchor( (0.8,0.6,0) )

# Connect body1 with the static environment
j4 = ode.BallJoint(world)
j4.attach(body3, ode.environment)
#j4.setAnchor( (1, 0, 0) )

j5 = ode.BallJoint(world)
j5.attach(body4, body2)
#j5.setAnchor( (0, 0.2, 0) )

j6 = ode.BallJoint(world)
j6.attach(body4, body3)
j6.setAnchor( (0.8, 0.6, 0) )
# Simulation loop...


fps = 50
dt = 1.0/fps
loopFlag = True
clk = pygame.time.Clock()

while loopFlag:
    events = pygame.event.get()
    for e in events:
        if e.type==QUIT:
            loopFlag=False
        if e.type==KEYDOWN:
            loopFlag=False

    # Clear the screen
    srf.fill((255,255,255))

    # Draw the two bodies
    x1,y1,z1 = body1.getPosition()
    x2,y2,z2 = body2.getPosition()
    x3,y3,z3 = body3.getPosition()
    x4,y4,z4 = body4.getPosition()
    #pygame.draw.circle(srf, (55,0,200), coord(x1,y1), 20, 0)
    pygame.draw.line(srf, (55,0,200), coord(0.2,0), coord(x1,y1), 2)
    #pygame.draw.circle(srf, (55,0,200), coord(x2,y2), 20, 0)
    pygame.draw.line(srf, (55,0,200), coord(x1,y1), coord(x2,y2), 2)
    pygame.draw.line(srf, (55,0,200), coord(x2,y2), coord(x3,y3), 2)
    pygame.draw.line(srf, (55,0,200), coord(x1,y1), coord(x4,y4), 2)
    pygame.draw.line(srf, (55,0,200), coord(x2,y2), coord(x4,y4), 2)

    pygame.display.flip()

    # Next simulation step
    world.step(dt)

    # Try to keep the specified framerate    
    clk.tick(fps)
"""
