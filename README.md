# Gomoku Agent
Program that plays Five-in-a-Row (also called Gobang or Gomoku) with a human opponent.
This Gomoku playing agent uses Minimax algorithm with alpha-beta pruning to search for the best move. The implementation is done in Python 3, using only standard libraries. Please read the report for more technical details.
## Usage
If you would like to play against this Agent (i.e. you are the human opponent) change the directory to this repository `cd your/path/Gomoku` and start the executable by `./gobang` command
You can also directly issue the following command `python3 gobang.py`
### flags:
`-n <number>` : size of the board. Sizes 5*5 to 26*26 are allowed. If n is not specified, the default value is 11*11.
`-l` : you will play as Light player, while computer will play as Dark. Dark players makes the first move
