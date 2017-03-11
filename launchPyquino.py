##Start Pyquino
##Use PyQt5 communcation with serial port and vitural machine with Vrep
##Including Python module: PyQt5, pygraphy, pyopengl
##Copyright (C) 2017 you shang [smpss91341@gmail.com]
from core.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication
from core.info import showof
from sys import argv, exit
if __name__=='__main__':
    QApplication.setStyle('fusion')
    app = QApplication(argv)
    run = MainWindow(showof())
    run.show()
    exit(app.exec_())
