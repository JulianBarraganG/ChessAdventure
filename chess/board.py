import pygame as py
import numpy as np
from .constants import *
from .pieces import *


class Board:
    """
    Contains array of board as well as methods to modify said array,
    before projecting to images via the Game class.
    """

    def __init__(self):
        self.array = [[None]*COLS for _ in range(ROWS)]

    def _start_pos(self, color):
        """
        Adds either black or white pieces to initial positions.
        """
        pawn_row, piece_row = (6, 7) if color == 'w' else (1, 0)

        # Add pawns to array
        for j in range(COLS):
            self.array[pawn_row][j]= Pawn(pawn_row, j, color)

        # Add pieces to array
        self.array[piece_row][0] = Rook(piece_row, 0, color)
        self.array[piece_row][7] = Rook(piece_row, 7, color)

        self.array[piece_row][1] = Knight(piece_row, 1, color)
        self.array[piece_row][6] = Knight(piece_row, 6, color)

        self.array[piece_row][2] = Bishop(piece_row, 2, color)
        self.array[piece_row][5] = Bishop(piece_row, 5, color)

        self.array[piece_row][3] = Queen(piece_row, 3, color)

        self.array[piece_row][4] = King(piece_row, 4, color)

    def reset_board(self):
        self.array = [[None]*COLS for _ in range(ROWS)] # clears the board.
        self._start_pos('w')
        self._start_pos('b')

    def fen_reader(self, fen):
        """
        Takes a fen string and converts the position into array form.
        Modifies the array of the board class.
        """
        self.array = [[None] * COLS for _ in range(ROWS)]  # clears the board.
        row = 0
        col = 0
    
        piece_mapping = {
            'p': Pawn,
            'k': King,
            'q': Queen,
            'r': Rook,
            'b': Bishop,
            'n': Knight,
        }
    
        for char in fen:
            if char.isdigit():
                col += int(char)
            elif char.lower() in piece_mapping:
                piece_class = piece_mapping[char.lower()]
                color = 'w' if char.isupper() else 'b'
                self.array[row][col] = piece_class(row, col, color)
                col += 1
            elif char == '/':
                row += 1
                col = 0
            elif char.isspace():
                break
            