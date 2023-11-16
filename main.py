import pygame as py
from chess.board import Board
from chess.constants import *
from chess.pieces import *
from chess.game import Game, Move



def draw_gamestate(game, screen, sq_selected):
      game.show_bg(screen)
      game.show_pieces(screen)

      if sq_selected:
        row, col = sq_selected
        highlight_rect = py.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        py.draw.rect(screen, py.Color('Yellow'), highlight_rect, 4)

def get_promotion_choice(screen):
    font = py.font.Font(None, 24)
    text = font.render("Choose promotion (Q for Queen, R for Rook, B for Bishop, N for Knight)", True, py.Color('White'))
    
    # Create a surface with a black border
    text_with_border = py.Surface((text.get_width() + 2, text.get_height() + 2))
    text_with_border.fill(py.Color('Black'))
    text_with_border.blit(text, (1, 1))
    
    # Center the bordered text on the screen
    text_rect = text_with_border.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    screen.blit(text_with_border, text_rect)
    py.display.flip()

    while True:
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.unicode.lower() in ['q', 'r', 'b', 'n']:
                    return event.unicode.lower()


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
   moves = game.get_valid_moves()
   move_made = False

   while run:
      for event in py.event.get():
            if event.type == py.QUIT:
               run = False
            
            # mouse clicks
            elif event.type == py.MOUSEBUTTONDOWN:
               pos = py.mouse.get_pos()
               row, col = pos[1]//SQ_SIZE, pos[0]//SQ_SIZE # (i, j) of clicked square.
               if sq_selected == (row, col): 
                  sq_selected = () # deselect
                  player_clicked = [] # clear click-queue
               else:
                  sq_selected = (row, col)
                  player_clicked.append(sq_selected)
                  if len(player_clicked) == 2:
                     move = Move(player_clicked[0], player_clicked[1], game.board.array)
                     for i in range(len(moves)):
                        if move == moves[i]:
                           if moves[i].pawn_promotion:
                              choice = get_promotion_choice(screen)
                              promote_to = {'q': Queen, 'r': Rook, 'b': Bishop, 'n': Knight}[choice]
                              game.make_move(moves[i], promote_to=promote_to(moves[i].f_row, moves[i].f_col,
                                                                                    ("w" if game.white_to_move else "b")))                           
                           else:
                              game.make_move(moves[i])
                           move_made = True
                           player_clicked = []
                           sq_selected = ()
                     if not move_made:
                        player_clicked = [sq_selected] # invalid moves, move your click to the invalid square
               
               # undo press
            elif event.type == py.KEYDOWN:
               if event.key == py.K_LEFT:
                  game.undo_move()
                  move_made = True



            if move_made:
                moves = game.get_valid_moves()
                move_made = False
                     
      clock.tick(FPS) #sets tickrate to 60
      py.display.update()
      draw_gamestate(game, screen, sq_selected)


   py.quit()

if __name__ == "__main__":
   main()