# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, math, time
from .Ui_vrep_setting import Ui_Dialog
from ..vrep_remoAPI import vrep
from ..gcode.gcodeParser import *
import math
import time


la = 347
to = 30
pa = 40
sp = 235

class readingGcode(QThread):
    def __init__(self,getProgress, layers,  parent=None):
        super(readingGcode, self).__init__(parent)
        self.getProgress = getProgress
        self.layers = layers
        self.mutex = QMutex()
        self.stoped = False
    
    def run(self):
        with QMutexLocker(self.mutex): self.stoped = False
        self.getProgress.setValue(0)
        self.getProgress.setMaximum(len([e for e in self.layers[0].segments]))
        self.layer_vertices = list()
        for layer in self.layers:
            x = layer.start["X"]
            y = layer.start["Y"]
            z = layer.start["Z"]
            for seg in layer.segments:
                self.layer_vertices.append([x, y, z])
                seg_x = seg.coords["X"]
                seg_y = seg.coords["Y"]
                seg_z = seg.coords["Z"]
                self.layer_vertices.append([seg_x, seg_y, seg_z])
                self.getProgress.setValue(self.getProgress.value()+1)
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True

class vrepsetting(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(vrepsetting, self).__init__(parent)
        self.setupUi(self)
        self.initForms()
        # child threaded script: 
        # 內建使用 port 19997 若要加入其他 port, 在  serve 端程式納入
        #simExtRemoteApiStart(19999)
    
    def initForms(self): 
        self.openGcodeFile.clicked.connect(self.__open_file__)
        self.translate.clicked.connect(self.ik_transform)
    
    
    
    def ik_transform(self):
        
        tx = self.tx.value()
        ty = self.ty.value()
        tz = self.tz.value()
        
        a1x = tx+pa
        a1y = ty
        a1z = tz+to

        #pivot B
        b1x = tx+pa*math.cos(math.radians(120))
        b1y = ty +pa*math.sin(math.radians(120))
        b1z = tz+to
        ##pivotC
        c1x = tx+pa*math.cos(math.radians(240))
        c1y = ty+pa*math.sin(math.radians(240))
        c1z = tz+to
        ##carriage
        a2x = sp
        a2y = 0
        #a2z = tz+to+ha
        ##Cb
        b2x = sp*math.cos(math.radians(120))
        b2y = sp*math.sin(math.radians(120))
        ##carriage C2x = sp*cos(240)
        c2x = sp*math.cos(math.radians(240))
        c2y = sp*math.sin(math.radians(240))
        
        aa = math.sqrt((a2x-a1x)*(a2x-a1x)+(a2y-a1y)*(a2y-a1y))
        ha = math.sqrt(la*la-aa*aa)

        ab = math.sqrt((b2x-b1x)*(b2x-b1x)+(b2y-b1y)*(b2y-b1y))
        hb = math.sqrt(la*la-ab*ab)

        ac = math.sqrt((c2x-c1x)*(c2x-c1x)+(c2y-c1y)*(c2y-c1y))
        #print(ac)
        hc = math.sqrt(la*la-ac*ac)

        a2z = tz+to+ha
        b2z = tz+to+hb
        c2z = tz+to+hc
        
        print(a2z,"/n",b2z,"/n",c2z)
        self.translateShow.addItem("(X: {:.04f},Y: {:.04f},Z: {:.04f})".format(a2z, b2z, c2z))
    
    
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
                self.sendPoisiontoVrep(x, y, z)
                #print(x, y, z)
        else:
            print("No file")
            
    def sendPoisiontoVrep(self, e, r, t):
        
        vrep.simxFinish(-1)
        clientID = vrep.simxStart('127.0.0.1', 19998, True, True, 5000, 5)
        if clientID!= -1:
            #print("Connected to remote server")
            time.sleep(0.5)
            errorCode,plate=vrep.simxGetObjectHandle(clientID,'plate',vrep.simx_opmode_oneshot_wait)
        
        
            if errorCode == -1:
            #print('Can not find plate')
                sys.exit()                
            errorCode=vrep.simxSetObjectPosition(clientID,plate,-1,[e/1000,r/1000,t/1000+0.1165],vrep.simx_opmode_oneshot_wait)
        #print(e/1000,r/1000,t/1000)
        else:
            print('Connection not successful')
            sys.exit('Could not connect')
        '''
        time.sleep(0.5)
        errorCode,plate=vrep.simxGetObjectHandle(clientID,'plate',vrep.simx_opmode_streaming)
        
        
        if errorCode == -1:
            #print('Can not find plate')
            sys.exit()                
        errorCode=vrep.simxSetObjectPosition(clientID,plate,-1,[e/1000,r/1000,t/1000+0.1165], vrep.simx_opmode_streaming)
        #print(e/1000,r/1000,t/1000)
        '''
        
    def renderVertices(self):
        work = readingGcode(self.progressBar, self.model.layers)
        work.run()
        self.layer_vertices = work.layer_vertices
    
    def parsePostion(self, pos):
        row = self.layer_vertices[pos]
        return row[0], row[1], row[2]
    
    @pyqtSlot()
    def on_xAxisleft_clicked(self):
        test = []
        vrep.simxFinish(-1)         
        clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
        deg = math.pi/180
        if clientID!=-1: print("Connected to remote server")
        else:
            print('Connection not successful')
            sys.exit('Could not connect')
            
        errorCode, test = vrep.simxGetObjectPosition(clientID,'STL_Imported_sub14',0, vrep.simx_opmode_streaming)
        #errorCode, Xaxis_joint = vrep.simxSetObjectPosition(clientID, 'Xaxis_joint', vrep.simx_opmode_oneshot_wait)
        
        if errorCode==-1:
            print('Can not find left or right motor')
            sys.exit()
        
        
        print(test)
        print("test")
        #i =360
        #for i in range(360):
        #    errorCode = vrep.simxSetJointPosition(clientID, Xaxis_joint,i*deg, vrep.simx_opmode_oneshot_wait)
        #def setJointPosition(incAngle, steps):
        #    for i  in range(steps): errorCode = vrep.simxSetJointPosition(clientID, jointx, i*incAngle*deg, vrep.simx_opmode_oneshot_wait)
        
        #setJointPosition(10, 720)
        

'''        
-- Put some initialization code here:
simSetThreadSwitchTiming(2) -- Default timing for automatic thread switching
simExtRemoteApiStart(19999)


-- Here we execute the regular thread code:
res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    simAddStatusbarMessage('Lua runtime error: '..err)
end

-- Put some clean-up code here:
'''
 
