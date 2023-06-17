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

    # Draw the squares in background
    def _bg(self, screen):
        for i in range(ROWS):
            for j in range(COLS):
                if (j+i) % 2 == 0:
                    py.draw.rect(screen, DSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                else:
                    py.draw.rect(screen, LSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    def show_pieces(self, screen):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board.array[i, j]:
                    screen.blit(self.board.array[i, j].get_img(), self.board.array[i, j].calc_pos())