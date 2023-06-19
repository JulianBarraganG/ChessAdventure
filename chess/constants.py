import pygame

#### CANVAS CONSTANTS ####
WIDTH, HEIGHT = 600, 600 #The size of the canvas
FPS = 60
ROWS = COLS = 8
SQ_SIZE = WIDTH // COLS # 800 // 8 = 100. The square size of a square in pixels.


#### COLORS FOR SQUARES ####
LBROWN = (189, 145, 104, 10) # RGB code: #BD9168
WHITE = (255, 250, 205, 10) # RGB code: #FFFACD Lemonchiffon
TURQUOISE = (104, 189, 188, 10) #RGB code: #68BDBC Cyan

#### SET COLORS HERE ####
DSQ = TURQUOISE
LSQ = WHITE

##### STARTING FEN POS #####
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"