from chess.game import Game, Move
from chess.pieces import Queen
import random


CHECKMATE = 10000
STALEMATE = 0
DEPTH = 3

def count_material(game):
    """
    Takes the gamestate as input and returns zero-sum game of piece value.
    Values found in piece.value.
    """
    count = 0
    board = game.board.array
    if game.game_over: # consider moving this to negamax
        if game.white_to_move:
            # If white is to move and there is a check mate, white must be checkmated.
            count = (-CHECKMATE) if game.check_mate else 0
        else:
            # vice versa
            count = CHECKMATE if game.check_mate else 0
    else: 
        for row in board:
            for piece in row:
                if piece != None:
                    if piece.color == 'w':
                        count += piece.value
                    else:
                        count -= piece.value
    return count

def eval_position(game):
    """
    Evaluates position, currently only based on material.
    (Ideas for future evaluations: 
    Positional evaluation as well as threats and protection could add value to pieces.)
    """
    return count_material(game)

def negamax(game, moves, turn_multiplier, alpha, beta, depth=DEPTH):
    """
    NegaMax is an elaboration of minimax. max(a, b) = -max(-b, -a) is the key idea,
    making both black and white "maximizing player".
    Alpha-Beta pruning cuts away unnecessary branches.
    (To be added: helper function which orders moves by captures, attacks and checks to be considered first.)
    """
    global best_move

    if depth == 0 or game.game_over:
        return turn_multiplier * eval_position(game)
    
    max_eval = -CHECKMATE
    for move in moves:
        game.make_move(move)
        subsequent_moves = game.get_valid_moves()
        eval = -negamax(game, subsequent_moves, -turn_multiplier, -beta, -alpha, depth=depth-1)
        if eval > max_eval:
            max_eval = eval
            if depth == DEPTH:
                best_move = move
        game.undo_move()
        alpha = max(alpha, max_eval)
        if alpha >= beta:
            break
    return max_eval
    
# Predecessor to negamax        
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
            alpha = max(alpha, max_eval)
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
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval


def random_move(valid_moves):
    """Returns a random move in moves list"""
    move = random.randint(0, len(valid_moves) - 1)
    return valid_moves[move]

def engine_move(game, moves):
    """
    Currently based on NegaMax function. 
    See engine.py
    """
    random.shuffle(moves)
    negamax(game, moves, 1 if game.white_to_move else -1, -CHECKMATE, CHECKMATE)
    move = best_move
    return move