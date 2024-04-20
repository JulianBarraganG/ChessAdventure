import numpy as np
from chess.constants import *
from chess.castling import Castling_Rights

class Board:
    """
    Contains array of board as well as methods to modify said array,
    before projecting to images via the Game class.
    """

    def __init__(self):
        self.array = np.zeros((8, 8), dtype=np.uint8)

    def _start_pos(self, color):
        """
        Adds pieces to initial positions.
        """
        pawn_row, piece_row = (6, 7) if color == W else (1, 0)

        # Add pawns to array
        for j in range(COLS):
            self.array[pawn_row][j]= PAWN + color

        # Add pieces to array
        self.array[piece_row][0] = ROOK + color
        self.array[piece_row][7] = ROOK + color

        self.array[piece_row][1] = KNIGHT + color
        self.array[piece_row][6] = KNIGHT + color

        self.array[piece_row][2] = BISHOP + color
        self.array[piece_row][5] = BISHOP + color

        self.array[piece_row][3] = QUEEN + color

        self.array[piece_row][4] = KING + color

    def reset_board(self):
        self.array = np.zeros((8, 8), dtype=np.uint8) # clear board
        self._start_pos(W)
        self._start_pos(B)
    

    def fen_reader(self, game, fen=START_FEN):
        """
        Takes a fen string and converts the position into array form.
        Modifies the array of the board class.
        Modifies game state (i.e. castling rights, full- and half moves etc.)
        """
        self.array = np.zeros((8, 8), dtype=np.uint8) # clears the board.
        row = 0
        col = 0
    
        piece_mapping = STR2PIECE_MAPPING
        # Assign gamestate starting FEN
        self.fen_log = [fen]
        self.fen_count = {fen.split()[0]:1} # NOTE that threefold repitition only counts from FEN forward

        # Initiate pieces in array
        for char in fen:
            if char.isdigit():
                col += int(char)
            elif char.lower() in piece_mapping:
                piece_class = piece_mapping[char.lower()]
                color = W if char.isupper() else B
                self.array[row, col] = piece_class + color
                if char == 'K':
                    game.white_king_pos = (row, col)
                elif char == 'k':
                    game.black_king_pos = (row, col)
                col += 1
            elif char == '/':
                row += 1
                col = 0
            elif char.isspace():
                break
        
        # Assign player turn (black or white to play)
        player_turn = fen.split()[1]
        game.white_to_move = True if player_turn == "w" else False

        # Assign castling rights from FEN
        cr_string = fen.split()[2]
        fen_cr = Castling_Rights(False, False, False, False)
        if cr_string != "-":
            for char in cr_string:
                fen_cr.wks = True if char == "K" else False
                fen_cr.wqs = True if char == "Q" else False
                fen_cr.bks = True if char == "k" else False
                fen_cr.bqs = True if char == "q" else False
        game.castling_rights = fen_cr
        game.prev_castling_info = [fen_cr] # Castling rights log start from here.

        # Designate en passant square
        fen_ep = fen.split()[3]
        game.en_passant_square = fen_ep
        if fen_ep == "-":
            game.en_passant_possible = ()
        else:
            game.en_passant_possible = (FILE_TO_COL[fen_ep[0]], RANK_TO_ROW[fen_ep[1]])
        
        # Assign full- and half move count
        hm_count = int(fen.split()[4])
        fm_count = int(fen.split()[5])
        game.half_move = hm_count
        game.full_move = fm_count

        return self.array


    def board_to_fen(self, game):
        """
        Takes the game state (game) as input and returns the game state as a FEN notation string (international chess string gamestate convention).
        """
        board = self.array
        fen_position = ""
        fen_string = ""
        piece_mapping = PIECE2STRING_MAPPING
        cr = game.castling_rights

        # Convert board position into fen_string
        for i in range(ROWS):
            empty_squares = 0
            for j in range(COLS):
                if board[i][j]:
                    fen_position += piece_mapping[board[i][j]]
                elif not board[i][j]:
                    while not board[i][j]:
                        empty_squares += 1
                        if board[i][j + 1 if j + 1 < COLS else j]:
                            fen_position += str(empty_squares)
                            empty_squares = 0
                        elif j == COLS - 1:
                            fen_position += str(empty_squares)
                            empty_squares = 0
                            break
                        break
            if i < ROWS - 1:
                fen_position += "/"

        # At position as the first part of the fen_string
        fen_string += fen_position

        # Assigns turn to FEN
        fen_string += " w " if game.white_to_move else " b "

        # Assign castling rights
        castling_rights = "".join([
            "K" if cr.wks else "",
            "Q" if cr.wqs else "",
            "k" if cr.bks else "",
            "q" if cr.bqs else ""
        ])
        fen_string += castling_rights if castling_rights else "-"


        # Assign en passant
        fen_string += " "+ game.en_passant_square

        # Assign HALF move counter
        fen_string += " " + str(game.half_move)

        # Assign FULL move counter
        fen_string += " " + str(game.full_move)

        return fen_string