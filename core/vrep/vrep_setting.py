# -*- coding: utf-8 -*-

"""
Module implementing vrepsetting.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
import sys, math
from .Ui_vrep_setting import Ui_Dialog

from ..vrep_remoAPI import vrep
#from ..vrep_remoAPI import vrepConst


class vrepsetting(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(vrepsetting, self).__init__(parent)
        self.setupUi(self)
        
        # child threaded script: 
        # 內建使用 port 19997 若要加入其他 port, 在  serve 端程式納入
        #simExtRemoteApiStart(19999)
         
        
    
    @pyqtSlot()
    def on_xAxisleft_clicked(self):
        
        vrep.simxFinish(-1)         
        clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
        deg = math.pi/180
        if clientID!= -1:
            print("Connected to remote server")
        else:
            print('Connection not successful')
            sys.exit('Could not connect')
         
        errorCode,Revolute_joint_handle=vrep.simxGetObjectHandle(clientID,'Revolute_joint',vrep.simx_opmode_oneshot_wait)
         
        if errorCode == -1:
            print('Can not find left or right motor')
            sys.exit()

        def setJointPosition(incAngle, steps):
            for i  in range(steps):
                errorCode=vrep.simxSetJointPosition(clientID, Revolute_joint_handle, i*incAngle*deg, vrep.simx_opmode_oneshot_wait)
        setJointPosition(10, 72)
        print("test")
        
