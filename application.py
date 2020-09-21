import random
from modules import cmd
import time
from threading import Thread
import sys
from subprocess import Popen,CREATE_NEW_CONSOLE,PIPE
import keyboard

class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = {}

        cmd.Window.clear()
        for x in range(self.columns):
            for y in range(self.rows):
                self.board[x, y] = '.'

    def draw(self):
        cmd.Window.clear()
        board = f'{cmd.Color.random()}WELCOME  TO  TETRIS{cmd.Color.reset}\
        \n{cmd.Color.random()}CRE: OLAV A. ONSTAD{cmd.Color.reset}\n'
        for index, (key, value) in enumerate(self.board.items()):
            if(index % 10 == 0):
                board += '\n'

            board += f'{value} '

        print(board, file=sys.stdout.flush())


    def findDict(self, point: list()):
        pass

class piece:
    def __init__(self, grid, gm):
        self.symbol = '■'
        self.symbol_colored = cmd.Color.random() + self.symbol + cmd.Color.reset
        self.directions = {'down':[1, 0], 'left':[0, -1], 'right':[0, 1]}
        self.grid = grid
        self.pieces = [
            [(0,0),(0,1),(0,2),(0,3)],
            [(0,0),(0,1),(1,0),(1,1)],
            [(1,0),(0,1),(1,1),(1,2)],
            [(0,0),(0,1),(1,0),(2,0)],
            [(0,0),(0,1),(1,1),(2,1)],
            [(0,1),(1,0),(1,1),(2,0)]
        ]
        self.piece = random.choice(self.pieces)
        self.stationary = False

    def update(self):

        self.clear()
        for key, value in self.grid.board.items():
            for point in self.piece:
                if(point == key):
                    self.grid.board[key] = self.symbol_colored

    def clear(self):
        for key, value in self.grid.board.items():
            for point in self.piece:
                if(point == key):
                    self.grid.board[key] = '.'

    def move(self, direction):
        self.clear()
        piece = list()

        for index, point in enumerate(self.piece):
            point = (point[0] + direction[0], point[1] + direction[1])
            piece.append(point)

        if(self._isLegal(piece)[0]):
            self.piece = piece
        elif(self._isLegal(piece)[1]):
            self.stationary = True
            gm.add_blocks(piece)


        self.update()

    def _isLegal(self, piece: list()):
        for index, (key, value) in enumerate(self.grid.board.items()):
            for point in piece:
                if(point[0] >= self.grid.columns):
                    return False, True

                #WILL BE STATIONARY IF IT LOCKS FROM THE SIDE
                if point not in self.grid.board:
                    return False, False
                elif('■' in self.grid.board[point]):
                    return False, True
        return True, False

    def get_piece_dimensions(self):
        max_r = max_c = 0
        for point in self.piece:
            max_r = max(max_r, point[0])
            max_c = max(max_c, point[1])
        return max_r, max_c

    def rotate_piece(self):
        max_r, max_c = self.get_piece_dimensions()
        new_piece = []
        for r in range(max_r+1):
            for c in range(max_c+1):
                if (r,c) in self.piece:
                    new_piece.append((c, max_r-r))
        self.clear()
        self.piece = new_piece
        self.update()

class GameManager:
    def __init__(self):
        self.pieces = list()
        self.blocks = list(list())

    def add_blocks(self, piece):
        for block in piece:
            self.blocks.append(block)

#GLOBAL VARIABLES / OBJECTS
gm = GameManager()
grid = Grid(10, 20)

direction = 'none'
rotate = False
speed = 0.5



def gameLoop():
    global direction, rotate, speed
    while True:
        if(len(gm.pieces) > 0):
            if(gm.pieces[-1].stationary):
                gm.pieces.append(piece(grid, gm))
        else:
            gm.pieces.append(piece(grid, gm))

        if(rotate):
            gm.pieces[-1].rotate_piece()
        gm.pieces[-1].move(gm.pieces[-1].directions[random.choice(['down'])])

        if(direction != 'none'):
            gm.pieces[-1].move(gm.pieces[-1].directions[random.choice([direction])])

        grid.draw()
        direction = 'none'
        rotate = False
        time.sleep(speed)

def keyboardInput():
    global direction, rotate, speed
    while True:
        if(keyboard.is_pressed('a')):
            direction = 'left'
        elif(keyboard.is_pressed('d')):
            direction = 'right'
        elif(keyboard.is_pressed('r')):
            rotate = True

        if(keyboard.is_pressed('s')):
            speed = 0.1
        elif(keyboard.is_pressed('w')):
            speed = 0.8
        else:
            speed = 0.4

        time.sleep(0.05)

def main():
    Thread(target=gameLoop).start()
    Thread(target=keyboardInput).start()

if __name__ == '__main__':
    main()
