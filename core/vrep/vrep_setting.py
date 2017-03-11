# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, math, time
from .Ui_vrep_setting import Ui_Dialog
from ..vrep_remoAPI import vrep
from ..gcode.gcodeParser import *

class vrepsetting(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(vrepsetting, self).__init__(parent)
        self.setupUi(self)
        self.initForms()
        # child threaded script: 
        # 內建使用 port 19997 若要加入其他 port, 在  serve 端程式納入
        #simExtRemoteApiStart(19999)
    
    def initForms(self): self.openGcodeFile.clicked.connect(self.__open_file__)
    
    def __open_file__(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Files", '..', 'GCode(*.gcode)')
        if filename:
            
            #path = 'test_gcode.gcode'
            parser = GcodeParser()
            self.model = parser.parseFile(filename)
            print ("Done! %s"%self.model)
            
            self.renderVertices()
            get = []
            for i in range(len(self.layer_vertices)):
                x, y, z = self.parsePostion(i)
                get = str(x),str(y), str(z)
                self.gcodeList.addItem(str(get) )
                print(x, y, z)
        else:
            print("No file")
        
    def renderVertices(self):
        t1 = time.time()
        self.layer_vertices = list()
        for layer in self.model.layers:
            x = layer.start["X"]
            y = layer.start["Y"]
            z = layer.start["Z"]
            for seg in layer.segments:
                #print(seg)
                self.layer_vertices.append([x, y, z])
                seg_x = seg.coords["X"]
                seg_y = seg.coords["Y"]
                seg_z = seg.coords["Z"]
                self.layer_vertices.append([seg_x, seg_y, seg_z])
        print(self.layer_vertices)
    
    def parsePostion(self, pos):
        row = self.layer_vertices[pos]
        return row[0], row[1], row[2]
    
    @pyqtSlot()
    def on_xAxisleft_clicked(self):
        vrep.simxFinish(-1)         
        clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
        deg = math.pi/180
        if clientID!=-1: print("Connected to remote server")
        else:
            print('Connection not successful')
            sys.exit('Could not connect')
        
        errorCode, Revolute_joint_handle = vrep.simxGetObjectHandle(clientID, 'Revolute_joint', vrep.simx_opmode_oneshot_wait)
        
        if errorCode==-1:
            print('Can not find left or right motor')
            sys.exit()
        
        setJointPosition(10, 72)
        print("test")
        def setJointPosition(incAngle, steps):
            for i  in range(steps): errorCode = vrep.simxSetJointPosition(clientID, Revolute_joint_handle, i*incAngle*deg, vrep.simx_opmode_oneshot_wait)
