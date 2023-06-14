import pygame as py
#import os
from chess.board import board
#from svglib.svglib import svg2rlg # import svg2rlg function from svglib
#from reportlab.graphics import renderPM # import renderPM function from reportlab.graphics
from chess.constants import *
from chess.images import *
from chess.pieces import *

WIN = py.display.set_mode((WIDTH, HEIGHT))
BOARD = board(WIN)

a = Pawn()

print(a.calc_pos())

py.display.set_caption("Chess")

def draw_window():
   WIN.fill(WHITE)
   board(WIN)
#    for i in range(ROWS): 
#     for j in range(COLS):
#         if j == 6:
#             WIN.blit(W_PAWN, (i*SQ_SIZE, j*SQ_SIZE))
#         elif j == 1:
#             WIN.blit(B_PAWN, (i*SQ_SIZE, j*SQ_SIZE))
   py.display.update()


def main():
   clock = py.time.Clock()
   run = True
   while run:

       clock.tick(FPS) #sets tickrate to 60
       for event in py.event.get():
           if event.type == py.QUIT:
               run = False
       
       draw_window()


   py.quit()

if __name__ == "__main__":
   main()