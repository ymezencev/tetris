from PyQt5.QtWidgets import QStackedWidget, QWidget, QPushButton, \
                            QGridLayout, QVBoxLayout, QHBoxLayout, \
                            QLabel, QTableWidget, QTableWidgetItem
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.Qt import Qt

import random

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


class Cube(QPushButton):
    def __init__(self, color='#fff'):
        super().__init__()		
        self.color = color
        self.locked = False
        self.setFixedSize(QtCore.QSize(40, 40))
        self.update(self.color)        

    def update(self, color="#fff"):
        self.color = color
        self.setStyleSheet(f'background: {self.color};')


class Piece:
    def __init__(self, piece_num, piece_pos, x, y):
        self.x = x
        self.y = y
        self.piece_num = piece_num
        self.piece_pos = piece_pos
        self.locked = False

        O = [[(0, 0), (-1, 0), (-1, -1), (0, -1)]]
        I = [[(-2, 0), (-1, 0), (0, 0), (1, 0)], 
             [(0, 1), (0, 0), (0, -1), (0, -2)]]
        S = [[(-1, -1), (0, -1), (0, 0), (1, 0)],
             [(0, 1), (0, 0), (1, 0), (1. -1)]]
        Z = [[(-1, 0), (0, 0), (0, -1), (1, -1)],
             [(1, 1), (1, 0), (0, 0), (0, -1)]]
        L = [[(-1, -1), (-1, 0), (0, 0), (1, 0)],
             [(0, 1), (0, 0), (0, -1), (1, -1)],
             [(-1, 0), (0, 0), (1, 0), (1, 1)],
             [(-1, 1), (0, 1), (0, 0), (0, -1)]]
        J = [[(-1, 0), (0, 0), (1, 0), (1, -1)],
             [(0, -1), (0, 0), (0, 1), (1, 1)],
             [(-1, 1), (-1, 0), (0, 0), (1, 0)],
             [(-1, -1), (0, -1), (0, 0), (0, 1)]]
        T = [[(-1, 0), (0, 0), (0, -1), (1, 0)],
             [(0, 1), (0, 0), (1, 0), (0, -1)],
             [(-1, 0), (0, 0), (0, 1), (1, 0)],
             [(-1, 0), (0, 0), (0, 1), (0, -1)]]   

        self.shapes = [O, I, S, Z, L, J, T]
        colors = ['blue', 'red', 'yellow', 'green', 'pink', 'orange', 'brown']
        self.color = colors[self.piece_num]        
        self.check_pos()

    def check_pos(self):
        if self.piece_pos >= len(self.shapes[self.piece_num]):
            self.piece_pos = 0

    def get_coords(self):
        self.check_pos()    
        return self.shapes[self.piece_num][self.piece_pos]


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
        
        self.board = [[Cube() for j in range(20)] for i in range(10)]
        self.current_piece = None

        QtWidgets.qApp.installEventFilter(self) 
        self.update_board()        
        self.play_game()
        
        self.vbox.addWidget(self.tetrisbox)

    def update_board(self):
        # clear not locked cubes  
        for col_num, col_cubes in enumerate(self.board):
            for row_num, row_cube in enumerate(col_cubes):
                self.grid.removeWidget(row_cube)
                if not row_cube.locked:
                    row_cube.update()
                self.grid.addWidget(row_cube, row_num, col_num)                

    def remove_board(self): 
        for col_num, col_cubes in enumerate(self.board):
            for row_num, row_cube in enumerate(col_cubes):
                self.grid.removeWidget(row_cube)                
                row_cube.deleteLater()    	

    def get_piece(self):
    	# rand num to get rand piece
        piece_num = random.randint(0,6)        
        start_x = 5
        start_y = 0
        return Piece(piece_num=piece_num, piece_pos=0, x=start_x, y=start_y)

    def draw_piece(self, piece):
        # method adds piece to the board        
        x, y = 0, 1   
        coords = piece.get_coords()                
        for coords in piece.get_coords():            
            new_x = piece.x + coords[x]
            new_y =  piece.y + coords[y]            
            if (0 <= new_y < len(self.board[0])) and (0 <= new_x < len(self.board)):
                self.board[new_x][new_y].update(piece.color)  

    def check_lock(self, piece):
        x, y = 0, 1
        for coords in piece.get_coords():            
            _x = piece.x + coords[x]
            _y = piece.y + coords[y]
            if _y == len(self.board[0])-1:
                return True
            if self.board[_x][_y+1].locked:
                return True
            if self.board[_x+1][_y].locked:
                return True
        return False

    def lock_piece(self, piece):
        x, y = 0, 1
        for coords in piece.get_coords():            
            _x = piece.x + coords[x]
            _y = piece.y + coords[y]
            self.board[_x][_y].locked = True
        piece.locked = True

    def try_move(self, piece, dx=0, dy=0): 
        x, y = 0, 1
        if piece is None:
            return False        
        for coords in piece.get_coords():            
            new_x = piece.x + coords[x] + dx
            new_y = piece.y + coords[y] + dy
            if not (0 <= new_y < len(self.board[0])):
                return False
            if not (0 <= new_x < len(self.board)):
                return False
            if self.board[new_x][new_y].locked:
                return False
        return True

    def move_piece(self, piece, dx=0, dy=0):
        if piece.locked:
            return
        if self.try_move(piece, dx=dx, dy=dy):
            piece.y += dy
            piece.x += dx
            self.update_board()        
            self.draw_piece(piece)
            if self.check_lock(piece):
                self.lock_piece(piece)

    def try_rotate(self, piece):
        if piece.locked:
            return
        prev_pos = piece.piece_pos
        piece.piece_pos += 1
        if not self.try_move(piece):
            piece.piece_pos = prev_pos
            return False
        return True
     
    def rotate_piece(self, piece):
        if self.try_rotate(piece):            
            self.update_board()        
            self.draw_piece(piece)
            if self.check_lock(piece):
                self.lock_piece(piece)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:                    
            key = event.key()
            if key == Qt.Key_Left:
                self.move_piece(self.current_piece, dx=-1)
                return 1
            if key == Qt.Key_Right:
                self.move_piece(self.current_piece, dx=1)
                return 1            
            if key == Qt.Key_Down:
                self.move_piece(self.current_piece, dy=1)
                return 1  
            if key == Qt.Key_Up:
                self.rotate_piece(self.current_piece)
                return 1                                  
        return super().eventFilter(obj, event)

    def init_game(self):            
        self.update_board()

    def play_game(self):
        # main game loop
        
        if self.current_piece is None:
            self.current_piece = self.get_piece()
            self.next_piece = self.get_piece()
            self.update_board()
            self.draw_piece(self.current_piece) 
        if self.current_piece.locked:
            self.current_piece =  self.next_piece
            self.next_piece = self.get_piece()
            self.update_board()
            self.draw_piece(self.current_piece)              
        print("game")
