## Notes on Project

This project was my pet project, in the summer between my first and second year on the bachelor.
Although it has taught me a lot about OOB and structuring a project in Python, I must leave it behind.

The reality of chess engines, is that performance is essential. 

In the future, I will most likely reimplement chess in C++ or C# with focus on performance, and implemented AI algorithms from scratch.

However, another goal of mine is to do a Deep Reinforcement Learning chess engine, for which I will most likely be revisiting Python.

The current implementation is painfully slow, since it is mostly native Python.

### MiniMax Chess Engine

This following chess engine is a private project of mine, which was built for the purposes of learning and a love for Chess and Machine Learning.

Chess has been programmed from scratch, loading in some copyright free images for piece representation, and on top of this, a simple Engine has been added.

This opens the opertunity for exploring different modifications and improvements made to an engine, and study the effects of such.

Note that this engine style is in the style of Stockfish, with encoded biases from a user, potentially in the form of 100 years of chess theory, but still encoding bias.

In the future, I might convert the underlying data structure to something like tensors, and use PyTorch to do an AlphaZero inspired chess engine. A chess engine purely based on reinforcement learning.

But for now, feel free to challange my engine. The game works by having python and pygames. Then via your favorite terminal, navigate to the directory where the main.py file is and input **python main.py** this should open the browser, and you can play white against the engine.

If you wish to play black, swap the boolean values of player_one and player_two in the main.py script.


## TO DO

checks-and-pins debugging \\
move.captured_piece = Pawn after moving double at first step, figure out and fix.\\
find bugs and clean up performance test\\
queen was captured sideways by pawn in game against engine. Find bug?\\
add threading so engine can play engine\\
