from core.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    import sys
    QApplication.setStyle("fusion")
    app = QApplication(sys.argv)
    run = MainWindow()
    run.show()
    sys.exit(app.exec_())
 
