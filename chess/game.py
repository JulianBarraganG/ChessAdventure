import pygame as py
from .board import Board
from .constants import ROWS, COLS, DSQ, LSQ, SQ_SIZE, START_FEN, ALL_DIR

class Game:
    """
    This class oversees the game, 
    prints all methods, handles visualisation and more.
    Game is the frontmost class
    """

    def __init__(self):
        self.get_move_functions = {'pawn' : self.get_pawn_moves, 'rook' : self.get_rook_moves, 'knight' : self.get_knight_moves, 
                                   'queen': self.get_queen_moves, 'king': self.get_king_moves, 'bishop': self.get_bishop_moves}
        self.next_player = 'w'
        self.board = Board()
        self.board.reset_board()
        self.move_log = []
        self.white_to_move = True
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.in_check = False
        self.checks = []
        self.pins = []

    ############# DRAWING BLOCK #############
    def show_bg(self, screen):
        for i in range(ROWS):
            for j in range(COLS):
                if (j+i) % 2 == 0:
                    py.draw.rect(screen, LSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                else:
                    py.draw.rect(screen, DSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    def show_pieces(self, screen):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board.array[i][j]:
                    screen.blit(self.board.array[i][j].img, py.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    ############ DRAWING BLOCK END ############

    ########## MOVING BLOCK ###############    
    def make_move(self, move):

        # Update pieces on board and swap turns
        self.board.array[move.i_row][move.i_col] = None
        self.board.array[move.f_row][move.f_col] = move.moved_piece

        # Update move log
        self.move_log.append(move) 

        # Update kin pos
        if move.moved_piece.name == "king":
          if self.white_to_move:
              self.white_king_pos = (move.f_row, move.f_col)
          elif not self.white_to_move:
              self.black_king_pos = (move.f_row, move.f_col)

        # swap turns
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.move_log) == 0:
            return print("No moves to undo")
        else:
            move = self.move_log.pop()
            self.board.array[move.i_row][move.i_col] = move.moved_piece
            self.board.array[move.f_row][move.f_col] = move.captured_piece
            self.white_to_move = not self.white_to_move
    ######## MOVING BLOCK END #############    
    
    ############# CALCULATE LEGAL MOVES BLOCK #############
    def get_valid_moves(self):

        """
        Checks for all valid moves considering checks.
        NB: Check-mate, en-passant and pawn-promotion handled elsewhere.
        """
        board = self.board.array
        self.in_check, self.pins, self.checks = self.checks_and_pins()
        moves = []

        print("in check:", self.in_check)
        print("pins:", self.pins, "checks:", self.checks)

        if self.white_to_move:
            king_row = self.white_king_pos[0]
            king_col = self.white_king_pos[1]
        else:
            king_row = self.black_king_pos[0]
            king_col = self.black_king_pos[1]
                                    
        if self.in_check:
            if len(self.checks) == 1: # 1 piece checking
                the_check = self.checks[0]  # 4-tuple with pos of checking piece and direction.
                if board[the_check[0]][the_check[1]].name != "knight": #if checking piece is not a knight
                    checking_piece_row = the_check[0]
                    checking_piece_col = the_check[1]
                    valid_squares = []
                    for i in range(1, 8):
                        current_row = king_row + the_check[2] * i
                        current_col = king_col + the_check[3] * i
                        if (current_row, current_col) == (checking_piece_row, checking_piece_col):
                            valid_squares.append((current_row, current_col))
                            break
                        else:
                            valid_squares.append((current_row, current_col))
                else: # Knight is only checking piece.
                    valid_squares = [(the_check[0], the_check[1])] # only capturing or moving king.


                moves = self.get_all_moves()
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].moved_piece.name != "king":
                        if (moves[i].f_row, moves[i].f_col) not in valid_squares:
                            moves.remove(moves[i])
                return moves
            
            else: # double check
                print("DOUBLE-CHECK")
                self.get_king_moves(king_row, king_col, moves)
                return moves

        else: # not in check                
            return self.get_all_moves()
        
    def get_all_moves(self):
        moves = []
        for i in range(ROWS):
            for j in range(COLS):
                if self.board.array[i][j]:
                    turn = self.board.array[i][j].color
                else: 
                    continue
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board.array[i][j].name
                    self.get_move_functions[piece](i, j, moves)

        return moves
    
    ############ COMPLEX CHECK ALGORITHM ##################
    def checks_and_pins(self):
        """
        Helper function. Checks for checks and pins.
        """
        
        checks = []
        pins = []
        in_check = False
        board = self.board.array

        # var name for king coordinates of king in question
        k = self.white_king_pos if self.white_to_move else self.black_king_pos
        init_row = k[0]
        init_col = k[1]

        # identity colors for algorithm
        ally = 'w' if self.white_to_move else 'b'
        enemy = 'b' if self.white_to_move else 'w'
        
        ################# KNIGHT CHECKS #####################
        """ Handles the knight checks seperately from all other checks."""
        knight_pattern = (
            (init_row-1, init_col-2),
            (init_row-1, init_col+2),
            (init_row+1, init_col-2),
            (init_row+1, init_col+2),
            (init_row-2, init_col-1),
            (init_row-2, init_col+1),
            (init_row+2, init_col-1),
            (init_row+2, init_col+1)
        )

        for pat in knight_pattern:
            if 0 <= pat[0] <= 7 and 0 <= pat[1] <= 7 and board[pat[0]][pat[1]]:
                potential_knight = board[pat[0]][pat[1]]
                if potential_knight.name == "knight" and potential_knight.color == enemy:
                    in_check = True
                    checks.append((pat[0], pat[1], (pat[0]-init_row), (pat[1]-init_col))) # append knight checks. 
                    #Will uniquely have either row or col dir +-2

        ######################################################



        ############## CHECKS AND PINS ALGORITHM #############
        """ Beams out from the kings position and locates checks and pins for each of the 8 directions. """
        for j in range(len(ALL_DIR)):
            possible_pins = () #reset possible pins
            d = ALL_DIR[j]
            for i in range(1, 8): # start from 1, since 0 incrementation is the kings square itself.
                end_row = init_row + d[0] * i
                end_col = init_col + d[1] * i
                if 0 <= end_row < ROWS and 0 <= end_col < COLS:
                    if self.board.array[end_row][end_col]:
                        end_piece = self.board.array[end_row][end_col]
                        if end_piece.color == ally:
                            if end_piece.name == "king": # "allied king" encounters occur internally in get_king_moves()
                                continue
                            if possible_pins == ():
                                possible_pins = (end_row, end_col, d[0], d[1])
                            else:
                                break # double allied piece, can't be any pin
                        elif end_piece.color == enemy:
                            name = end_piece.name
                            # for all dir 4 possible check-patterns:
                            # 1) orthogonal rook checks
                            # 2) diagonal bishop checks
                            # 3) any dir queen check
                            # 4) pawn checks (1 square away)    
                            if (name == 'rook' and 0 <= j <= 3) \
                                    or (name == 'bishop' and 4 <= j <= 7) \
                                    or (name == 'pawn' and i == 1 and ally == 'w' and (j == 6 or j == 7)) \
                                    or (name == 'pawn' and i == 1 and ally == 'b' and (j == 4 or j == 5)) \
                                    or name == 'queen':

                                if possible_pins == ():
                                    in_check = True
                                    checks.append((end_row, end_col, d[0], d[1]))
                                    break
                                else:
                                    pins.append(possible_pins)
                                    break

                            else:
                                break

                    else:
                        continue

        return in_check, pins, checks
        ############ CHECKS AND PINS ALGORITHM END ###########
    ########### CALCULATE LEGAL MOVES BLOCK END ###########
    

    ############ GET PIECE MOVES FUNCTIONS ############
    def get_king_moves(self, i, j, moves):

        board = self.board.array

        move_pattern = (
            (i-1, j+1), #up right
            (i-1, j-1), #up left
            (i-1, j), #up
            (i, j+1), #right
            (i, j-1), #left
            (i+1, j+1), #down right
            (i+1, j-1), #down left
            (i+1, j), # down
        )

        ally = 'w' if self.white_to_move else 'b' # whites turn

        # filter out moves that move "out of the board"
        possible_moves = tuple(filter(lambda move: move[0] >= 0 and move[0] < (ROWS) and move[1] >= 0 and move[1] < (COLS), move_pattern))
        
        #for every move within board, check if valid.
        for tpl in possible_moves:

            # temp move king pos to see if it enters check
            if ally == 'w':
                self.white_king_pos = tpl
            else:
                self.black_king_pos = tpl
            
            in_check, x, y = self.checks_and_pins()

            if not in_check and (not board[tpl[0]][tpl[1]] or not board[tpl[0]][tpl[1]].color == ally): # safe empty or enemy square.
                moves.append(Move((i, j), (tpl[0], tpl[1]), board))

            # reset king pos
            if ally == 'w':
                self.white_king_pos = (i, j)
            else:
                self.black_king_pos = (i, j)

    def get_pawn_moves(self, i, j, moves):
        """
        Calculates all possible pawn moves, and adds them to the moves list
        """
        board = self.board.array
        enemy = 'b' if self.white_to_move else 'w'
        dir = -1 if self.white_to_move else 1
        start_row = 6 if self.white_to_move else 1
        end_row = 0 if self.white_to_move else 7
        pinned = False
        pin_dir = None
        orthogonal_dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))

        for pin in self.pins:
            if (i, j) == (pin[0], pin[1]):
                pinned = True
                pin_dir = pin[2], pin[3]

        # Extraction of logic
        forward_empty = not board[i + dir][j]
        two_squares_empty = not board[i + 2 * dir][j] and i == start_row # allow for double advance first pawn move.
        left_capture_possible = j > 0 and board[i + dir][j - 1] and board[i + dir][j - 1].color == enemy
        right_capture_possible = j < COLS - 1 and board[i + dir][j + 1] and board[i + dir][j + 1].color == enemy

        if not pinned: # add normal legal moves/captures.
            
            # Add advancing moves
            if forward_empty and (i + dir != end_row):
                moves.append(Move((i, j), (i + dir, j), board))
                if two_squares_empty:
                    moves.append(Move((i, j), (i + 2 * dir, j), board))

            # Add captures
            if left_capture_possible:
                moves.append(Move((i, j), (i + dir, j - 1), board))
            if right_capture_possible:
                moves.append(Move((i, j), (i + dir, j + 1), board))

        elif 0 < j < (COLS - 1): # if pinned and capture stays within board (pinned == True implicit).

            # Logic allowing the capture of pinning piece.
            diagonal_capture_possible = board[i + pin_dir[0]][j + pin_dir[1]] and board[i + pin_dir[0]][j + pin_dir[1]].color == enemy

            if diagonal_capture_possible: 
                moves.append(Move((i, j), (i + pin_dir[0], j + pin_dir[1]), board))

            # No captures available if orthogonally pinned, but advances are:
            elif pin_dir in orthogonal_dirs and forward_empty: 
                moves.append(Move((i, j), (i + dir, j), board))
                if two_squares_empty:
                    moves.append(Move((i, j), (i + 2 * dir, j), board))


        
    def get_knight_moves(self, i, j, moves):
        """
        Calculates all possible knight moves, and adds them to the moves list
        """
        board = self.board.array
        pinned = False
        for pin in self.pins:
            if (i, j) == (pin[0], pin[1]):
                pinned = True

        move_pattern = (
            (i-1, j-2),
            (i-1, j+2),
            (i+1, j-2),
            (i+1, j+2),
            (i-2, j-1),
            (i-2, j+1),
            (i+2, j-1),
            (i+2, j+1)
        )

        ally = 'w' if self.white_to_move else 'b'

        possible_moves = tuple(filter(lambda move: move[0] >= 0 and move[0] < (ROWS) and move[1] >= 0 and move[1] < (COLS), move_pattern))

        if not pinned:
            for tpl in possible_moves:
                if not board[tpl[0]][tpl[1]] or not board[tpl[0]][tpl[1]].color == ally:
                    moves.append(Move((i, j), (tpl[0], tpl[1]), board))
    
    

    # Helper function for generating moves for sliding pieces
    def generate_sliding_moves(self, i, j, moves, dirs):
        """
        The same functionality is used for calculating both rook and bishop moves, except for the directions tuple.
        Helper function reduces redundancy and extracts the calculations.
        """
        board = self.board.array
        pin_dir = None

        # Check if piece at (i, j) is pinned
        for pin in self.pins:
            if (i, j) == (pin[0], pin[1]):
                pin_dir = pin[2], pin[3]

        for dir in dirs:
            if pin_dir and dir != pin_dir and dir != (-pin_dir[0], -pin_dir[1]):
                continue  # skip if pinned
            
            row_dir, col_dir = dir[0], dir[1]
            r, c = i + row_dir, j + col_dir

            # while within the board, add legal moves
            while 0 <= r < ROWS and 0 <= c < COLS:
                if not board[r][c]:
                    moves.append(Move((i, j), (r, c), board))
                elif board[r][c] and board[r][c].color != board[i][j].color:
                    moves.append(Move((i, j), (r, c), board))
                    break
                else:
                    break
                r += row_dir
                c += col_dir


    def get_rook_moves(self, i, j, moves):
        """
        Calculates all possible rook moves, and adds them to the moves list.
        """
        dirs = ((1, 0), (-1, 0), (0, 1), (0, -1)) # orthogonal directions
        self.generate_sliding_moves(i, j, moves, dirs)


    def get_bishop_moves(self, i, j, moves):
        """
        Calculates all possible rook moves, and adds them to the moves list
        """
        dirs = ((1, 1), (-1, -1), (1, -1), (-1, 1)) # diagonal directions
        self.generate_sliding_moves(i, j, moves, dirs)

    def get_queen_moves(self, i, j, moves):
        """
        Calc queen moves.
        """
        self.get_bishop_moves(i, j, moves)
        self.get_rook_moves(i, j, moves)
    ########## GET PIECE MOVES FUNCTIONS END ##########

