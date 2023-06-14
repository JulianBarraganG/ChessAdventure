import pygame as py
from .constants import *
from .images import *

class Piece:
    def __init__(self, row, col, color):
        self.x = row
        self.y = col
        self.color = color

    def calc_pos(self):
        self.pos = (self.x, self.y)
        print(self.pos)

class Pawn(Piece):
    def __init__(self):
        super().__init__(0, 0, 'w')
