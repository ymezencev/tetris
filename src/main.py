
import sys

from PyQt5 import QtGui, QtCore, QtWidgets                           
from project_css import style
from tetris import HighScores, Tetris, NexiPieces


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
pages = {"StartPage": 0, "GamePage": 1}


class MainWindow(QtWidgets.QMainWindow):
    # The main window that contains all the pages
    def __init__(self):
        super().__init__()    

        # Main window settings 
        self.icon = "logo.png"

        self.setWindowTitle('Tetris')
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)                
        self.setWindowIcon(QtGui.QIcon(self.icon))    
        self.setStyleSheet(style)                                         
        
        # App pages
        self.appStack = QtWidgets.QStackedWidget()
        
        self.startPage = StartPage()                
        self.gamePage = GamePage()
        self.appStack.addWidget(self.startPage)
        self.appStack.addWidget(self.gamePage)               

        self.appStack.setCurrentIndex(pages['StartPage'])
        #self.appStack.setCurrentIndex(pages['GamePage'])
        self.setCentralWidget(self.appStack)

        self.center()

    def center(self):
        # Move an app to the center of a screen
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())    


class StartPage(QtWidgets.QWidget):
    # The first page you see when you launch the app
    def __init__(self):
        super().__init__()              
        self.hbox = QtWidgets.QHBoxLayout()            
        self.setLayout(self.hbox)

        self.start_btn = QtWidgets.QPushButton()
        self.start_btn.setFixedSize(QtCore.QSize(400, 120))
        self.start_btn.setText("START GAME")
        self.start_btn.clicked.connect(lambda: window.appStack.setCurrentIndex(pages["GamePage"]))

        self.hbox.addWidget(self.start_btn)


class GamePage(QtWidgets.QWidget):
    # Page where you play tetris    
    def __init__(self):
        super().__init__()              
        
        self.hbox = QtWidgets.QHBoxLayout()        
        self.setLayout(self.hbox)        

        self.tetris = Tetris()        
        self.scores = HighScores()
        self.empty_space = QtWidgets.QWidget()
        self.next_pieces = NexiPieces()
        
        self.hbox.addWidget(self.scores)
        self.hbox.addWidget(self.tetris)                              
        self.hbox.addWidget(self.next_pieces)   


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
