from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import (QApplication, QWidget)

class SerialPortInput(QtWidgets.QTextEdit):
    def __init__(self,parent = None):
        super(SerialPortInput,self).__init__(parent)
        self._is_hex = False
        
    def keyPressEvent(self, event):
        if self._is_hex:
            #event.setText("%2dX " % (ord(str(event.text()))))
            hex_data = "%02X " % (ord(str(event.text())))
            qhex_data = QtCore.QString("%s" % hex_data)
            #print('hex_data = %s' % hex_data)
            new_event = QtWidgets.QKeyEvent(event.type(),event.key(),event.modifiers(),
                                       qhex_data,
                                        event.isAutoRepeat(),event.count())
            return super(SerialPortInput,self).keyPressEvent(new_event)
        else:
            return super(SerialPortInput,self).keyPressEvent(event)
        
    def setIsHex(self,isHex):
        self._is_hex = isHex
