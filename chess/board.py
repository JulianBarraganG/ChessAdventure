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

    def board_to_fen(self):
        """
        Iterates through the array (Board) and returns fen position.
        """
        board = self.array
        fen_position = ""
        piece_mapping = {
            'pawn' : 'p',
            'king' : 'k',
            'queen' : 'q',
            'rook' : 'r',
            'bishop' : 'b',
            'knight' : 'n'
        }

        for i in range(ROWS):
            empty_squares = 0
            for j in range(COLS):
                if board[i][j]:
                    fen_position += piece_mapping[board[i][j].name] if board[i][j].color == "b" else piece_mapping[board[i][j].name].upper()
                elif not board[i][j]:
                    while not board[i][j]:
                        empty_squares += 1
                        if board[i][j + 1 if j + 1 < COLS else j]:
                            fen_position += str(empty_squares)
                            empty_squares = 0
                        elif j == COLS - 1:
                            fen_position += str(empty_squares)
                            empty_squares = 0
                            break
                        break
            if i < ROWS - 1:
                fen_position += "/"
        return fen_position