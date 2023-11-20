import pygame

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