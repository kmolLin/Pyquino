'''
Start Pyquino 
Use PyQt5 communcation with serial port and vitural machine with Vrep
Including Python module: PyQt5, pygraphy,pyopengl
Copyright (C) 2017 you shang [smpss91341@gmail.com]
'''

from core.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    import sys
    QApplication.setStyle("fusion")
    app = QApplication(sys.argv)
    run = MainWindow()
    run.show()
    sys.exit(app.exec_())
 
