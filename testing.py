import chess

# Initialize the chess board
board = chess.Board()

# Check whose turn it is
if board.turn:
    print("It is White's turn.")
else:
    print("It is Black's turn.")
