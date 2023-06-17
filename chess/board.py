import pygame as py
import numpy as np
from .constants import *
from .pieces import *
#from functions import *


class Board:
    """
    Contains array of board as well as methods to modify said array,
    before projecting to images via the Game class.
    """
    
    def __init__(self):
        self.array = np.array([[None]*8]*8)
        self._reset_board('w')
        self._reset_board('b')

    def _reset_board(self, color):
        pawn_row, piece_row = (6, 7) if color == 'w' else (1, 0)

        # Add pawns to array
        for j in range(COLS):
            # when indexing array, [j, i] since each list is a row, we first index which list then which col.
            self.array[j, pawn_row] = Pawn(pawn_row, j, color)

        # Add pieces to array
        self.array[0, piece_row] = Rook(piece_row, 0, color)
        self.array[7, piece_row] = Rook(piece_row, 7, color)

        self.array[1, piece_row] = Knight(piece_row, 1, color)
        self.array[6, piece_row] = Knight(piece_row, 6, color)

        self.array[2, piece_row] = Bishop(piece_row, 2, color)
        self.array[5, piece_row] = Bishop(piece_row, 5, color)

        self.array[3, piece_row] = Queen(piece_row, 3, color)

        self.array[4, piece_row] = King(piece_row, 4, color)

    def fen_reader(self, fen):
        self.array = np.array([[None]*8]*8) # reset array
        row = 0
        col = 0
        for char in fen:
            if char.isdigit():
                col += int(char)
            elif char == 'P':
                self.array[col, row] = Pawn(row, col, 'w')
                col += 1
            elif char == 'p':
                self.array[col, row] = Pawn(row, col, 'b')
                col += 1
            elif char == 'K':
                self.array[col, row] = King(row, col, 'w')
                col += 1
            elif char == 'k':
                self.array[col, row] = King(row, col, 'b')
                col += 1
            elif char == 'Q':
                self.array[col, row] = Queen(row, col, 'w')
                col += 1
            elif char == 'q':
                self.array[col, row] = Queen(row, col, 'b')
                col += 1
            elif char == 'R':
                self.array[col, row] = Rook(row, col, 'w')
                col += 1
            elif char == 'r':
                self.array[col, row] = Rook(row, col, 'b')
                col += 1
            elif char == 'B':
                self.array[col, row] = Bishop(row, col, 'w')
                col += 1
            elif char == 'b':
                self.array[col, row] = Bishop(row, col, 'b')
                col += 1
            elif char == 'N':
                self.array[col, row] = Knight(row, col, 'w')
                col += 1
            elif char == 'n':
                self.array[col, row] = Knight(row, col, 'b')
                col += 1
            elif char == '/':
                row += 1
                col = 0
            elif char.isspace(): 
                break
