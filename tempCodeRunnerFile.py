import random
import subprocess
import chess
import matplotlib.pyplot as plt
from collections import Counter

class StockfishEngine:
    
    def __init__(self, stockfish_path="stockfish"):
        self.stockfish_path = stockfish_path
        self.process = subprocess.Popen(
            self.stockfish_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        self.board = chess.Board()

    def track_piece_move(self, games=1, depth=1, fen="", initial_fen=""):
        initial_fen = fen  # Store the initial FEN for resetting
        self.board.set_fen(fen)

        self.white_pieces = {'P': [], 'B': [], 'N': [], 'R': [], 'Q': [], 'K': []}
        self.black_pieces = {'p': [], 'b': [], 'n': [], 'r': [], 'q': [], 'k': []}

        for _ in range(games):
            # Reset to the initial FEN at the start of each game
            self.board.reset()
            self.board.set_fen(initial_fen)
            fen = initial_fen

            while not (
                self.board.is_checkmate() or
                self.board.is_stalemate() or
                self.board.is_insufficient_material() or
                self.board.is_seventyfive_moves() or
                self.board.is_fivefold_repetition() or
                self.board.can_claim_fifty_moves() or
                self.board.can_claim_threefold_repetition()
            ):
                best_move = self.find_best_move(fen, random.randint(1, depth))

                # Handle promotions, en passant, and regular moves
                if len(best_move) == 5:
                    square_index = chess.parse_square(best_move[2:4])
                    square = chess.square_name(square_index)
                    piece = self.board.piece_at(chess.parse_square(best_move[:2]))
                    if piece:
                        if self.board.turn:
                            self.white_pieces[piece.symbol()].append(square)
                        else:
                            self.black_pieces[piece.symbol()].append(square)
                elif "e.p." in best_move:
                    square_index = chess.parse_square(best_move[-5:-3])
                    square = chess.square_name(square_index)
                    piece = self.board.piece_at(chess.parse_square(best_move[:2]))
                    if piece:
                        if self.board.turn:
                            self.white_pieces[piece.symbol()].append(square)
                        else:
                            self.black_pieces[piece.symbol()].append(square)
                else:
                    square_index = chess.parse_square(best_move[-2:])
                    square = chess.square_name(square_index)
                    piece = self.board.piece_at(chess.parse_square(best_move[:2]))
                    if piece:
                        if self.board.turn:
                            self.white_pieces[piece.symbol()].append(square)
                        else:
                            self.black_pieces[piece.symbol()].append(square)

                # Push the legal move and update FEN
                self.board.push_uci(best_move)
                fen = self.board.fen()

        white_ranking = self.rank_pieces(self.white_pieces)
        black_ranking = self.rank_pieces(self.black_pieces)
        
        return white_ranking, black_ranking, games

    def rank_pieces(self, piece_dict):
        result = []
        for piece, locations in piece_dict.items():
            counter = Counter(locations)
            total_moves = sum(counter.values())
            most_common_location = [(loc, round(count / total_moves * 100, 2)) for loc, count in counter.most_common()]
            result.append((piece, most_common_location))
        return result
    
    # Plotting the ranking as individual pie charts
    @staticmethod
    def plot_ranking_pie_charts(white_ranking, black_ranking, total_games):
        fig, axes = plt.subplots(2, len(white_ranking), figsize=(15, 8))
        fig.suptitle(f'Piece Movement Frequency (Total Games: {total_games})', fontsize=16)

        # Plot white pieces
        for i, (piece, locations) in enumerate(white_ranking):
            squares, percentages = zip(*locations[:8])  # Show only top 8 locations
            axes[0, i].pie(
                percentages, labels=squares, autopct=lambda p: f'{p:.1f}%' if p > 5 else '', 
                startangle=140, 
                textprops={'fontsize': 6.5},
                colors=plt.cm.Blues([0.3 + 0.7 * i / len(white_ranking) for _ in range(len(squares))])
            )
            axes[0, i].set_title(f'White {piece}', fontsize=20)

        # Plot black pieces
        for i, (piece, locations) in enumerate(black_ranking):
            squares, percentages = zip(*locations[:8])  # Show only top 8 locations
            axes[1, i].pie(
                percentages, labels=squares, autopct=lambda p: f'{p:.1f}%' if p > 5 else '', 
                startangle=140, 
                textprops={'fontsize': 6.5},
                colors=plt.cm.Reds([0.3 + 0.7 * i / len(black_ranking) for _ in range(len(squares))])
            )
            axes[1, i].set_title(f'Black {piece}', fontsize=20)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

    def send_command(self, command):
        if self.process.stdin.closed:
            raise ValueError("Attempting to send command to a closed process.")
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

    def get_output(self):
        output = self.process.stdout.readline()
        return output.strip()

    def find_best_move(self, fen, depth=1):
        self.set_position(fen)
        self.send_command(f"go depth {depth}")
        while True:
            output = self.get_output()
            if output.startswith("bestmove"):
                return output.split()[1]

    def set_position(self, fen):
        self.send_command(f"position fen {fen}")

    def set_option(self, name, value):
        self.send_command(f"setoption name {name} value {value}")
        self.get_output()

    def quit(self):
        self.send_command("quit")
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.stderr.close()
        self.process.terminate()

# Example usage:

engine = StockfishEngine(r"C:\Users\mcbac\Downloads\stockfish-windows-x86-64-avx2 (1)\stockfish\stockfish-windows-x86-64-avx2.exe")
engine.send_command("setoption name Threads value 12")
print("Starting!")

# Set a position and get the best move rankings
white_ranking, black_ranking, total_games = engine.track_piece_move(
    games=100, 
    depth=5, 
    fen="rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR b KQkq - 0 1", 
    initial_fen="rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR b KQkq - 0 1"
)

engine.plot_ranking_pie_charts(white_ranking, black_ranking, total_games)

# Close the engine when done
# engine.quit()
