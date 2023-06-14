import pygame as py
import os
from .constants import WIDTH, HEIGHT, ROWS, COLS, SQ_SIZE

##### PIECE IMG LOADING #####

### Black Pieces ###

#White King
B_KING_IMG = py.image.load(os.path.join('Assets', 'Chess_kdt45.png'))
B_KING = py.transform.smoothscale(B_KING_IMG, (HEIGHT//ROWS, WIDTH//COLS))

#Black Queen
B_QUEEN_IMG = py.image.load(os.path.join('Assets', 'Chess_qdt45.png'))
B_QUEEN = py.transform.smoothscale(B_QUEEN_IMG, (HEIGHT//ROWS, WIDTH//COLS))

#Black Bishop
B_BISHOP_IMG = py.image.load(os.path.join('Assets', 'Chess_bdt45.png'))
B_BISHOP = py.transform.smoothscale(B_BISHOP_IMG, (HEIGHT//ROWS, WIDTH//COLS))

#White Rook
B_ROOK_IMG = py.image.load(os.path.join('Assets', 'Chess_rdt45.png'))
B_ROOK = py.transform.smoothscale(B_ROOK_IMG, (HEIGHT//ROWS, WIDTH//COLS))

#White Knight
B_KNIGHT_IMG = py.image.load(os.path.join('Assets', 'Chess_ndt45.png'))
B_KNIGHT = py.transform.smoothscale(B_KNIGHT_IMG, (HEIGHT//ROWS, WIDTH//COLS))

#White Pawn
B_PAWN_IMG = py.image.load(os.path.join('Assets', 'Chess_pdt45.png'))
B_PAWN = py.transform.smoothscale(B_PAWN_IMG, (HEIGHT//ROWS, WIDTH//COLS))

### White Pieces ###

#White King
W_KING_IMG = py.image.load(os.path.join('Assets', 'Chess_klt45.png'))
W_KING = py.transform.smoothscale(W_KING_IMG, (HEIGHT//ROWS, WIDTH//COLS))

#White Queen
W_QUEEN_IMG = py.image.load(os.path.join('Assets', 'Chess_qlt45.png'))
W_QUEEN = py.transform.smoothscale(W_QUEEN_IMG, (HEIGHT//ROWS, WIDTH//COLS))

#White Rook
W_ROOK_IMG = py.image.load(os.path.join('Assets', 'Chess_rlt45.png'))
W_ROOK = py.transform.smoothscale(W_ROOK_IMG, (HEIGHT//ROWS, WIDTH//COLS))

#White Bishop
W_BISHOP_IMG = py.image.load(os.path.join('Assets', 'Chess_blt45.png'))
W_BISHOP = py.transform.smoothscale(W_BISHOP_IMG, (HEIGHT//ROWS, WIDTH//COLS))

#White Knight
W_KNIGHT_IMG = py.image.load(os.path.join('Assets', 'Chess_nlt45.png'))
W_KNIGHT = py.transform.smoothscale(W_KNIGHT_IMG, (HEIGHT//ROWS, WIDTH//COLS))

#White Pawn
W_PAWN_IMG = py.image.load(os.path.join('Assets', 'Chess_plt45.png'))
W_PAWN = py.transform.smoothscale(W_PAWN_IMG, (HEIGHT//ROWS, WIDTH//COLS))