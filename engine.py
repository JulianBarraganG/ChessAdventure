from chess.game import Game, Move
from chess.pieces import Queen
import random

# game = Game()
# game.board.fen_reader(game, "k7/8/8/8/6p1/5p2/3PP3/K7 b - - 0 1")
# first_moves = game.get_valid_moves()
CHECKMATE = 10000
STALEMATE = 0
DEPTH = 4

def count_material(game):
    count = 0
    board = game.board.array
    color = 'w' if game.white_to_move else 'b'
    if game.game_over:
        if game.white_to_move:
            count = (-CHECKMATE) if game.check_mate else 0
        else:
            count = CHECKMATE if game.check_mate else 0
    else: 
        for row in board:
            for piece in row:
                if piece != None:
                    if piece.color == color:
                        count += piece.value
                    else:
                        count -= piece.value
    return count

def eval_position(game):
    return count_material(game)

# def negamax(game, moves, turn_multiplier, depth=DEPTH, alpha=-CHECKMATE, beta=CHECKMATE):
#     global best_move
#     if depth == 0 or game.game_over:
#         return turn_multiplier * eval_position(game)
    
#     max_eval = -CHECKMATE
#     for move in moves:
#         game.make_move(move)
#         subsequent_moves = game.get_valid_moves()
#         eval = -negamax(game, subsequent_moves, (-turn_multiplier), depth=depth-1, alpha=(-beta), beta=(-alpha))
#         game.undo_move()
#         if eval > max_eval:
#             max_eval = eval
#             if depth == DEPTH:
#                 best_move = move
#         if max_eval > alpha:
#             alpha = max_eval
#         if alpha >= beta:
#             break
#     return max_eval
    
        
def minimax(game, moves, maximizing_player, depth=DEPTH, alpha=(-CHECKMATE), beta=CHECKMATE):
    global best_move
    if depth == 0 or game.game_over:
        return eval_position(game)
    
    if len(moves) == 0:
        return eval_position(game)

    if maximizing_player:
        max_eval = -CHECKMATE
        for move in moves:
            game.make_move(move)
            moves = game.get_valid_moves()
            eval = minimax(game, moves, False, depth=(depth - 1), alpha=alpha, beta=beta)
            game.undo_move()
            if eval > max_eval:
                max_eval = eval
                if depth == DEPTH:
                    best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = CHECKMATE
        for move in moves:
            game.make_move(move)
            moves = game.get_valid_moves()
            eval = minimax(game, moves, True, depth=(depth - 1), alpha=alpha, beta=beta)
            game.undo_move()
            if eval < min_eval:
                min_eval = eval
                if depth == DEPTH:
                    best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval



def random_move(valid_moves):
    move = random.randint(0, len(valid_moves) - 1)
    return valid_moves[move]

def engine_move(game, moves):
    #random.shuffle(moves)
    minimax(game, moves, game.white_to_move)
    # negamax(game, moves, 1 if game.white_to_move else -1)
    move = best_move
    return move