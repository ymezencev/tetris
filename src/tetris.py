from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QVBoxLayout, \
                            QLabel, QTableWidget, QTableWidgetItem

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
                self.scores_tbl.setItem(row_num, column_num, 
                                        QTableWidgetItem(str(data)))        


class Cube(QPushButton):
    # tetris grid consists of 20x10 cubes
    def __init__(self, color='#fff'):
        super().__init__()           
        self.color = color
        self.locked = False
        self.setFixedSize(QtCore.QSize(40, 40))
        self.set_color(self.color)        

    def set_color(self, color="#fff"):        
        if not self.locked:
            self.color = color
            self.setStyleSheet(f'background: {self.color};')

    def clear(self):
        self.set_color()


class Piece:
    # one piece consists of several colored cubes    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.randint(0,6)
        self.position = 0
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

        self.all_shapes = [O, I, S, Z, L, J, T]
        colors = ['blue', 'red', 'yellow', 'green', 'pink', 'orange', 'brown']

        self.color = colors[self.shape]

    def move_next_pos(self):
        # checks if piece_pos has been exceeded
        self.position += 1
        if self.position >= len(self.all_shapes[self.shape]):
            self.position = 0        

    def get_coords(self):
        return self.all_shapes[self.shape][self.position]

    def get_absolute_coords(self):        
        abs_coords = []
        for coords in self.get_coords():
            abs_x, abs_y = self.x + coords[0], self.y + coords[1]
            # we dont get cubes positions above the board, 
            # so we can rotate and move piece on top
            if abs_y >= 0:
                abs_coords.append((abs_x, abs_y))
        return abs_coords


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

        # Tetris game parameters
        self.score = 0
        self.speed = 1000
        self.level = 1        

        self.row_len = 10
        self.col_len = 20
        self.board = [[Cube() for i in range(self.row_len)] 
                                  for j in range(self.col_len)]                    

        self.timer = QTimer(self)        
        self.timer.timeout.connect(self.game_loop)
        self.next_level()

        self.current_piece = self.get_piece()
        self.next_piece = self.get_piece()                
        
        self.clear_board()
        self.draw_piece()
        self.vbox.addWidget(self.tetrisbox)
    
    def next_level(self):
        self.level *= 2
        self.time = self.speed / self.level
        self.timer.setInterval(self.time)
        self.timer.start()


    def game_loop(self):        
        # main game loop                       

        if self.game_over():
            print("Game Over!")
            return        

        if self.current_piece.locked:
            if self.try_remove_lines():
                self.next_level()
            self.current_piece =  self.next_piece
            self.next_piece = self.get_piece()
            self.draw_piece() 
            return
                
        self.fall_piece()
                             
    def clear_board(self):
        # clear not locked cubes  
        for row_num, row_cubes in enumerate(self.board):
            for col_num, col_cube in enumerate(row_cubes):
                self.grid.removeWidget(col_cube)                
                col_cube.clear()
                self.grid.addWidget(col_cube, row_num, col_num) 

    def get_piece(self):
        # get random piece              
        start_pos = (round(self.row_len/2), 0)
        return Piece(*start_pos)        

    def draw_piece(self):
        self.clear_board()
        # method adds piece to the board  
        if self.current_piece is None:
            return      
        for coords in self.current_piece.get_absolute_coords():
            _x, _y = coords
            if self.check_out_conditions(x=_x, y=_y):                
                self.board[_y][_x].set_color(self.current_piece.color) 

    def move_piece(self, dx=0, dy=0):
        if self.current_piece is None:
            return
        if self.current_piece.locked:
            return        
        if self.try_move(dx=dx, dy=dy):            
            self.current_piece.y += dy
            self.current_piece.x += dx
            self.clear_board()        
            self.draw_piece()
            self.try_lock_piece()


    def rotate_piece(self):
        if self.current_piece is None:
            return
        if self.try_rotate():            
            self.clear_board()        
            self.draw_piece()
            self.try_lock_piece()

    def fall_piece(self):
        self.move_piece(dy=1)

    def try_lock_piece(self):
        if self.check_lock_conditions():
            for coords in self.current_piece.get_absolute_coords():
                _x, _y = coords
                self.board[_y][_x].locked = True
            self.current_piece.locked = True     
        return True       

    def try_remove_lines(self):
        for row_num, row in enumerate(self.board):
            if set([col.locked for col in row]) <= {1}:
                for col in row:
                        col.setParent(None)
                del self.board[row_num]
                self.board.insert(0, [Cube() for i in range(self.row_len)])        
                return True
        return False        


    def eventFilter(self, obj, event):        
        if event.type() == QtCore.QEvent.KeyPress:                    
            key = event.key()

            if key == Qt.Key_Left:
                self.move_piece(dx=-1)                
            if key == Qt.Key_Right:
                self.move_piece(dx=1)                
            if key == Qt.Key_Down:
                self.move_piece(dy=1)                
            if key == Qt.Key_Up:
                self.rotate_piece()

            return True 
        return super().eventFilter(obj, event)

    def check_out_conditions(self, x, y):
        # checks if cube coords are out of the board        
        if (y < self.col_len) and (0 <= x < self.row_len):
            return True
        else:
            return False

    def try_move(self, dx=0, dy=0):         
        # check if we can move piece
        if self.current_piece is None:
            return False     

        for coords in self.current_piece.get_absolute_coords():
            _x = coords[0] + dx
            _y = coords[1] + dy
            if not self.check_out_conditions(x=_x, y=_y):
                return False       
            if self.board[_y][_x].locked:                
                return False           
        return True     

    def try_rotate(self):
        # check if we can rotate piece
        if self.current_piece is None:
            return
        if self.current_piece.locked:
            return
        prev_position = self.current_piece.position
        self.current_piece.move_next_pos()
        if not self.try_move():
            self.current_piece.position = prev_position
            return False
        return True   

    def check_lock_conditions(self):
        if self.current_piece is None:
            return      
        for coords in self.current_piece.get_absolute_coords():
            _x, _y = coords

            if _y == self.col_len - 1:
                return True
            if self.board[_y+1][_x].locked:
                return True           
        return False        

    def game_over(self):
        if self.check_lock_conditions() and self.current_piece.y == 0:
            return True
        return False        
