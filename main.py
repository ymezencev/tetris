from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QDesktopWidget, QStackedWidget, QWidget, QPushButton, QGridLayout
from PyQt5 import QtGui, QtCore, QtWidgets
import sys

from styles import project_css
from config import WINDOW_WIDTH, WINDOW_HEIGHT

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

        self.appStack.setCurrentIndex(1)        
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
        self.grid = QGridLayout()        
        self.setLayout(self.grid)

        self.start_btn = QPushButton()
        self.start_btn.setFixedSize(QtCore.QSize(400, 120))
        self.start_btn.setText("START GAME")
        self.start_btn.clicked.connect(lambda: window.appStack.setCurrentIndex(pages["GamePage"]))

        self.grid.addWidget(self.start_btn)


class GamePage(QWidget):
    def __init__(self):
        super().__init__()		        
        self.grid = QGridLayout()        
        self.setLayout(self.grid)

        self.tetris = Tetris()
        self.empty_space = QWidget()
        self.grid.addWidget(self.tetris, 1, 0)
        self.grid.addWidget(self.empty_space, 0, 0) 
        self.grid.addWidget(self.empty_space, 2, 0)
                

class Tetris(QWidget):
    def __init__(self):
        super().__init__()		   
        self.setFixedSize(QtCore.QSize(410, 820))     
        self.grid = QGridLayout()                
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(1)        
        self.setLayout(self.grid)        
        

        for i in range(20):
            for j in range(10):
                empty_piece = Piece()                 
                self.grid.addWidget(empty_piece, i, j)




class Piece(QPushButton):
    def __init__(self, color='#D0D0D0'):
        super().__init__()		
        self.color = color
        self.setFixedSize(QtCore.QSize(40, 40))
        self.setStyleSheet(f'background: {self.color};')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
