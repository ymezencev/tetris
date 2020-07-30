from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget,  \
                            QStackedWidget, QWidget, QPushButton, \
                            QVBoxLayout, QHBoxLayout, QLabel                            
from PyQt5 import QtGui, QtCore, QtWidgets
import sys

from styles import project_css
from config import WINDOW_WIDTH, WINDOW_HEIGHT

from tetris import HighScores, Tetris, NexiPieces

pages = {"StartPage": 0, "GamePage": 1}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()    

        # Main window settings 
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.icon = "logo.png"

        self.setWindowTitle('Tetris')
        self.setMinimumSize(self.width, self.height)                
        self.setWindowIcon(QtGui.QIcon(self.icon))    
        self.setStyleSheet(project_css)           						        
        
		# Pages
        self.appStack = QStackedWidget()
        
        self.startPage = StartPage()                
        self.gamePage = GamePage()
        self.appStack.addWidget(self.startPage)
        self.appStack.addWidget(self.gamePage)               

        #self.appStack.setCurrentIndex(pages['StartPage'])
        self.appStack.setCurrentIndex(pages['GamePage'])        
        self.setCentralWidget(self.appStack)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class StartPage(QWidget):
    def __init__(self):
        super().__init__()		        
        self.hbox = QHBoxLayout()            
        self.setLayout(self.hbox)

        self.start_btn = QPushButton()
        self.start_btn.setFixedSize(QtCore.QSize(400, 120))
        self.start_btn.setText("START GAME")
        self.start_btn.clicked.connect(lambda: window.appStack.setCurrentIndex(pages["GamePage"]))

        self.hbox.addWidget(self.start_btn)


class GamePage(QWidget):
    def __init__(self):
        super().__init__()		        
        self.hbox = QHBoxLayout()        
        self.setLayout(self.hbox)        

        self.tetris = Tetris()        
        self.scores = HighScores()
        self.empty_space = QWidget()
        self.next_pieces = NexiPieces()
        
        self.hbox.addWidget(self.scores)
        self.hbox.addWidget(self.tetris)                              
        self.hbox.addWidget(self.next_pieces)   


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
