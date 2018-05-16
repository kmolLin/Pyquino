# painter class 

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import ode
import math


class CanvasPaint(QWidget):
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

    fps = 50
    dt = 0.01
    
    def __init__(self, parent = None):
        super(CanvasPaint, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.zoom = 100
        self.loopFlag = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.timeout.connect(lambda: self.world.step(self.dt)) #sec
    
    def setTimer(self, flag, checkmode):
        if flag:
            self.timer.start(self.dt*1000) # msec
        else:
            self.timer.stop()
    
    @pyqtSlot(int)
    def setMotor(self, vel: int):
        self.j1.setParam(ode.ParamVel, vel)
    
    def paintEvent(self, event):
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.fillRect(event.rect(), QBrush(Qt.white))
        self.painter.translate(self.width()/2, self.height()/2)
        x1,y1,z1 = self.body1.getPosition()
        angle = self.j1.getAngle()
        self.painter.drawText(self.width()/2, self.height()/2, str(math.degrees(angle)))
        x2,y2,z2 = self.body2.getPosition()
        pen = QPen(Qt.black)
        pen.setWidth(3)
        self.painter.setPen(pen)
        self.painter.drawLine(QPointF(0, -2)*self.zoom, QPointF(x1, -y1)*self.zoom)
        self.painter.drawLine(QPointF(x1, -y1)*self.zoom, QPointF(x2, -y2)*self.zoom)
        self.painter.end()

    
