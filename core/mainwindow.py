# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import platform
from . import serialportcontext
import threading
import time
import serial

from .Ui_mainwindow import Ui_MainWindow
from .monitor.machine_mointor import Machine
# from .graphy.graphy import Dialog
import pnael
import os
import sys
from .vrep.vrep_setting import vrepsetting


class Thread_wait_forLNC(QThread):
    lnc_signal = pyqtSignal(int)

    def __init__(self, folder, parent=None):
        QThread.__init__(self, parent)
        self.folder = folder
        self.flag = True

    def run(self):
        t0 = 0
        while self.flag:
            if os.path.isfile(f'{self.folder}/START'):
                os.remove(f"{self.folder}/START")
                if t0 == 0:
                    t0 = 1
                    self.lnc_signal.emit(0)
            elif os.path.isfile(f'{self.folder}/STOP'):
                self.flag = False
                self.remove_stopflag()
            else:
                t0 = 0
            time.sleep(0.5)

    def remove_stopflag(self):
        os.remove(f"{self.folder}/STOP")

    def stop_flag(self):
        self.flag = False

    def create_end_file(self):
        f = open(f"{self.folder}/END", "w")
        f.close()

class MainWindow(QMainWindow):
    """ 
    Class documentation goes here.
    """
    _receive_signal = QtCore.pyqtSignal(str)
    _auto_send_signal = QtCore.pyqtSignal()

    def __init__(self, args, parent=None):

        super(MainWindow, self).__init__(parent)
        loadUi("core/mainwindow.ui", self)
        # self.setupUi(self)
        self.show()
        '''
        pal = QPalette()
        pal.setColor(QPalette.Background, QColor(125,125 ,125))
        
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        '''
        self.initForms()

        # self.comboBoxBaud.setCurrentIndex(len(bauds) - 1)

    def initForms(self):

        if platform.system() == "Windows":
            ports = list()
            for i in range(8):
                ports.append("COM%d" % ((i + 1)))
            self.comboBoxPort.addItems(ports)
            print(ports)
        else:
            # todo:scan system serial port
            self.__scanSerialPorts__()

        bauds = ["50", "75", "134", "110", "150", "200", "300", "600", "1200", "2400", "4800", "9600", "14400", "19200",
                 "38400", "56000", "57600",
                 "115200"]
        self.comboBoxBaud.addItems(bauds)
        self.comboBoxBaud.setCurrentIndex(len(bauds) - 1)

        checks = ["None", "Odd", "Even", "Zero", "One"]
        self.comboBoxCheckSum.addItems(checks)
        self.comboBoxCheckSum.setCurrentIndex(len(checks) - 1)

        bits = ["4 Bits", "5 Bits", "6 Bits", "7 Bits", "8 Bits"]
        self.comboBoxBits.addItems(bits)
        self.comboBoxBits.setCurrentIndex(len(bits) - 1)

        stopbits = ["1 Bit", "1.5 Bits", "2 Bits"]
        self.comboBoxStopBits.addItems(stopbits)
        self.comboBoxStopBits.setCurrentIndex(0)

        # self._auto_send_signal.connect(self.__auto_send_update__)

        # self.xAxis

        port = self.comboBoxPort.currentText()
        baud = int("%s" % self.comboBoxBaud.currentText(), 10)
        self._serial_context_ = serialportcontext.SerialPortContext(port=port, baud=baud)

        #        self.lineEditReceivedCounts.setText("0")
        #        self.lineEditSentCounts.setText("0")
        self.pushButtonOpenSerial.clicked.connect(self.__open_serial_port__)
        # self.pushButtonClearRecvArea.clicked.connect(self.__clear_recv_area__)
        self.pushButtonSendData.clicked.connect(self.__send_data__)
        self._receive_signal.connect(self.__display_recv_data__)
        self._receive_signal.connect(self.__test_received__)
        # self.pushButtonOpenRecvFile.clicked.connect(self.__save_recv_file__)
        self.actionSend.triggered.connect(self.__open_send_file__)
        # self.actionOpenGL.triggered.connect(self.__opengl__)
        self.actionVrep.triggered.connect(self.__teset__)
        self._send_file_data = ''
        self.numberx = 0
        self.numbery = 0
        self.numberz = 0
        # self.__control__()
        self.actionControl.triggered.connect(self.__control__)

        ##machine_control button setting
        self.unlockMachine.clicked.connect(self.__unlockMachine__)
        self.yAxisup.clicked.connect(self.__yAxisup__)
        self.yAxisdown.clicked.connect(self.__yAxisdown__)
        self.xAxisrigh.clicked.connect(self.__xAxisrigh__)
        self.xAxisleft.clicked.connect(self.__xAxisleft__)
        self.zupButton.clicked.connect(self.__zupButton__)
        self.zdownButton.clicked.connect(self.__zdownButton__)

        self.tt = ""

    # def __auto_send_update__(self):
    #    self.lineEditSentCounts.setText("%d" % self._serial_context_.getSendCounts())

    def __teset__(self):
        dlg1 = vrepsetting()
        dlg1.show()
        if dlg1.exec_(): pass
        # self.GLWidget = QOpenGLWidget()
        """
        self.openGLWidget = gl.GLViewWidget()
        self.horizontalLayout.insertWidget(0, self.openGLWidget)
        self.openGLWidget.show()
        g = gl.GLGridItem()
        g.scale(2,2,1)
        self.openGLWidget.addItem(g)
        #plot = pg.PlotWidget()
        #self.openGLWidget = QOpenGLWidget()
        #self.openGLWidget = gl.GLViewWidget()
        #self.openGLWidget.setCameraPosition(distance=40)
        #self.openGLWidget.addWidget(plot) 
        #self.openGLWidget.show()
        #123
        #self.openGLWidget.setWindowTitle('pyqtgraph example: GLMeshItem')
        #self.openGLWidget.setCameraPosition(distance=40)
        """
        print("I'm test")

    '''
    def __opengl__(self):
        dlg2 = Dialog()
        dlg2.show()
        if dlg2.exec_(): pass
    '''

    @pyqtSlot()
    def on_automode_btn_clicked(self):
        # run the automode wait for signal
        self.lnc_thread = Thread_wait_forLNC(f"C:/Users/smpss/kmol/Pyquino")
        self.lnc_thread.lnc_signal.connect(self.test_process)
        self.lnc_thread.start()

    def test_process(self):
        """auto mode send the gcode from PAON"""
        if os.path.isfile(f'C:/Users/smpss/kmol/Pyquino/data.txt'):
            f = open("C:/Users/smpss/kmol/Pyquino/data.txt", "r")
            # print(f"$J=G21G91Y{f.read()}F150")
            text = f"$J=G21G91Y{f.read()}F250"
            f.close()
            print(text)
            self.__test__send(text)
            self.qti = QTimer()
            self.qti.timeout.connect(self.aaa)
            self.qti.start(500)
            os.remove(f"C:/Users/smpss/kmol/Pyquino/data.txt")
        # check the locate
        # self.__test__send("?")
        # print(self.tt)
        # self.lnc_thread.create_end_file()

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
                    print("g1", filename)
                    line = self._send_file_.readlines()
                    print(line)
                    if not line:
                        break
                    else:
                        self._send_file_data += line
                self._send_file_.close()
                self._send_file_ = None
            # self.textEditSent.clear()
            if len(self._send_file_data) > 0:
                print("123", self._send_file_data)
                self.textEditSent.setText(self._send_file_data)
        except Exception as e:
            print(e)
            # QtGui.QMessageBox.critical(self,u"打开文件",u"无法打开文件,请检查!")

    def __unlockMachine__(self):
        print("unlock")
        pass

    def __test_received__(self, data):
        if data.startswith("<Idle"):
            x, y, z = data.split("|")[1].split(":")[1].split(",")
            print(f"X:{x} Y:{y} Z:{z}")
            self.stop_timer()

        elif data.startswith("<Run|"):
            pass

    def __yAxisup__(self):
        print("yAxisup")
        getstep = self.stepbox.value()
        print(getstep)
        self.numbery = pnael.__pane__(self.numbery, getstep)
        self.yAxis.display(self.numbery)
        ## do for the project to went the gcode (+)
        text = str(getstep)
        data = str('G91' + '\n' + 'G01' + 'y' + text + '\n' + 'G90' + '\n')
        if self._serial_context_.isRunning():
            if len(data) > 0: self._serial_context_.send(data, 0)
        pass

    def __yAxisdown__(self):
        print("yAxisdown")
        self.numbery = pnael.__minerse__(self.numbery, self.stepbox.value())
        self.yAxis.display(self.numbery)
        ## do for the project to wend the gcode  (-)
        text = str(-1 * self.stepbox.value())
        print(text)
        data = str('G91' + '\n' + 'G01' + 'y' + text + '\n' + 'G90' + '\n')
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
        # self.lineEditSentCounts.setText("0")

    def __clear_recv_counts(self):
        self._serial_context_.clearRecvCounts()

    # self.lineEditReceivedCounts.setText("0")

    def __set_display_hex__(self):
        self.textEditReceived.clear()

    def __display_recv_data__(self, data):
        # for l in range(len(data)):
        #   hexstr = "%02X " % ord(str(data[l]))
        #  self.textEditReceived.insertPlainText(hexstr)
        # print("gogog", data)
        for l in range(len(data)):
            self.textEditReceived.insertPlainText(data[l])
            sb = self.textEditReceived.verticalScrollBar()
            sb.setValue(sb.maximum())
        for c in range(len(data)):
            self.textEditReceived2.insertPlainText(data[c])
            sb = self.textEditReceived2.verticalScrollBar()
            sb.setValue(sb.maximum())
        # if self.checkBoxNewLine.isChecked():
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
        if self._serial_context_.isRunning():
            self._serial_context_.close()
            self.pushButtonOpenSerial.setText(u'open')
            print("open")
        else:
            try:
                # currentIndex() will get the number
                portss = self.comboBoxPort.currentText()
                port = self.comboBoxPort.currentText()
                print("the", portss)
                baud = int("%s" % self.comboBoxBaud.currentText(), 10)
                self._serial_context_ = serialportcontext.SerialPortContext(port=port, baud=baud)
                # print(self._serial_context_ )
                self._serial_context_.recall()
                self._serial_context_.registerReceivedCallback(self.__data_received__)
                print("4")
                self._serial_context_.open()
                print("5")
                self.pushButtonOpenSerial.setText(u'close')
            except Exception as e:
                print("error")
                # QtGui.QMessageBox.critical(self,u"打开端口",u"打开端口失败,请检查!")

    def __clear_recv_area__(self):
        self.textEditReceived.clear()

    def __clear_send_area__(self):
        self.textEditSent.clear()

    @pyqtSlot()
    def on_test_btn_clicked(self):
        self.__test__send("G0 Y-100")
        time.sleep(0.5)
        self.qti = QTimer()
        self.qti.timeout.connect(self.aaa)
        self.qti.start(500)

    @pyqtSlot()
    def on_stop_clicked(self):
        self.qti.stop()

    def stop_timer(self):
        self.qti.stop()
        self.lnc_thread.create_end_file()

    def aaa(self):
        self.__test__send("?")

    def closeEvent(self, event):
        self._is_auto_sending = False
        if self._serial_context_.isRunning():
            self._serial_context_.close()
            # if self._recv_file_ != None:
        # self._recv_file_.flush()
        # self._recv_file_.close()

    def __data_received__(self, data):
        # print('recv:%s' % data)
        self._receive_signal.emit(data)
        # if self._recv_file_ != None and self.checkBoxSaveAsFile.isChecked():
        #    self._recv_file_.write(data)

    def __test__send(self, data1):
        data = str(data1 + '\n')
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)

    def __send_data__(self):
        data = str(self.textEditSent.toPlainText() + '\n')
        print("i m data", data)
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)
                print(data)
                # self.lineEditSentCounts.setText("%d" % self._serial_context_.getSendCounts())
                # if self.checkBoxEmptyAfterSent.isChecked():
                # self.textEditSent.clear()

                # if self.checkBoxSendLooping.isChecked():
                #  self.pushButtonSendData.setEnabled(False)
                # delay = self.spinBox.value() * 100.0 / 1000.0
                # delay = 100.0 / 1000.0
                # self._auto_send_thread = threading.Thread(target=self.__auto_send__,args=(delay,))

                # self._is_auto_sending = True
                # self._auto_send_thread.setDaemon(True)
                # self._auto_send_thread.start()

    def __auto_send__(self, delay):
        while self._is_auto_sending:
            # if self.checkBoxSendFile.isChecked():
            # if len(self._send_file_data) > 0:
            # self._serial_context_.send(self._send_file_data, self.checkBoxSendHex.isChecked())
            # self._auto_send_signal.emit()
            # break
            # else:
            data = str(self.textEditSent.toPlainText())
            print("123gogo", data)
            if self._serial_context_.isRunning():
                if len(data) > 0:
                    self._serial_context_.send(data, 1)
                    # self._auto_send_signal.emit()
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

        data = str('G29' + '\n')
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)


#        MainWindow.__test__send(self, data)
# self.__test__send(self, data)
'''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    run = MainWindow()
    run.show()
    sys.exit(app.exec_())

'''
