from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QDesktopWidget,  \
                            QStackedWidget, QWidget, QPushButton, QGridLayout, QVBoxLayout, \
                            QLabel, QTableWidget, QTableWidgetItem
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
        self.scores = HighScores()
        self.empty_space = QWidget()
        self.next_pieces = NexiPieces()
        
        self.grid.addWidget(self.scores, 0, 1)        
        self.grid.addWidget(self.tetris, 0, 2)                 
        self.grid.addWidget(self.next_pieces, 0, 3)        
        

class HighScores(QWidget):
    def __init__(self):
        super().__init__()
        #self.setFixedSize(QtCore.QSize(300, 100))    
        self.setFixedWidth(300) 
        self.vbox = QVBoxLayout()                
        self.setLayout(self.vbox)        
        
        self.title = QLabel("High scores")
        empty_space = QWidget()

        self.colsDict = {'Rank': 0, 'Player': 1, 'Score': 2}

        self.scores_tbl= QTableWidget()        
        self.scores_tbl.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scores_tbl.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scores_tbl.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scores_tbl.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scores_tbl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.scores_tbl.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.scores_tbl.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scores_tbl.setShowGrid(False)
        self.scores_tbl.setRowCount(0)        
        self.scores_tbl.setColumnCount(3)
        self.scores_tbl.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.scores_tbl.verticalHeader().setDefaultSectionSize(20)
        self.scores_tbl.verticalHeader().hide()
        self.scores_tbl.setHorizontalHeaderLabels([*self.colsDict])            

        self.get_scores()

        self.vbox.addWidget(self.title)        
        self.vbox.addWidget(self.scores_tbl)
        

    def get_scores(self):
        self.scores_tbl.setRowCount(0)
        score_data = [(1, 'Tim', 1000), (2, 'Sam', 950), (3, 'Kate', 900)]

        for row_num, row_data in enumerate(score_data):
            self.scores_tbl.insertRow(row_num)
            for column_num, data in enumerate(row_data):
                self.scores_tbl.setItem(row_num, column_num, QTableWidgetItem(str(data)))


class NexiPieces(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QtCore.QSize(200, 400))     
        self.grid = QGridLayout()                
        self.setLayout(self.grid)        
        
        title = QLabel("Next")

        self.grid.addWidget(title)


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
