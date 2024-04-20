import time
from tqdm import tqdm
from chess.game import *
from chess.constants import START_FEN

def perft(depth, game, nodes=0, counts=[]):
    if depth == 0:
        return 1  # Leaf node, count as 1 node reached

    moves = game.get_valid_moves()
    count = nodes

    with tqdm(total=len(moves), desc=f"Depth {depth}", leave=False) as pbar:
        for move in moves:
            game.make_move(move)
            count += perft(depth - 1, game)
            game.undo_move()
            pbar.update(1)

    counts.append(count)
    return count

depth = 4
initial_game = Game()
initial_game.board.fen_reader(initial_game, START_FEN)
start_time = time.time()
counts = []
result = perft(depth, initial_game, counts=counts)
end_time = time.time()
elapsed_time = end_time - start_time

minutes, seconds = divmod(elapsed_time, 60)
print(f"\nNodes at each level: {counts}")
print(f"\nResult at final depth {depth}: {result}")
print(f"\nTime taken: {int(minutes)} minutes and {seconds:.2f} seconds")
