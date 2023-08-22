import pygame as py
from .constants import *
import os

class Piece:
    def __init__(self, row, col, color : str, name : str, value : float):
        self.x = row*SQ_SIZE
        self.y = col*SQ_SIZE
        self.color = color
        self.name = name
        self.value = value
        self.img = self.get_img()
        self.pos = self.calc_pos()

    def calc_pos(self):
        """Returns row and col of piece"""
        self.pos = (self.x//SQ_SIZE, self.y//SQ_SIZE)
        return self.pos
    
    def get_img(self):
        img = py.image.load(os.path.join('Assets', f'{self.name}_{self.color}45.png'))
        transformed_img = py.transform.smoothscale(img, (HEIGHT//ROWS, WIDTH//COLS))
        return transformed_img

class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, 'pawn', 1.)

class King(Piece):
    def __init__(self,  row, col, color):
        super().__init__( row, col, color, 'king', 10000.)

class Queen(Piece):
    def __init__(self, row, col, color):
        super().__init__( row, col, color, 'queen', 9.)


class Rook(Piece):
    def __init__(self,  row, col, color):
        super().__init__( row, col, color, 'rook', 5.)

class Bishop(Piece):
    def __init__(self,  row, col, color):
        super().__init__( row, col, color, 'bishop', 3.1)


class Knight(Piece):
    def __init__(self,  row, col, color):
        super().__init__( row, col, color, 'knight', 3.)