# painter class 

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ..IO.representation import *
import ode
import math

example, inputs = ("M[" +
        "J[R, color[Green], P[0.0, 0.0], L[ground, link_1]], " +
        "J[R, color[Green], P[12.92, 32.53], L[link_1, link_2]], " +
        "J[R, color[Green], P[73.28, 67.97], L[link_2, link_3]], " +
        "J[R, color[Green], P[33.3, 66.95], L[link_2]], " +
        "J[R, color[Green], P[90.0, 0.0], L[ground, link_3]]" +
        "]", {0: ('ground', 'link_1')})

class CanvasPaint(QWidget):
    """
    world = ode.World()
    world.setGravity((0,-9.81,0))

    
    # Create two bodies
    body1 = ode.Body(world)
    M = ode.Mass()
    M.setSphere(2500, 0.05)
    body1.setMass(M)
    body1.setPosition((1,2,0))

    body2 = ode.Body(world)
    M = ode.Mass()
    M.setSphere(2500, 0.05)
    body2.setMass(M)
    body2.setPosition((2,2,0))

    # Connect body1 with the static environment
    j1 = ode.HingeJoint(world)
    j1.attach(body1, ode.environment)
    j1.setAnchor( (0,2,0) )
    j1.setAxis( (0,0,1) )
    j1.setParam(ode.ParamFMax, 22)
    j1.setParam(ode.ParamVel, 0)
    
    
    # Connect body2 with body1

    j2 = ode.BallJoint(world)
    j2.attach(body1, body2)
    j2.setAnchor( (1,2,0) )
    """
    
    fps = 50
    dt = 0.01
    
    def __init__(self, parent = None):
        super(CanvasPaint, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.zoom = 1
        self.loopFlag = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.timeout.connect(lambda: self.world.step(self.dt)) #sec
    
    def test(self):
        
        self.world = ode.World()
        self.world.setGravity((0,-9.81,0))
        vpoints = parse_vpoints(example)
        
        self.vlinks = {}
        for i, vpoint in enumerate(vpoints):
            for link in vpoint.links:
                if link in self.vlinks:
                    self.vlinks[link].add(i)
                else:
                    self.vlinks[link] = {i}
        print(self.vlinks)
        self.bodies = []
    
        for i, vpoint in enumerate(vpoints):
            body = ode.Body(self.world)
            M = ode.Mass()
            M.setSphere(250, 0.05)
            body.setMass(M)
            x, y = vpoint
            body.setPosition((x, y, 0))
            self.bodies.append(body)
        
        self.bodies[0].setGravityMode(False)
        
        joints = []
        for name, vlink in self.vlinks.items():
            link = list(vlink)
            print(link)
            if name == 'ground':
                for p in link:
                    if p in inputs:
                        print("input:", p)
                        j = ode.HingeJoint(self.world)
                        #j.attach(bodies[(vlinks[inputs[p][1]] - {p}).pop()], ode.environment)
                        j.attach(self.bodies[1], ode.environment)
                        j.setAxis((0, 0, 1))
                        j.setAnchor(self.bodies[0].getPosition())
                        j.setParam(ode.ParamVel, 2)
                        j.setParam(ode.ParamFMax, 22000)
                    else:
                        print("grounded:", p)
                        j = ode.BallJoint(self.world)
                        j.attach(self.bodies[p], ode.environment)
                        j.setAnchor(self.bodies[p].getPosition())
                    joints.append(j)
            elif len(link) >= 2:
                print("link:", link[0], link[1])
                j = ode.BallJoint(self.world)
                j.attach(self.bodies[link[0]], self.bodies[link[1]])
                j.setAnchor(self.bodies[link[0]].getPosition())
                joints.append(j)
                # TODO : need to add select method in this joint type
                for p in link[2:]:
                    print("other:", p, link[0], link[1])
                    for k in range(2):
                        j = ode.BallJoint(self.world)
                        j.attach(self.bodies[p], self.bodies[link[k]])
                    joints.append(j)
    
    def setTimer(self, flag, checkmode):
        if flag:
            self.timer.start(self.dt*1000) # msec
        else:
            self.timer.stop()
    
    @pyqtSlot(int)
    def setMotor(self, vel: int):
        self.j1.setParam(ode.ParamVel, vel)
    
    def coord(self, c):
        print(c[0], c[1])
        return c[0], c[1]
    
    def paintEvent(self, event):
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.fillRect(event.rect(), QBrush(Qt.white))
        self.painter.translate(self.width()/2, self.height()/2)
        pen = QPen(Qt.black)
        pen.setWidth(3)
        
        def draw(c1, c2):
            self.painter.setPen(pen)
            self.painter.drawLine(QPointF(c1[0], -c1[2])*self.zoom, QPointF(c2[0], -c2[1])*self.zoom)
            print(c1, c2)
            self.painter.end()
            
        for name, vlink in self.vlinks.items():
            if name == 'ground':
                continue
            pos = [self.bodies[n].getPosition() for n in vlink]
            for n in range(0, len(pos)):
                draw(pos[n-1], pos[n])
        """
        x1,y1,z1 = self.body1.getPosition()
        angle = self.j1.getAngle()
        x2,y2,z2 = self.body2.getPosition()
        
        self.painter.setPen(pen)
        self.painter.drawLine(QPointF(0, -2)*self.zoom, QPointF(x1, -y1)*self.zoom)
        self.painter.drawLine(QPointF(x1, -y1)*self.zoom, QPointF(x2, -y2)*self.zoom)
        self.painter.end()
        """
    
