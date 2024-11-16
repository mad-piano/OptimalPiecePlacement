from StockFishEnginePython import *

def ReviewPosition():
    # Example usage:
    position = "rnbqkbnr/pp2pppp/2p5/3pP3/3P4/2N5/PPP2PPP/R1BQKBNR w KQkq - 1 5"
    engine = StockfishEngine(r"C:\Users\mcbac\OneDrive\Desktop\Chess-Util\stockfish\stockfish-windows-x86-64-avx2.exe")
    engine.send_command("setoption name Threads value 12")
    print("Reviewing Position...")

    # Set a position and get the best move rankings
    white_ranking, black_ranking, total_games = engine.track_piece_move(
        games=100, 
        depth=30, 
        fen=position, 
        initial_fen=position,
        move_limit=20
    )

    engine.plot_ranking_pie_charts(white_ranking, black_ranking, total_games, total_moves=20, opening_name="Caro-Kann Defense: H5 Attack", depth=30)

    # Close the engine when done
    # engine.quit()

if __name__ == "__main__":
    # Code to be executed only when the script is run directly
    ReviewPosition()