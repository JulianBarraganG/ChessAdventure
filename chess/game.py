import pygame as py
from .board import Board
from .constants import ROWS, COLS, DSQ, LSQ, SQ_SIZE

class Game:
    """
    This class oversees the game, 
    prints all methods, handles visualisation and more.
    Game is the frontmost class
    """

    def __init__(self):
        self.next_player = 'w'
        self.board = Board()
        self.board.reset_board()
        self.move_log = []
        self.white_to_move = True
        self.get_move_functions = {'pawn' : self.get_pawn_moves, 'rook' : self.get_rook_moves, 'knight' : self.get_knight_moves, 
                                   'queen': self.get_queen_moves, 'king': self.get_king_moves, 'bishop': self.get_bishop_moves}

    # Draw the squares in background
    def show_bg(self, screen):
        for i in range(ROWS):
            for j in range(COLS):
                if (j+i) % 2 == 0:
                    py.draw.rect(screen, DSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                else:
                    py.draw.rect(screen, LSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    def show_pieces(self, screen):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board.array[i][j]:
                    screen.blit(self.board.array[i][j].img, py.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    def make_move(self, move):
        self.board.array[move.i_row][move.i_col] = None
        self.board.array[move.f_row][move.f_col] = move.moved_piece
        self.move_log.append(move) 
        self.white_to_move = not self.white_to_move # Swap turns
        #print(move.get_chess_notation())

    # Checks for all valid moves considering checks. check-mate, en-passant and pawn-promotion handled elsewhere.
    def get_valid_moves(self):
        return self.get_all_moves() # for now we don't care about checks
    
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

    def get_pawn_moves(self, i, j, moves):
        """
        Calculates all possible pawn moves, and adds them to the moves list
        """
        board = self.board.array
        if self.white_to_move: # whites turn
            # move 1 forward, or 2 if first move.
            if not board[i-1][j]:
                moves.append(Move((i, j), (i-1, j), board))
                if not board[i-2][j] and i == 6:
                    moves.append(Move((i, j), (i-2, j), board))
            # captures
            if j > 0:
                if board[i-1][j-1] and board[i-1][j-1].color == 'b':
                    moves.append(Move((i, j), (i-1, j-1), board))
            if j < (COLS-1):
                if board[i-1][j+1] and board[i-1][j+1].color == 'b':
                    moves.append(Move((i, j), (i-1, j+1), board))
        else: # blacks turn
            # move 1 forward, or 2 if first move.
            if not board[i+1][j]:
                moves.append(Move((i, j), (i+1, j), board))
                if not board[i+2][j] and i == 1:
                    moves.append(Move((i, j), (i+2, j), board))
            # captures
            if j > 0:
                if board[i+1][j-1] and board[i+1][j-1].color == 'w':
                    moves.append(Move((i, j), (i+1, j-1), board))
            if j < (COLS-1):
                if board[i+1][j+1] and board[i+1][j+1].color == 'w':
                    moves.append(Move((i, j), (i+1, j+1), board))
        
    def get_knight_moves(self, i, j, moves):
        """
        Calculates all possible knight moves, and adds them to the moves list
        """
        board = self.board.array
        move_pattern = [
            (i-1, j-2),
            (i-1, j+2),
            (i+1, j-2),
            (i+1, j+2),
            (i-2, j-1),
            (i-2, j+1),
            (i+2, j-1),
            (i+2, j+1)
        ]

        possible_moves = []

        if self.white_to_move: # whites turn
            possible_moves = list(filter(lambda move: move[0] >= 0 and move[0] < (ROWS) and move[1] >= 0 and move[1] < (COLS), move_pattern))
            for tpl in possible_moves:
                if not board[tpl[0]][tpl[1]] or not board[tpl[0]][tpl[1]].color == 'w':
                    moves.append(Move((i, j), (tpl[0], tpl[1]), board))

        if not self.white_to_move: # blacks turn
            possible_moves = list(filter(lambda move: move[0] >= 0 and move[0] < (ROWS) and move[1] >= 0 and move[1] < (COLS), move_pattern))
            for tpl in possible_moves:
                if not board[tpl[0]][tpl[1]] or not board[tpl[0]][tpl[1]].color == 'b':
                    moves.append(Move((i, j), (tpl[0], tpl[1]), board))

    def get_rook_moves(self, i, j, moves):
        """
        Calculates all possible rook moves, and adds them to the moves list
        """
        board = self.board.array

        def add_move(start, end, color):
            """
            Helper function extracting logic for simplicity.
            """
            if board[end[0]][end[1]] and board[end[0]][end[1]].color == color:
                return False
            moves.append(Move(start, end, board))
            if board[end[0]][end[1]] and board[end[0]][end[1]].color == ('b' if color == 'w' else 'w'):
                return False
            return True

        if self.white_to_move:
            col = 'w' # white rook moves
            u = i - 1
            while u >= 0 and add_move((i, j), (u, j), col): # up
                u -= 1
            d = i + 1
            while d < ROWS and add_move((i, j), (d, j), col): # down
                d += 1
            l = j - 1
            while l >= 0 and add_move((i, j), (i, l), col): # left
                l -=1
            r = j + 1
            while r < COLS and add_move((i, j), (i, r), col): # right
                r += 1

        else:
            col = 'b' # black rook moves
            u = i - 1
            while u >= 0 and add_move((i, j), (u, j), col): # up
                u -= 1
            d = i + 1
            while d < ROWS and add_move((i, j), (d, j), col): # down
                d += 1
            l = j - 1
            while l >= 0 and add_move((i, j), (i, l), col): # left
                l -=1
            r = j + 1
            while r < COLS and add_move((i, j), (i, r), col): # right
                r += 1

    def get_bishop_moves(self, i, j, moves):
        """
        Calculates all possible rook moves, and adds them to the moves list
        """
        board = self.board.array

        def add_move(start, end, color):
            """
            Helper function extracting logic for simplicity.
            """
            if board[end[0]][end[1]] and board[end[0]][end[1]].color == color:
                return False
            moves.append(Move(start, end, board))
            if board[end[0]][end[1]] and board[end[0]][end[1]].color == ('b' if color == 'w' else 'w'):
                return False
            return True
        
        if self.white_to_move:
            col = 'w' # white bishop moves
            u = i - 1
            l = j - 1
            while (u >= 0 and l >= 0) and add_move((i,j), (u, l), col): # up and left
                u -= 1
                l -= 1

            u = i - 1
            r = j + 1
            while (u >= 0 and r < COLS) and add_move((i, j), (u, r), col): # up and right
                u -= 1
                r += 1

            d = i + 1
            l = j - 1
            while (d < ROWS and l >=0) and add_move((i, j), (d, l), col): # down and left
                d += 1
                l -= 1
                
            d = i + 1
            r = j + 1
            while (d < ROWS and r < COLS) and add_move((i, j), (d, r), col): # down and right
                d += 1
                r += 1
        else:
            col = 'b' # black bishop moves
            u = i - 1
            l = j - 1
            while (u >= 0 and l >= 0) and add_move((i,j), (u, l), col): # up and left
                u -= 1
                l -= 1

            u = i - 1
            r = j + 1
            while (u >= 0 and r < COLS) and add_move((i, j), (u, r), col): # up and right
                u -= 1
                r += 1

            d = i + 1
            l = j - 1
            while (d < ROWS and l >=0) and add_move((i, j), (d, l), col): # down and left
                d += 1
                l -= 1
    
            d = i + 1
            r = j + 1
            while (d < ROWS and r < COLS) and add_move((i, j), (d, r), col): # down and right
                d += 1
                r += 1

    def get_king_moves(self, i, j, moves):

        board = self.board.array
        move_pattern = [
            (i-1, j+1), #up right
            (i-1, j-1), #up left
            (i-1, j), #up
            (i, j+1), #right
            (i, j-1), #left
            (i+1, j+1), #down right
            (i+1, j-1), #down left
            (i+1, j), # down
        ]

        possible_moves = []


        if self.white_to_move: # whites turn
            possible_moves = list(filter(lambda move: move[0] >= 0 and move[0] < (ROWS) and move[1] >= 0 and move[1] < (COLS), move_pattern))
            for tpl in possible_moves:
                if not board[tpl[0]][tpl[1]] or not board[tpl[0]][tpl[1]].color == 'w':
                    moves.append(Move((i, j), (tpl[0], tpl[1]), board))

        if not self.white_to_move: # blacks turn
            possible_moves = list(filter(lambda move: move[0] >= 0 and move[0] < (ROWS) and move[1] >= 0 and move[1] < (COLS), move_pattern))
            for tpl in possible_moves:
                if not board[tpl[0]][tpl[1]] or not board[tpl[0]][tpl[1]].color == 'b':
                    moves.append(Move((i, j), (tpl[0], tpl[1]), board))

    def get_queen_moves(self, i, j, moves):
        """
        Calc queen moves.
        """
        self.get_bishop_moves(i, j, moves)
        self.get_rook_moves(i, j, moves)


class Move():

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