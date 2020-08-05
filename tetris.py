from PyQt5.QtWidgets import QStackedWidget, QWidget, QPushButton, \
                            QGridLayout, QVBoxLayout, QHBoxLayout, \
                            QLabel, QTableWidget, QTableWidgetItem
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.Qt import Qt, QTimer

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
             [(0, 1), (0, 0), (1, 0), (1, -1)]]

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
        # check if piece_pos has been exceeded
        if self.piece_pos >= len(self.shapes[self.piece_num]):
            self.piece_pos = 0

    def get_coords(self):
        self.check_pos()    
        return self.shapes[self.piece_num][self.piece_pos]

    def get_top_y(self):
        return min([y for x,y in self.get_coords()])


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
        # Tetris layout parameters          
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
        QtWidgets.qApp.installEventFilter(self)

        # Tetris parameters
        self.board = [[Cube() for j in range(20)] for i in range(10)]
        self.current_piece = None
        self.next_piece = None

        self.update_board()                            
        self.play_game()
        self.vbox.addWidget(self.tetrisbox)

    def init_game(self):
        self.current_piece = self.get_piece()
        self.next_piece = self.get_piece()
        self.update_board()
        self.draw_piece() 

    def play_game(self):
        # main game loop          
        self.init_game()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.game_cycle)
        self.timer.start()                      
                               
    def game_cycle(self):                

        if self.game_over():
            print("Game Over!")
            return

        if self.current_piece.locked:
            print("Next one pls!")
            self.current_piece =  self.next_piece
            self.next_piece = self.get_piece()
            print(self.current_piece.x, self.current_piece.y)
            self.update_board()
            self.draw_piece()
            return

        self.go_down()

    def game_over(self):
        if self.check_lock() and self.current_piece.y == 0:
            return True
        return False

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

    def draw_piece(self):
        # method adds piece to the board  
        if self.current_piece is None:
            return      
        x, y = 0, 1      
        # fix top position     
        top_y =  self.current_piece.y + self.current_piece.get_top_y()                      
        if top_y < 0:
            if not self.check_lock():
                self.current_piece.y += abs(top_y)
        # draw piece
        for coords in self.current_piece.get_coords():            
            new_x = self.current_piece.x + coords[x]
            new_y =  self.current_piece.y + coords[y]            
            if (0 <= new_y < len(self.board[0])) and (0 <= new_x < len(self.board)):
                self.board[new_x][new_y].update(self.current_piece.color)  

    def check_lock(self):
        if self.current_piece is None:
            return
        x, y = 0, 1
        for coords in self.current_piece.get_coords():            
            _x = self.current_piece.x + coords[x]
            _y = self.current_piece.y + coords[y]            
            if _y == len(self.board[0])-1:
                return True
            if self.board[_x][_y+1].locked:
                return True            
        return False

    def lock_piece(self):
        if self.current_piece is None:
            return
        x, y = 0, 1
        for coords in self.current_piece.get_coords():            
            _x = self.current_piece.x + coords[x]
            _y = self.current_piece.y + coords[y]
            self.board[_x][_y].locked = True
        self.current_piece.locked = True

    def try_move(self, dx=0, dy=0): 
        x, y = 0, 1
        if self.current_piece is None:
            return False        
    
        for coords in self.current_piece.get_coords():            
            new_x = self.current_piece.x + coords[x] + dx
            new_y = self.current_piece.y + coords[y] + dy
            if not (0 <= new_y < len(self.board[0])):
                return False
            if not (0 <= new_x < len(self.board)):
                return False
            if self.board[new_x][new_y].locked:
                return False      

        return True

    def move_piece(self, dx=0, dy=0):
        if self.current_piece is None:
            return
        if self.current_piece.locked:
            return
        if self.try_move(dx=dx, dy=dy):
            self.current_piece.y += dy
            self.current_piece.x += dx
            self.update_board()        
            self.draw_piece()
            if self.check_lock():
                self.lock_piece()

    def try_rotate(self):
        if self.current_piece is None:
            return
        if self.current_piece.locked:
            return
        prev_pos = self.current_piece.piece_pos
        self.current_piece.piece_pos += 1
        if not self.try_move():
            self.current_piece.piece_pos = prev_pos
            return False
        return True
     
    def rotate_piece(self):
        if self.current_piece is None:
            return
        if self.try_rotate():            
            self.update_board()        
            self.draw_piece()
            if self.check_lock():
                self.lock_piece()

    def go_down(self):
        self.move_piece(dy=1)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:                    
            key = event.key()
            if key == Qt.Key_Left:
                self.move_piece(dx=-1)
                return 1
            if key == Qt.Key_Right:
                self.move_piece(dx=1)
                return 1            
            if key == Qt.Key_Down:
                self.move_piece(dy=1)
                return 1  
            if key == Qt.Key_Up:
                self.rotate_piece()
                return 1                                  
        return super().eventFilter(obj, event)

