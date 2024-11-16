# Chess Position Review and Analysis Tool

This Python script uses the Stockfish chess engine to analyze specific positions and simulate self-play to generate insights into piece placement. It creates visualizations showing the most common squares for each piece during the analysis, helping players and enthusiasts study optimal piece positioning, particularly in the opening phase of the game.

## Features
- **Stockfish Integration**: Leverages Stockfish for high-depth position analysis.
- **Self-Play Simulation**: Runs multiple games with the engine to understand the flow of the position.
- **Piece Placement Insights**: Generates pie chart visualizations to highlight the most frequently visited squares by each piece.
- **Opening Study**: Ideal for analyzing specific openings and learning good squares for pieces.

## Example Usage
The included example focuses on the **Caro-Kann Defense: H5 Attack**, analyzing 100 games with a depth of 30 moves, and visualizes the results in a clear and intuitive format.

```python
def ReviewPosition():
    # Example usage:
    position = "rnbqkbnr/pp2pppp/2p5/3pP3/3P4/2N5/PPP2PPP/R1BQKBNR w KQkq - 1 5"
    engine = StockfishEngine(r"path\to\stockfish.exe")
    engine.track_piece_move(games=100, depth=30, fen=position)
    engine.plot_ranking_pie_charts()
