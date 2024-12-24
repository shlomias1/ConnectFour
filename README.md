# Connect Four with MCTS AI

This project implements the classic Connect Four game, allowing a human player to compete against an AI controlled by the Monte Carlo Tree Search (MCTS) algorithm. The game features both a command-line interface (CLI) and a graphical user interface (GUI) built with Python's `tkinter` library.

---

## Features

1. **Game Logic:**
   - Implements Connect Four rules with a 7x6 board.
   - Detects win conditions (horizontal, vertical, diagonal) and draw scenarios.

2. **AI Opponent:**
   - Uses MCTS for decision-making, with customizable simulation count.
   - Dynamically adapts to gameplay, optimizing moves to maximize its chances of winning.

3. **Multiple Interfaces:**
   - **Command-Line Interface (CLI):** Play via terminal input.
   - **Graphical User Interface (GUI):** Interactive GUI built with `tkinter` for a more intuitive experience.

4. **Error Handling:**
   - Prevents illegal moves and provides informative messages.

5. **Customizable Settings:**
   - Adjustable number of MCTS simulations for AI difficulty tuning.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd connect-four
   ```

2. **Install required packages:**
   Ensure you have Python 3.7+ installed. Install `tkinter` if not already included (on most systems, it is bundled with Python).

---

## How to Run

### Command-Line Interface (CLI):
1. Run the CLI version:
   ```bash
   python connect_four.py
   ```
2. Follow the prompts to make moves and play against the AI.

### Graphical User Interface (GUI):
1. Run the GUI version:
   ```bash
   python connect_four.py
   ```
2. Use the arrow buttons to make your move. The game updates dynamically.

---

## How to Play

1. Players take turns dropping pieces into one of the seven columns.
2. The goal is to align four of your pieces (horizontally, vertically, or diagonally) before your opponent.
3. The game ends when a player wins or the board is full (draw).

---

## Code Overview

### Main Components

1. **ConnectFour Class:**
   - Handles game state, move legality, win detection, and board representation.

2. **MCTSPlayer Class:**
   - AI logic powered by Monte Carlo Tree Search.

3. **ConnectFourGUI Class:**
   - GUI implementation for intuitive gameplay.

4. **Main Function:**
   - Entry point for both CLI and GUI modes.

### Key Files:
- `connect_four.py`: Contains all game logic, MCTS implementation, and GUI.

---

## Customization

- **AI Difficulty:** Adjust the number of simulations in `MCTSPlayer`:
  ```python
  mcts_player = MCTSPlayer(simulations=3000)
  ```
- **Exploration Weight:** Modify exploration-exploitation tradeoff:
  ```python
  MCTSPlayer(exploration_weight=2)
  ```

---

## Future Improvements

1. Add support for multiplayer mode (local or online).
2. Enhance GUI aesthetics.
3. Optimize MCTS for better performance on larger simulation counts.

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

## Acknowledgements

- MCTS algorithm for strategic AI gameplay.
- Python's `tkinter` for creating an intuitive graphical interface.

