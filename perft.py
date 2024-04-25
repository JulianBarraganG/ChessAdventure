import time
from tqdm import tqdm
from chess.game import *
from chess.constants import START_FEN

def perft(depth, game, nodes=0, captures=0, counts=None):
    if depth == 0:
        return 1, 0  # Leaf node, count as 1 node reached and 0 captures

    if counts is None:
        counts = []

    moves = game.get_valid_moves()
    count = nodes
    take = captures

    with tqdm(total=len(moves), desc=f"Depth {depth}", leave=False) as pbar:
        for move in moves:
            if move.captured_piece:
                take += 1
            game.make_move(move)
            sub_count, sub_captures = perft(depth - 1, game)
            count += sub_count
            take += sub_captures
            game.undo_move()
            pbar.update(1)

    counts.append(count)
    return count, take

depth = 1
initial_game = Game()
initial_game.board.fen_reader(initial_game, "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - ")
start_time = time.time()
total_moves, total_captures = perft(depth, initial_game)
end_time = time.time()
elapsed_time = end_time - start_time

minutes, seconds = divmod(elapsed_time, 60)
print(f"\nTotal moves at final depth {depth}: {total_moves}")
print(f"\nTotal captures at final depth {depth}: {total_captures}")
print(f"\nTime taken: {int(minutes)} minutes and {seconds:.2f} seconds")
