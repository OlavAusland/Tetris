import random
from modules import cmd
import time

class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = {}

        cmd.Window.clear()
        for x in range(self.columns):
            for y in range(self.rows):
                self.board[x, y] = '.'
                if(x == 9):
                    self.board[x, y] = '#'

    def draw(self):
        cmd.Window.clear()
        for index, (key, value) in enumerate(self.board.items()):
            if(index % 10 == 0):
                print()

            print(value, end=" ")


    def findDict(self, point: list()):
        pass

class Shape():
    def __init__(self, grid):
        self.directions = {'down':[1, 0], 'left':[0, -1], 'right':[0, 1]}
        self.grid = grid
        self.start_x = 0
        self.start_y = 0
        self.shapes = [
            [
                (0, 0),
                (0, 1),
                (0 + 1, 0),
                (0 + 1, 1)
            ],
            [
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3)
            ],
            [
                (0, 1),
                (1, 0),
                (1, 1),
                (1, 2)
            ],
            [
                (0, 1),
                (0, 2),
                (1, 0),
                (1, 1)
            ],
            [
                (0, 0),
                (0, 1),
                (1, 1),
                (1, 2)
            ],
            [
                (0, 0),
                (1, 0),
                (1, 1),
                (1, 2)
            ],
            [
                (1, 0),
                (1, 1),
                (1, 2),
                (0, 2)
            ]
        ]
        self.shape = random.choice(self.shapes)
        self.test = 1

    def update(self):

        self.clear()
        for key, value in self.grid.board.items():
            for point in self.shape:
                if(point == key):
                    self.grid.board[key] = '#'


    def clear(self):
        for key, value in self.grid.board.items():
            for point in self.shape:
                if(point == key):
                    self.grid.board[key] = '.'

    def move(self, direction):
        self.clear()
        shape = list()

        for index, point in enumerate(self.shape):
            point = (point[0] + direction[0], point[1] + direction[1])
            shape.append(point)

        if(self._isLegal(shape)):
            self.shape = shape

            self.update()

    def _isLegal(self, shape: list()):
        for index, (key, value) in enumerate(self.grid.board.items()):
            for point in self.shape:
                if(self.grid.board[point] == '#'):
                    return False
        return True


grid = Grid(10, 20)
shape = Shape(grid)

for index in range(19):
    shape.move(shape.directions['down'])
    grid.draw()
    time.sleep(0.1)
