import  subprocess

from PyQt5.QtWidgets import QStackedWidget, QWidget, QPushButton, \
                            QGridLayout, QVBoxLayout, QHBoxLayout, \
                            QLabel, QTableWidget, QTableWidgetItem
from PyQt5 import QtGui, QtCore, QtWidgets



class HighScores(QWidget):
    def __init__(self):
        super().__init__()        
        self.setFixedWidth(300) 
        self.vbox = QVBoxLayout()                
        self.vbox.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.vbox)                

        self.title = QLabel("High scores")
        self.title.setStyleSheet("font-size: 24px;")                

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
        self.scores_tbl.verticalHeader().setDefaultSectionSize(20)
        self.scores_tbl.verticalHeader().hide()
        self.scores_tbl.horizontalHeader().hide()
        self.scores_tbl.resizeColumnToContents(0)          
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


class Piece(QPushButton):
    def __init__(self, color='#FFFFFF'):
        super().__init__()		
        self.color = color
        self.setFixedSize(QtCore.QSize(40, 40))
        self.setStyleSheet(f'background: {self.color};')


class NexiPieces(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)    
        self.vbox = QVBoxLayout()                
        self.setLayout(self.vbox)        
        self.vbox.setAlignment(QtCore.Qt.AlignTop)
        self.title = QLabel("Next")
        self.title.setStyleSheet("font-size: 24px;")                
        self.vbox.addWidget(self.title)  


class Tetris(QWidget):
    def __init__(self):
        super().__init__()		           
        self.vbox = QVBoxLayout()
        self.setFixedWidth(450)
        self.vbox.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.vbox)


        self.tetrisbox = QWidget()
        self.tetrisbox.setFixedSize(QtCore.QSize(410, 820))                   
        self.grid = QGridLayout()        
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(1)        
        self.tetrisbox.setLayout(self.grid)                

        self.field = [[Piece() for j in range(10)] for i in range(20)]        
        self.draw_field()

        self.field[1][1] = Piece('#000000')
        self.draw_field()
        self.field[2][2] = Piece('#ff0000')
        self.field[1][1] = Piece('#ff0000')

        self.draw_field()
        

        
        self.vbox.addWidget(self.tetrisbox)        

    def draw_field(self):
    	for row_num, row_val in enumerate(self.field):
            for col_num, col_val in enumerate(row_val):
                self.grid.removeWidget(col_val)
                self.grid.addWidget(col_val, row_num, col_num)

    def remove_field(self):
    	for row_num, row_val in enumerate(self.field):
            for col_num, col_val in enumerate(row_val):
                self.grid.removeWidget(col_val)
                col_val.deleteLater()

    def deleteGridWidget(self, index):
        item = self.sa_grid.itemAt(index)
        if item is not None:
        	widget = item.widget()
        	if widget is not None:
        		self.sa_grid.removeWidget(widget)
        		widget.deleteLater()


