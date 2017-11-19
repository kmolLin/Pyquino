# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets , QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import platform
from . import serialportcontext
import time
from .Ui_mainwindow import Ui_MainWindow



class MainWindow(QMainWindow, Ui_MainWindow):

    _receive_signal = QtCore.pyqtSignal(str)
    _auto_send_signal = QtCore.pyqtSignal()
    def __init__(self, args, parent=None):
        
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initForms()
        
    def initForms(self):
        
        if platform.system() == "Windows":
            ports = list()
            for i in range(8):
                ports.append("COM%d" %((i+1)))    
            self.comboBoxPort.addItems(ports)
            #print(ports)
        else:
            self.__scanSerialPorts__()
        # setting bauds and get serial port
        bauds = ["50","75","134","110","150","200","300","600","1200","2400","4800","9600","14400","19200","38400","56000","57600",
            "115200"]
        self.comboBoxBaud.addItems(bauds)
        self.comboBoxBaud.setCurrentIndex(len(bauds) - 1)
        # setting Checkbox 
        checks = ["None","Odd","Even","Zero","One"]
        self.comboBoxCheckSum.addItems(checks)
        self.comboBoxCheckSum.setCurrentIndex(len(checks) - 1)
        # setting start Bit of the hex
        bits = ["4 Bits", "5 Bits","6 Bits", "7 Bits", "8 Bits"]
        self.comboBoxBits.addItems(bits)
        self.comboBoxBits.setCurrentIndex(len(bits) - 1)
        #setting stop bit of the box
        stopbits = ["1 Bit","1.5 Bits","2 Bits"];
        self.comboBoxStopBits.addItems(stopbits)
        self.comboBoxStopBits.setCurrentIndex(0)
        # get the comboBox get number
        port = self.comboBoxPort.currentText()
        baud = int("%s" % self.comboBoxBaud.currentText(), 10)
        self._serial_context_ = serialportcontext.SerialPortContext(port = port,baud = baud)
        
        # connect to the method of UI items
        self.pushButtonOpenSerial.clicked.connect(self.__open_serial_port__)
        self.pushButtonSendData.clicked.connect(self.__send_data__)
        self._receive_signal.connect(self.__display_recv_data__)
        self.actionSend.triggered.connect(self.__open_send_file__)
        self._send_file_data = ''
    
    #TODO: send file but not do yet
    def __open_send_file__(self):
        filename = QFileDialog.getOpenFileName(self, caption="Open Send File")
        try:
            if filename and 0:
                print(filename)
                self._send_file_ = open(filename, 'r', encoding='UTF-8')
                while True:
                    line = self._send_file_.readlines()
                    print(line)
                    if not line: break
                    else: self._send_file_data += line
                self._send_file_.close()
                self._send_file_ = None
            if len(self._send_file_data) > 0:
                self.textEditSent.setText(self._send_file_data)
        except Exception as e:
            print(e)
            #QtGui.QMessageBox.critical(self,u"open files",u"please chech the files !")
    
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
        self.textEditReceived.insertPlainText(data)
        for l in range(len(data)):
            sb = self.textEditReceived.verticalScrollBar()
            sb.setValue(sb.maximum())
        for c in range(len(data)):
            self.textEditReceived2.insertPlainText(data[c])
            sb = self.textEditReceived2.verticalScrollBar()
            sb.setValue(sb.maximum())
    
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
                portss = self.comboBoxPort.currentText()
                port = self.comboBoxPort.currentText()
                baud = int("%s" % self.comboBoxBaud.currentText(),10)
                self._serial_context_ = serialportcontext.SerialPortContext(port = port,baud = baud)
                self._serial_context_ .recall()
                self._serial_context_.registerReceivedCallback(self.__data_received__)
                self._serial_context_.open()
                self.pushButtonOpenSerial.setText(u'close')
            except Exception as e:
                print("error")
                #QtGui.QMessageBox.critical(self,u"Open port",u"please check the port!")
    
    def __clear_recv_area__(self): self.textEditReceived.clear()
    def __clear_send_area__(self): self.textEditSent.clear()
    
    def closeEvent(self, event):
        self._is_auto_sending = False
        if self._serial_context_.isRunning():
            self._serial_context_.close()
    
    def __data_received__(self,data):
        self._receive_signal.emit(data)
    
    def __test__send(self, data1):
        data = str(data1+'\n')
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)
    
    def __send_data__(self):
        data = str(self.textEditSent.toPlainText()+'\n')
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)
    
    def __auto_send__(self,delay):
        while self._is_auto_sending:
            data = str(self.textEditSent.toPlainText())
            if self._serial_context_.isRunning():
                if len(data) > 0:
                    self._serial_context_.send(data, 1)
            time.sleep(delay)
    

