# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets , QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import platform
from . import serialportcontext
import threading
import time
import serial

from .Ui_mainwindow import Ui_MainWindow
#from .Ui_mainwindow2 import Ui_MainWindow2
from .monitor.machine_mointor import Machine
from .graphy.graphy import Dialog
from .GraphyViewModule import graphy
from .RightClick import rightClick
import pnael 
from .settingForm import SettingForm

from .vrep.vrep_setting import vrepsetting



class MainWindow(QMainWindow, Ui_MainWindow):

    _receive_signal = QtCore.pyqtSignal(str)
    _auto_send_signal = QtCore.pyqtSignal()
    def __init__(self, args, parent=None):
        
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        rightClick(self)
        '''
        pal = QPalette()
        pal.setColor(QPalette.Background, QColor(125,125 ,125))
        
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        '''
        print(args)
        self.initForms()

        #self.comboBoxBaud.setCurrentIndex(len(bauds) - 1)        
        
        
    def initForms(self):
        
        if platform.system() == "Windows":
            ports = list()
            for i in range(8):
                ports.append("COM%d" %((i+1)))    
            self.comboBoxPort.addItems(ports)
            print(ports)
        else:
            #todo:scan system serial port
            self.__scanSerialPorts__()
        
        bauds = ["50","75","134","110","150","200","300","600","1200","2400","4800","9600","14400","19200","38400","56000","57600",
            "115200"]
        self.comboBoxBaud.addItems(bauds)
        self.comboBoxBaud.setCurrentIndex(len(bauds) - 1)
        
        checks = ["None","Odd","Even","Zero","One"]
        self.comboBoxCheckSum.addItems(checks)
        self.comboBoxCheckSum.setCurrentIndex(len(checks) - 1)
        
        bits = ["4 Bits", "5 Bits","6 Bits", "7 Bits", "8 Bits"]
        self.comboBoxBits.addItems(bits)
        self.comboBoxBits.setCurrentIndex(len(bits) - 1)
        
        stopbits = ["1 Bit","1.5 Bits","2 Bits"];
        self.comboBoxStopBits.addItems(stopbits)
        self.comboBoxStopBits.setCurrentIndex(0)
        
        
        #self._auto_send_signal.connect(self.__auto_send_update__)
        
        port = self.comboBoxPort.currentText()
        baud = int("%s" % self.comboBoxBaud.currentText(), 10)
        self._serial_context_ = serialportcontext.SerialPortContext(port = port,baud = baud)
        
