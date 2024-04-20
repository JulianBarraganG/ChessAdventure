import pygame as py
import os

#### CANVAS CONSTANTS ####
WIDTH, HEIGHT = 760, 760 #The size of the canvas
FPS = 60
ROWS = COLS = 8
SQ_SIZE = WIDTH // COLS # 800 // 8 = 100. The square size of a square in pixels.


#### COLORS FOR SQUARES ####
LBROWN = (189, 145, 104, 10) # RGB code: #BD9168
WHITE = (255, 250, 205, 10) # RGB code: #FFFACD Lemonchiffon
TURQUOISE = (104, 189, 188, 10) #RGB code: #68BDBC Cyan

#### SET COLORS HERE ####
DSQ = LBROWN
LSQ = WHITE

##### STARTING FEN POS #####
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"

##### BOARD DIRECTIONS ####
ALL_DIR = ((-1, 0), # up
           (1, 0), # down
           (0, 1), # right
           (0, -1), # left
           (1, -1), # down left
           (1, 1), # down right
           (-1, -1), # up left
           (-1, 1) # up right
           )

# For constructing PGN notation
ROW_TO_RANK = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
COL_TO_FILE = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

# Inverse dictionaries
RANK_TO_ROW = {v: k for k, v in ROW_TO_RANK.items()}
FILE_TO_COL = {v: k for k, v in COL_TO_FILE.items()}

# Constants for pieces
EMPTY, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = 0, 1, 2, 3, 4, 5, 6
W, B = 16, 8  # Using 8 for BLACK as it will set the fourth bit to 1

# Mapping str to pieces
STR2PIECE_MAPPING = {
    'p': PAWN,
    'k': KING,
    'q': QUEEN,
    'r': ROOK,
    'b': BISHOP,
    'n': KNIGHT,
}

# Mapping pieces to strings
PIECE2STRING_MAPPING = {
    PAWN+W: 'P',
    PAWN+B: 'p',
    KNIGHT+W: 'N',
    KNIGHT+B: 'n',
    KING+W: 'K',
    KING+B: 'k',
    BISHOP+W: 'B',
    BISHOP+B: 'b',
    ROOK+W: 'R',
    ROOK+B: 'r',
    QUEEN+W: 'Q',
    QUEEN+B: 'q',
}

PIECE_NAMES = {
    PAWN: 'pawn',
    KING: 'king',
    KNIGHT: 'knight',
    BISHOP: 'bishop',
    QUEEN: 'queen',
    ROOK: 'rook'
}

def preload_images():
    images = {}
    # Load images for white pieces
    for piece, name in PIECE_NAMES.items():
        images[piece + W] = load_image(name, 'w')

    # Load images for black pieces
    for piece, name in PIECE_NAMES.items():
        images[piece + B] = load_image(name, 'b')

    return images

def load_image(piece_name, color):
    img = py.image.load(os.path.join('Assets', f'{piece_name}_{color}45.png'))
    transformed_img = py.transform.smoothscale(img, (SQ_SIZE, SQ_SIZE))
    return transformed_img