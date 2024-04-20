import pygame as py
from .board import Board
from .constants import *
from .castling import Castling_Rights

class Game:
    """
    This class oversees the game, 
    prints all methods, handles visualisation and more.
    Game is the frontmost class
    """

    def __init__(self, flipping=False, flipped=False):
        # Can be shorter if we change get_all_moves()
        self.get_move_functions = {PAWN+W: self.get_pawn_moves, PAWN+B: self.get_pawn_moves, 
                                   ROOK+W: self.get_rook_moves, ROOK+B: self.get_rook_moves,
                                   KNIGHT+W: self.get_knight_moves, KNIGHT+B: self.get_knight_moves, 
                                   QUEEN+W: self.get_queen_moves, QUEEN+B: self.get_queen_moves, 
                                   KING+W: self.get_king_moves, KING+B: self.get_king_moves, 
                                   BISHOP+W: self.get_bishop_moves, BISHOP+B: self.get_bishop_moves}
        self.board = Board()
        self.board.reset_board()
        self.images = preload_images()
        ## FEN related variables ##
        self.fen_log = [START_FEN]
        self.fen_count = {START_FEN.split()[0]:1} # Keeps track of three-fold repeated position.
        self.half_move = 0
        self.full_move = 0
        # Board flipping vars
        self.flipping = flipping
        self.flipped = flipped if not self.flipping else False
        # Game Over booleans
        self.draw_fifty = False
        self.draw_by_repetition = False
        self.stale_mate = False
        self.check_mate = False
        ####################
        self.move_log = []
        self.white_to_move = True
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.in_check = False
        self.checks = []
        self.pins = []
        self.castling_rights = Castling_Rights(True, True, True, True)
        self.prev_castling_info = [Castling_Rights(True, True, True, True)]
        self.en_passant_possible = ()
        self.en_passant_square = "-"


    ########################### DRAWING BLOCK ###########################
    def show_bg(self, screen):
        for i in range(ROWS):
            for j in range(COLS):
                if (j+i) % 2 == 0:
                    py.draw.rect(screen, LSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                else:
                    py.draw.rect(screen, DSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    def show_pieces(self, screen):
        if (not self.flipping or self.white_to_move) and not self.flipped:
            for i in range(ROWS):
                for j in range(COLS):
                    if self.board.array[i, j]:
                        screen.blit(self.images[(self.board.array[i, j])], py.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        elif (self.flipping and not self.white_to_move) or self.flipped:
            for i in range(ROWS):
                for j in range(COLS):
                    if self.board.array[i, j]:
                        screen.blit(self.images[self.board.array[i, j]]), py.Rect(abs(j-(COLS-1))*SQ_SIZE, (abs(i-(ROWS-1)))*SQ_SIZE, SQ_SIZE, SQ_SIZE)

    ########################## DRAWING BLOCK END ##########################

    ########################## MOVING BLOCK ###############################    
    def make_move(self, move, promote_to=0):

        board = self.board.array
        self.full_move += 1
        self.half_move += 1

        # Update pieces on board and swap turns
        board[move.i_row, move.i_col] = 0
        if not move.pawn_promotion:
            board[move.f_row, move.f_col] = move.moved_piece
        else:
            board[move.f_row, move.f_col] = promote_to

        # En Passant
        dir = 1 if self.white_to_move else -1
        if (move.moved_piece & PAWN) == PAWN:
            self.half_move = 0
            if move.en_passant:
                self.en_passant_square = move.en_passant_square
                board[move.i_row, move.f_col] = 0
                self.en_passant_possible = ()
            if abs(move.i_row - move.f_row) == 2:
                self.en_passant_possible = move.f_row + dir, move.i_col
            else:
                self.en_passant_possible = ()
                self.en_passant_square = "-"
        else:
            self.en_passant_possible = ()
            self.en_passant_square = "-"
        
        # Update half move for captures
        if move.captured_piece:
            self.half_move = 0

        # Update kin pos and castling rights
        if (move.moved_piece & KING) == KING:
            if move.i_col - move.f_col == -2: # Kingside Castle
                board[move.i_row, move.i_col+1] = board[move.i_row, COLS-1]
                board[move.i_row, COLS-1] = 0
            if move.i_col - move.f_col == 2: # Queenside Castle
                board[move.i_row, move.i_col-1] = board[move.i_row, 0]
                board[move.i_row, 0] = 0
            if self.white_to_move:
                self.white_king_pos = (move.f_row, move.f_col)
                if self.castling_rights.wqs or self.castling_rights.wks:
                    self.castling_rights.wqs = self.castling_rights.wks = False
            else:
                self.black_king_pos = (move.f_row, move.f_col)
                if self.castling_rights.bqs or self.castling_rights.bks:
                    self.castling_rights.bqs = self.castling_rights.bks = False
        
        # Update rook castling  rights
        if (move.moved_piece & ROOK) == ROOK:
            if move.i_row == (ROWS - 1) and move.i_col == 0:
                self.castling_rights.wqs = False
            elif move.i_row == (ROWS - 1) and move.i_col == (COLS - 1):
                self.castling_rights.wks = False
            elif move.i_row == 0 and move.i_col == 0:
                self.castling_rights.bqs = False
            elif move.i_row == 0 and move.i_col == (COLS - 1):
                self.castling_rights.bks = False
        

        # Update castling log
        self.prev_castling_info.append(Castling_Rights(self.castling_rights.wqs, self.castling_rights.wks, self.castling_rights.bqs, self.castling_rights.bks))       

        # Update move log
        self.move_log.append(move)

        # Swap turns
        self.white_to_move = not self.white_to_move

        # Update fen log 
        fen = self.board.board_to_fen(self)
        self.fen_log.append(fen)
        latest_fen = fen.split()[0] # latest_fen means latest FEN position

        # Count repeated fen count, update draw_by_rep bool if threefold is reached.
        if latest_fen in self.fen_count:
            self.fen_count[latest_fen] += 1
            if self.fen_count[latest_fen] == 3:
                self.draw_by_repetition = True
        else:
            self.fen_count[latest_fen] = 1
        
        # fifty move rule draw
        if self.half_move == 50:
            self.draw_fifty = True


    def undo_move(self):
        if len(self.move_log) == 0:
            return print("No moves to undo")
        else:
            self.full_move -= 1
            undone_fen = self.fen_log.pop()
            move = self.move_log.pop()
            self.prev_castling_info.pop()
            board = self.board.array

            self.board.array[move.i_row, move.i_col] = move.moved_piece
            self.board.array[move.f_row, move.f_col] = move.captured_piece

            if move.en_passant:
                self.board.array[move.i_row, move.f_col] = move.captured_piece
                self.board.array[move.f_row, move.f_col] = 0
                self.en_passant_possible = (move.f_row, move.f_col)

            # Update castling rights
            temp = self.prev_castling_info[-1]
            self.castling_rights = Castling_Rights(temp.wqs, temp.wks, temp.bqs, temp.bks) # NOTE: new object every time. Never reference.
            
            # Undo castling moves
            if (move.moved_piece & KING) == KING and move.i_col - move.f_col == -2: # Kingside castle to be undone
                board[move.i_row, COLS-1] = board[move.i_row, move.i_col+1]
                board[move.i_row, move.i_col+1] = 0

            elif (move.moved_piece & KING) == KING and move.i_col - move.f_col == 2: # Queenside castle to be undone
                board[move.i_row, 0] = board[move.i_row, move.i_col-1]
                board[move.i_row, move.i_col-1] = 0

            # Update fen counts and log
            undone_pos = undone_fen.split()[0]
            if undone_pos in self.fen_count:
                if self.fen_count[undone_pos] == 1:
                    del self.fen_count[undone_pos]
                else:
                    self.fen_count[undone_pos] -=1

            # Update half_move
            self.half_move = int((self.fen_log[-1].split())[-2]) # after popping, take last FEN in log to update half_move

            # Update en_passant_square
            self.en_passant_square = self.fen_log[-1].split()[-3]

            # Swap turns
            self.white_to_move = not self.white_to_move

            # Update king pos
            if (move.moved_piece & KING) == KING:
                if self.white_to_move:
                    self.white_king_pos = (move.i_row, move.i_col)
                else:
                    self.black_king_pos = (move.i_row, move.i_col)
            
            # Undo Checkmate, Stalemate and Draw by rep
            self.check_mate = False
            self.stale_mate = False
            self.draw_by_repetition = False

    ######################## MOVING BLOCK END #############################    
    
    ################# CALCULATE LEGAL MOVES BLOCK #################
    def get_valid_moves(self):

        """
        Checks for all valid moves considering checks.
        NB: Check-mate, en-passant and pawn-promotion handled elsewhere.
        """
        board = self.board.array
        self.in_check, self.pins, self.checks = self.checks_and_pins()
        moves = []

        if self.white_to_move:
            king_row = self.white_king_pos[0]
            king_col = self.white_king_pos[1]
        else:
            king_row = self.black_king_pos[0]
            king_col = self.black_king_pos[1]
                                    
        if self.in_check:
            if len(self.checks) == 1: # 1 piece checking
                the_check = self.checks[0]  # 4-tuple with pos of checking piece and direction.
                checking_piece = board[the_check[0], the_check[1]]
                if (checking_piece & KNIGHT) != KNIGHT: # if checking piece is not a knight
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
                    if not (moves[i].moved_piece & KING == KING): # check if the moved piece is a king, if NOT then proceed.
                        if (moves[i].f_row, moves[i].f_col) not in valid_squares:
                            moves.remove(moves[i])
                if len(moves) == 0:
                    self.check_mate = True
                return moves
            
            else: # double check
                self.get_king_moves(king_row, king_col, moves)
                if len(moves) == 0:
                    self.in_check = True
                return moves

        else: # not in check
            moves = self.get_all_moves()
            if len(moves) == 0:
                self.stale_mate = True                
            return moves
        
    def get_all_moves(self):
        moves = []
        for i in range(ROWS):
            for j in range(COLS):
                if self.board.array[i, j]:
                    turn = W if (self.board.array[i, j] & W) == W else B
                else: 
                    continue
                if (turn == W and self.white_to_move) or (turn == B and not self.white_to_move):
                    piece = self.board.array[i, j]
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
        ally_mask = W if self.white_to_move else B
        enemy_mask = B if self.white_to_move else W
        
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
            if 0 <= pat[0] <= 7 and 0 <= pat[1] <= 7 and board[pat[0], pat[1]]:
                potential_knight = board[pat[0], pat[1]]
                if (potential_knight & KNIGHT) == KNIGHT and (potential_knight & 24) == enemy_mask: 
                    in_check = True
                    checks.append((pat[0], pat[1], (pat[0]-init_row), (pat[1]-init_col))) # append knight checks. 
                    # Will uniquely have either row or col dir +-2

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
                    if self.board.array[end_row, end_col]:
                        end_piece = self.board.array[end_row, end_col]
                        if (end_piece & 24) == ally_mask: # end piece is an ally
                            if (end_piece & KING) == KING: # "allied king" encounters occur internally in get_king_moves()
                                continue
                            if possible_pins == ():
                                possible_pins = (end_row, end_col, d[0], d[1])
                            else:
                                break # double allied piece, can't be any pin
                        elif (end_piece & 24) == enemy_mask: # end piece is an enemy
                            piece = end_piece - enemy_mask
                            # for all dir 4 possible check-patterns:
                            # 1) orthogonal rook checks
                            # 2) diagonal bishop checks
                            # 3) any dir queen check
                            # 4) pawn checks (1 square away)    
                            if (piece == ROOK and 0 <= j <= 3) \
                                    or (piece == BISHOP and 4 <= j <= 7) \
                                    or (piece == PAWN and i == 1 and ally_mask == W and (j == 6 or j == 7)) \
                                    or (piece == PAWN and i == 1 and ally_mask == B and (j == 4 or j == 5)) \
                                    or piece == QUEEN:

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

        ally_mask = W if self.white_to_move else B # 16 if it is white to move, ow/ 8
        # enemy_mask = B if self.white_to_move else W # 8 if it is white to move, ow/ 16

        # filter out moves that move "out of the board"
        possible_moves = tuple(filter(lambda move: move[0] >= 0 and move[0] < (ROWS) and move[1] >= 0 and move[1] < (COLS), move_pattern))
        
        #for every move within board, check if valid.
        for tpl in possible_moves:

            # temp move king pos to see if it enters check
            if ally_mask == W:
                self.white_king_pos = tpl
            else:
                self.black_king_pos = tpl
            
            in_check, _, _ = self.checks_and_pins()

            # Appending legal king moves
            target_square = board[tpl[0], tpl[1]]
            if not in_check and (not target_square or not (target_square & 24) == ally_mask): # safe empty or enemy square.
                moves.append(Move((i, j), (tpl[0], tpl[1]), board))

                # Further checking if castling is possible
                if not in_check and tpl[1] == j+1:
                    if self.white_to_move:
                        if self.castling_rights.wks and tpl[1]+1 < COLS and not board[tpl[0], tpl[1]] and not board[tpl[0], tpl[1]+1]:
                            self.white_king_pos = tpl[0], tpl[1]+1
                            in_check, _, _ = self.checks_and_pins()
                            if not in_check:
                                moves.append(Move((i, j), (i, j+2), board)) # append white ks castling move
                    else:
                        if self.castling_rights.bks and tpl[1]+1 < COLS and not board[tpl[0], tpl[1]] and not board[tpl[0], tpl[1]+1]:
                            self.black_king_pos = tpl[0], tpl[1] + 1
                            in_check, _, _ = self.checks_and_pins()
                            if not in_check:
                                moves.append(Move((i, j), (i, j+2), board)) # append black ks castling move

                if not in_check and tpl[1] == j-1: # If king can move ones towards queen, we can check if castling is possible
                    if self.white_to_move:
                        if self.castling_rights.wqs and not board[tpl[0], tpl[1]] and not board[tpl[0], tpl[1]-1] and not board[tpl[0], tpl[1]-2]:
                            self.white_king_pos = tpl[0], tpl[1]-1
                            in_check, _, _ = self.checks_and_pins()
                            if not in_check:
                                moves.append(Move((i, j), (i, j-2), board)) # append white qs castling move
                    else:
                        if self.castling_rights.bqs and not board[tpl[0], tpl[1]] and not board[tpl[0], tpl[1]-1] and not board[tpl[0], tpl[1]-2]:
                            self.black_king_pos = tpl[0], tpl[1]-1
                            in_check, _, _ = self.checks_and_pins()
                            if not in_check:
                                moves.append(Move((i, j), (i, j-2), board)) # append black qs castling move

            # reset king pos
            if ally_mask == W:
                self.white_king_pos = (i, j)
            else:
                self.black_king_pos = (i, j)


    def get_pawn_moves(self, i, j, moves):
        """
        Calculates all possible pawn moves, and adds them to the moves list
        """
        board = self.board.array
        enemy_mask = B if self.white_to_move else W
        dir = -1 if self.white_to_move else 1
        start_row = 6 if (self.board.array[i, j] & 24) == W else 1
        end_row = 0 if self.white_to_move else 7
        pinned = False
        pin_dir = None
        orthogonal_dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))

        for pin in self.pins:
            if (i, j) == (pin[0], pin[1]):
                pinned = True
                pin_dir = pin[2], pin[3]

        # Extraction of logic
        forward_empty = not board[i + dir, j] if 0 <= i + dir < ROWS else False
        two_squares_empty = not board[i + 2 * dir, j] and i == start_row if 0 <= i + 2 * dir < ROWS else False  # allow for double advance first pawn move.
        left_capture_possible = j > 0 and board[i + dir, j - 1] and (board[i + dir, j - 1] & 24) == enemy_mask if 0 <= i + dir < ROWS else False
        right_capture_possible = j < COLS - 1 and board[i + dir, j + 1] and (board[i + dir, j + 1] & 24) == enemy_mask if 0 <= i + dir < ROWS else False

        if not pinned: # add normal legal moves/captures.
            
            if i + dir == end_row and not board[i + dir, j]: # append pawn promotion move.
                moves.append(Move((i, j), (i + dir, j), board, pawn_promotion=True))

            # Add advancing moves
            if forward_empty and (i + dir != end_row):
                moves.append(Move((i, j), (i + dir, j), board))
                if two_squares_empty:
                    moves.append(Move((i, j), (i + 2 * dir, j), board, en_passant=True))

            # Add captures
            if left_capture_possible:
                moves.append(Move((i, j), (i + dir, j - 1), board)) if i + dir != end_row else moves.append(Move((i, j), (i + dir, j - 1), board, pawn_promotion=True))
            if right_capture_possible:
                moves.append(Move((i, j), (i + dir, j + 1), board)) if i + dir != end_row else moves.append(Move((i, j), (i + dir, j + 1), board, pawn_promotion=True))

            # En Passant Captures
            if self.en_passant_possible != ():
                if self.en_passant_possible[0] - dir == i and abs(self.en_passant_possible[1] - j) == 1:
                    moves.append(Move((i, j), (self.en_passant_possible[0], self.en_passant_possible[1]), board, True))

        elif 0 < j < (COLS - 1): # if pawn is pinned and capture stays within board (pinned == True implicit).

            # Logic allowing the capture of pinning piece.
            diagonal_capture_possible = board[i + pin_dir[0], j + pin_dir[1]] and (board[i + pin_dir[0], j + pin_dir[1]] & 24) == enemy_mask

            # Capturing in en passant direction
            if self.en_passant_possible != ():
                r = self.en_passant_possible[0] # en_passant row
                c = self.en_passant_possible[1] # en_passant col
                pinned_en_passant_possible = (r, c) == (i + pin_dir[0], j + pin_dir[1]) # en passant square in pin direction
                if pinned_en_passant_possible:
                    moves.append(Move((i, j), (self.en_passant_possible[0], self.en_passant_possible[1]), board, True))

            # Pinned diagonally, then capturing on said diag is possible
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

        enemy_mask = B if self.white_to_move else W # 0b0100 if white to move else 0b1000.

        possible_moves = tuple(filter(lambda move: move[0] >= 0 and move[0] < (ROWS) and move[1] >= 0 and move[1] < (COLS), move_pattern))

        if not pinned:
            for tpl in possible_moves:
                target_square = board[tpl[0], tpl[1]]
                if target_square == EMPTY or (target_square & 24) == enemy_mask: # target square & 24 keeps the 16 or 8 bit position of target square
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
                if not board[r, c]:
                    moves.append(Move((i, j), (r, c), board))
                elif board[r, c] and ((board[r, c] & 24) != (board[i, j] & 24)): # if board[r,c] is not empty and board[r, c] shares color with board[i, j] (pieces)
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
############################ MOVE CLASS ###################################
class Move():
    """
    Move class handles a chess "move" that a player can make, 
    containing information about initial and end position of a "move",
    which piece was moved, what piece was captured etc.
    """

    row_to_rank = ROW_TO_RANK
    col_to_file = COL_TO_FILE


    def __init__(self, init_pos, final_pos, array, en_passant = False, pawn_promotion = False):
        self.i_row = init_pos[0]
        self.i_col = init_pos[1]
        self.f_row = final_pos[0]
        self.f_col = final_pos[1]
        self.array = array
        self.moved_piece = array[self.i_row, self.i_col]
        self.en_passant = en_passant
        self.pawn_promotion = pawn_promotion
        self.captured_piece = array[self.f_row, self.f_col] if not self.en_passant else array[self.i_row, self.f_col]
        self.moveID = 1000*self.i_row+100*self.i_col+10*self.f_row+self.f_col
        self.en_passant_square = "-" if not self.en_passant else self.col_to_file[self.f_col] + self.row_to_rank[self.f_row + (1 if (self.moved_piece & 24) == W else -1)]
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return True if self.moveID == other.moveID else False

    # chess-notation helper
    def get_rank_file(self):
        return self.col_to_file[self.f_col] + self.row_to_rank[self.f_row]
    
    # implement fully later.
    def get_chess_notation(self):
        if (self.moved_piece & PAWN) == PAWN and not self.captured_piece:
            return self.get_rank_file()
        elif (self.moved_piece & PAWN) == PAWN and self.captured_piece:
            return self.col_to_file[self.f_col] + "x" + self.col_to_file[self.i_col] + self.row_to_rank[self.f_row]
        

################################ END OF MOVE CLASS ##################################
#####################################################################################