import pygame as py
from chess.board import Board
from chess.constants import *
from chess.pieces import *
from chess.game import Game

SCREEN = py.display.set_mode((WIDTH, HEIGHT))
game = Game()
py.display.set_caption("Chess")

def draw_window():
   py.display.update()
   game._bg(SCREEN)
   game.show_pieces(SCREEN)

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