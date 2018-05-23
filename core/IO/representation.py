# Institutional representation
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