##########################################################################
############################ NEW CLASS ###################################
class Move():
    """
    Move class handles a chess "move" that a player can make, 
    containing information about initial and end position of a "move",
    which piece was moved, what piece was captured etc.
    """

    row_to_rank = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    col_to_file = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}


    def __init__(self, init_pos, final_pos, array):
        self.i_row = init_pos[0]
        self.i_col = init_pos[1]
        self.f_row = final_pos[0]
        self.f_col = final_pos[1]
        self.array = array
        self.moved_piece = array[self.i_row][self.i_col]
        self.captured_piece = array[self.f_row][self.f_col]
        self.moveID = 1000*self.i_row+100*self.i_col+10*self.f_row+self.f_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return True if self.moveID == other.moveID else False

    # chess-notation helper
    def get_rank_file(self):
        return self.col_to_file[self.f_col] + self.row_to_rank[self.f_row]
    
    # implement fully later.
    def get_chess_notation(self):
        if self.moved_piece.name == "pawn" and not self.captured_piece:
            return self.get_rank_file()
        elif self.moved_piece.name == "pawn" and self.captured_piece:
            return self.col_to_file[self.f_col] + "x" + self.col_to_file[self.i_col] + self.row_to_rank[self.f_row]
        
################################ END OF MOVE CLASS ##################################
#####################################################################################