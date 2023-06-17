import pygame as py
from chess.board import Board
from chess.constants import *
from chess.pieces import *
from chess.game import Game, Move



def draw_gamestate(game, screen):
      game.show_bg(screen)
      game.show_pieces(screen)
                     

def main():
   py.init()
   screen = py.display.set_mode((WIDTH, HEIGHT))
   py.display.set_caption("Chess")
   clock = py.time.Clock()
   screen.fill(py.Color("white"))
   run = True
   game = Game()
   sq_selected = () # tuple of coordinates for selected square.
   player_clicked = [] # list of 

   while run:
      for event in py.event.get():
            if event.type == py.QUIT:
               run = False
            elif event.type == py.MOUSEBUTTONDOWN:
               pos = py.mouse.get_pos()
               row, col = pos[1]//SQ_SIZE, pos[0]//SQ_SIZE # (i,j) of clicked square.
               if sq_selected == (row, col): 
                  sq_selected = () # deselect
                  player_clicked = [] # clear click-queue
               else:
                  sq_selected = (row, col)
                  player_clicked.append(sq_selected)
                  if len(player_clicked) == 2:
                     move = Move(player_clicked[0], player_clicked[1], game.board.array)
                     if game.board.array[move.i_row][move.i_col]:
                        game.make_move(move)
                     player_clicked = []
                     sq_selected = ()
                     
      clock.tick(FPS) #sets tickrate to 60
      py.display.update()
      draw_gamestate(game, screen)


   py.quit()

if __name__ == "__main__":
   main()