#        self.lineEditReceivedCounts.setText("0")
#        self.lineEditSentCounts.setText("0")
        self.pushButtonOpenSerial.clicked.connect(self.__open_serial_port__)
       # self.pushButtonClearRecvArea.clicked.connect(self.__clear_recv_area__)
        self.pushButtonSendData.clicked.connect(self.__send_data__)
        self._receive_signal.connect(self.__display_recv_data__)
       # self.pushButtonOpenRecvFile.clicked.connect(self.__save_recv_file__)
        self.actionSend.triggered.connect(self.__open_send_file__)
        self.actionOpenGL.triggered.connect(self.__opengl__)
        self.actionVrep.triggered.connect(self.__teset__)
        self._send_file_data = ''
        self.numberx = 0
        self.numbery = 0
        self.numberz = 0
        #self.__control__()
        self.actionControl.triggered.connect(self.__control__)
        
        ##machine_control button setting
        self.unlockMachine.clicked.connect(self.__unlockMachine__)
        self.yAxisup.clicked.connect(self.__yAxisup__)
        self.yAxisdown.clicked.connect(self.__yAxisdown__)
        self.xAxisrigh.clicked.connect(self.__xAxisrigh__)
        self.xAxisleft.clicked.connect(self.__xAxisleft__)
        self.zupButton.clicked.connect(self.__zupButton__)
        self.zdownButton.clicked.connect(self.__zdownButton__)
        self.graphyViewModule.insertWidget(1, graphy())
        # def __auto_send_update__(self):
        #    self.lineEditSentCounts.setText("%d" % self._serial_context_.getSendCounts())
   
    @pyqtSlot(QPoint)
    def on_treeWidget_context_menu(self, point):
        action = self.popMenu_treeWidget.exec_(self.treeWidget.mapToGlobal(point))
        if action == self.action_treeWidget_add:
            dlg = SettingForm()
            dlg.show()
            if dlg.exec_():
                self.formfile = dlg.getlist
                self.reflesh()
                print(self.formfile)
        elif action ==self.action_treeWidget_del:
            try :
                self.tree.takeTopLevelItem(self.treeitemSelct[1])
            except:
                print("No select")
        elif action == self.action_treeWidget_send:
            try :
                ## 0807 not yet to do
                data = 'asa'
                if self._serial_context_.isRunning():
                    if len(data) > 0: self._serial_context_.send(data, 0)
                    print(self.tree.currentItem().takeChildren())
            except:
                pass
                
                
    def reflesh(self):
        if self.formfile['component'] == "Motor":
            root = QTreeWidgetItem([self.formfile['Name'], self.formfile['component']])
            root.setFlags((root.flags() | Qt.ItemIsEditable))
            root.addChild(QTreeWidgetItem(["Max", str(self.formfile['Mini']) ]))
            root.addChild(QTreeWidgetItem(["Min", str(self.formfile['Max'])]))
            root.addChild(QTreeWidgetItem(["signal", self.formfile['signal']]))
            
            self.tree.addTopLevelItem(root)
        elif self.formfile['component'] == "Sensor":
            root = QTreeWidgetItem([self.formfile['Name'], self.formfile['component']])
            root.setFlags((root.flags() | Qt.ItemIsEditable))
            root.addChild(QTreeWidgetItem(["signal", self.formfile['signal']]))
            
            self.tree.addTopLevelItem(root)
        elif self.formfile['component'] == "Light":
            root = QTreeWidgetItem([self.formfile['Name'], self.formfile['component']])
            root.setFlags((root.flags() | Qt.ItemIsEditable))
            root.addChild(QTreeWidgetItem(["signal", self.formfile['signal']]))
            self.tree.addTopLevelItem(root)
        
        
        
    
    def __teset__(self):
        dlg1 = vrepsetting()
        dlg1.show()
        if dlg1.exec_(): pass
        #self.GLWidget = QOpenGLWidget()
        print("I'm test")
    
    def __opengl__(self):
        dlg2 = Dialog()
        dlg2.show()
        if dlg2.exec_(): pass
            #a  = dlg2.a
    
    def __control__(self):
        print("control open")
        dlg = Machine()
        dlg.show()
        if dlg.exec_(): pass
    
    def __open_send_file__(self):
        filename = QFileDialog.getOpenFileName(self, caption="Open Send File")
        print("123")
        try:
            if filename and 0:
                print(filename)
                self._send_file_ = open(filename, 'r', encoding='UTF-8')
                while True:
                    print("g1",filename )
                    line = self._send_file_.readlines()
                    print(line)
                    if not line: break
                    else: self._send_file_data += line
                self._send_file_.close()
                self._send_file_ = None
            #self.textEditSent.clear()
            if len(self._send_file_data) > 0:
                print("123", self._send_file_data)
                self.textEditSent.setText(self._send_file_data)
        except Exception as e:
            print(e)
            #QtGui.QMessageBox.critical(self,u"打开文件",u"无法打开文件,请检查!")
    
    def __unlockMachine__(self):
        print("unlock")
        pass
    
    def __yAxisup__(self):
        print("yAxisup")
        getstep = self.stepbox.value()
        print(getstep)
        self.numbery = pnael.__pane__(self.numbery, getstep)
        self.yAxis.display(self.numbery)
        ## do for the project to went the gcode (+)
        text = str(getstep)
        data = str('G91'+'\n'+'G01'+ 'y'+text+'\n'+ 'G90'+'\n')
        if self._serial_context_.isRunning():
            if len(data) > 0: self._serial_context_.send(data, 0)
        pass
    
    def __yAxisdown__(self):
        print("yAxisdown")
        self.numbery = pnael.__minerse__(self.numbery, self.stepbox.value())
        self.yAxis.display(self.numbery)
        ## do for the project to wend the gcode  (-)
        text = str(-1*self.stepbox.value())
        print(text)
        data = str('G91'+'\n'+'G01'+ 'y'+text+'\n'+ 'G90'+'\n')
        if self._serial_context_.isRunning():
            if len(data) > 0: self._serial_context_.send(data, 0)
        pass
    
    def __xAxisrigh__(self):
        print("xAxisright")
        self.numberx = pnael.__pane__(self.numberx, self.stepbox.value())
        print(self.numberx)
        self.xAxis.display(self.numberx)
        pass
    
    def __xAxisleft__(self):
        print("xAxisleft")
        self.numberx = pnael.__minerse__(self.numberx, self.stepbox.value())
        self.xAxis.display(self.numberx)
        pass
    
    def __zupButton__(self):
        print("zupButton")
        self.numberz = pnael.__pane__(self.numberz, self.stepbox.value())
        self.zAxis.display(self.numberz)
        pass
    
    def __zdownButton__(self):
        print("zdownButton")
        self.numberz = pnael.__minerse__(self.numberz, self.stepbox.value())
        self.zAxis.display(self.numberz)
        pass
    
    def __handle_send_looping__(self):
        if self._is_auto_sending:
            self._is_auto_sending = False
            self.pushButtonSendData.setEnabled(True)
    
    def __clear_all_counts(self):
       # self.lineEditReceivedCounts.setText("0")
       # self.lineEditSentCounts.setText("0")
        self._serial_context_.clearAllCounts()
    
    def __clear_send_counts(self):
        self._serial_context_.clearSentCounts()
        #self.lineEditSentCounts.setText("0")
    
    def __clear_recv_counts(self):
        self._serial_context_.clearRecvCounts()
       # self.lineEditReceivedCounts.setText("0")
    
    def __set_display_hex__(self):
        self.textEditReceived.clear()    
    
    def __display_recv_data__(self,data):
        #for l in range(len(data)):
        #   hexstr = "%02X " % ord(str(data[l]))
        #  self.textEditReceived.insertPlainText(hexstr)
        self.textEditReceived.insertPlainText(data)
        print("gogog",len(data))
        for l in range(len(data)):
            #self.textEditReceived.insertPlainText(data[l])  
            sb = self.textEditReceived.verticalScrollBar()
            sb.setValue(sb.maximum())
            #print("test recive", data[l])
        for c in range(len(data)):
            self.textEditReceived2.insertPlainText(data[c])
            sb = self.textEditReceived2.verticalScrollBar()
            sb.setValue(sb.maximum())
        #if self.checkBoxNewLine.isChecked():
        #    self.textEditReceived.insertPlainText("\n")
        # self.lineEditReceivedCounts.setText("%d" % self._serial_context_.getRecvCounts())
    
    def __scanSerialPorts__(self):
        ports = []
        for i in range(32):
            ports.append("/dev/ttyS%d" % i)
        for i in range(32):
            ports.append("/dev/ttyACM%d" % i)
        self.comboBoxPort.addItems(ports)
    
    def __open_serial_port__(self):
        if  self._serial_context_.isRunning():
            self._serial_context_.close()
            self.pushButtonOpenSerial.setText(u'open')
            print("open")
        else:
            try:
                #currentIndex() will get the number
                portss = self.comboBoxPort.currentText()
                port = self.comboBoxPort.currentText()
                print("the", portss)
                baud = int("%s" % self.comboBoxBaud.currentText(),10)
                self._serial_context_ = serialportcontext.SerialPortContext(port = port,baud = baud)
                #print(self._serial_context_ )
                self._serial_context_ .recall()
                self._serial_context_.registerReceivedCallback(self.__data_received__)
                print("4")
                self._serial_context_.open()
                print("5")
                self.pushButtonOpenSerial.setText(u'close')
            except Exception as e:
                print("error")
                #QtGui.QMessageBox.critical(self,u"打开端口",u"打开端口失败,请检查!")
    
    def __clear_recv_area__(self): self.textEditReceived.clear()
    def __clear_send_area__(self): self.textEditSent.clear()
    
    def closeEvent(self, event):
        self._is_auto_sending = False
        if self._serial_context_.isRunning():
            self._serial_context_.close()
        # if self._recv_file_ != None:
            print("123")
           # self._recv_file_.flush()
           # self._recv_file_.close()
    
    def __data_received__(self,data):
        print('recv:%s' % data)
        self._receive_signal.emit(data)
        #if self._recv_file_ != None and self.checkBoxSaveAsFile.isChecked():
        #    self._recv_file_.write(data)
    
    def __test__send(self, data1):
        print(data1)
        data = str(data1+'\n')
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)
                print(data)
    
    def __send_data__(self):
        data = str(self.textEditSent.toPlainText()+'\n')
        print("i m data", data)
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)
                print(data)
                #self.lineEditSentCounts.setText("%d" % self._serial_context_.getSendCounts())
                #if self.checkBoxEmptyAfterSent.isChecked():
                    #self.textEditSent.clear()
            
                #if self.checkBoxSendLooping.isChecked():
                  #  self.pushButtonSendData.setEnabled(False)
                    #delay = self.spinBox.value() * 100.0 / 1000.0
                    #delay = 100.0 / 1000.0
                   # self._auto_send_thread = threading.Thread(target=self.__auto_send__,args=(delay,))
                    
                   # self._is_auto_sending = True
                   # self._auto_send_thread.setDaemon(True)
                    #self._auto_send_thread.start()
    
    def __auto_send__(self,delay):
        while self._is_auto_sending:
            #if self.checkBoxSendFile.isChecked():
                #if len(self._send_file_data) > 0:
                    #self._serial_context_.send(self._send_file_data, self.checkBoxSendHex.isChecked())
                    #self._auto_send_signal.emit()
                    #break
            #else:
            data = str(self.textEditSent.toPlainText())
            print("123gogo", data)
            if self._serial_context_.isRunning():
                if len(data) > 0:
                    self._serial_context_.send(data, 1)
                    #self._auto_send_signal.emit()
            time.sleep(delay)
    
    @pyqtSlot()
    def on_homeButton_clicked(self):
        print("test the button")
        self.numberx = 0
        self.numbery = 0
        self.numberz = 0
        
        self.xAxis.display(self.numberx)
        self.yAxis.display(self.numbery)
        self.zAxis.display(self.numberz)
        
        data = str('G29'+'\n')
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)
#        MainWindow.__test__send(self, data)
        #self.__test__send(self, data)
        

    
    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    def on_tree_currentItemChanged(self, current, previous):
        """
        Slot documentation goes here.
        
        @param current DESCRIPTION
        @type QTreeWidgetItem
        @param previous DESCRIPTION
        @type QTreeWidgetItem
        """
        # TODO: not implemented yet
        #print(current.text(0))

    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_tree_itemChanged(self, item, column):
        if column==0:
            finder = lambda x: self.tree.findItems(x, (Qt.MatchFixedString), 1)
            checkName = finder('Sensor')
            checkName += finder('Motor')
            checkName += finder('Light')
            names = [item.text(0) for item in checkName]
            del names[names.index(item.text(0))]
            print(names)
            print(item.text(0) in names)
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_tree_itemClicked(self, item, column):
        self.treeitemSelct = [item, column]
        print(column)

