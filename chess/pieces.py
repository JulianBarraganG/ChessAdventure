import pygame as py
from .constants import *
import os

class Piece:
    def __init__(self, color : str, name : str, value : float):
        self.color = color
        self.name = name
        self.value = value
        self.img = self.get_img()
    
    def get_img(self):
        img = py.image.load(os.path.join('Assets', f'{self.name}_{self.color}45.png'))
        transformed_img = py.transform.smoothscale(img, (HEIGHT//ROWS, WIDTH//COLS))
        return transformed_img

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'pawn', 10)

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'king', 0)

class Queen(Piece):
    def __init__(self,color):
        super().__init__(color, 'queen', 90)


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'rook', 50)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'bishop', 31)


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'knight', 3)