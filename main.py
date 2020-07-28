import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QDesktopWidget
from PyQt5 import QtGui, QtCore, QtWidgets
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tetris')
        self.width = 1200
        self.height = 700
        
        self.icon = "logo.png"
        self.setMinimumSize(self.width, self.height)        
        self.center()
        self.setWindowIcon(QtGui.QIcon(self.icon))               


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
