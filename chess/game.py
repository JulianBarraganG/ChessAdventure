import pygame as py
from .board import Board
from .constants import ROWS, COLS, DSQ, LSQ, SQ_SIZE

class Game:
    """
    This class oversees the game, 
    prints all methods, handles visualisation and more.
    Game is the frontmost class
    """

    def __init__(self):
        self.next_player = 'w'
        self.board = Board()
        self.board.reset_board()
        self.move_log = []
        self.white_to_move = True

    # Draw the squares in background
    def show_bg(self, screen):
        for i in range(ROWS):
            for j in range(COLS):
                if (j+i) % 2 == 0:
                    py.draw.rect(screen, DSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                else:
                    py.draw.rect(screen, LSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    def show_pieces(self, screen):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board.array[i][j]:
                    screen.blit(self.board.array[i][j].img, py.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    def make_move(self, move):
        self.board.array[move.i_row][move.i_col] = None
        self.board.array[move.f_row][move.f_col] = move.moved_piece
        self.move_log.append(move) 
        self.white_to_move = not self.white_to_move # Swap turns

class Move():
    def __init__(self, init_pos, final_pos, array):
        self.i_row = init_pos[0]
        self.i_col = init_pos[1]
        self.f_row = final_pos[0]
        self.f_col = final_pos[1]
        self.moved_piece = array[self.i_row][self.i_col]
        self.captured_piece = array[self.f_row][self.f_col]