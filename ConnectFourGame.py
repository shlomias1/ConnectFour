import tkinter as tk
from tkinter import messagebox
import math

class TicTacToe:
    EMPTY = 0
    X = 1
    O = -1

    def __init__(self):
        self.board = [[self.EMPTY] * 3 for _ in range(3)]
        self.current_player = self.X

    def make_move(self, row, col):
        if self.board[row][col] == self.EMPTY:
            self.board[row][col] = self.current_player
            self.current_player = self.X if self.current_player == self.O else self.O
            return True
        return False

    def undo_move(self, row, col):
        self.board[row][col] = self.EMPTY
        self.current_player = self.X if self.current_player == self.O else self.O

    def check_winner(self):
        for i in range(3):
            if abs(sum(self.board[i])) == 3:
                return self.board[i][0]
            if abs(sum(row[i] for row in self.board)) == 3:
                return self.board[0][i]

        if abs(sum(self.board[i][i] for i in range(3))) == 3:
            return self.board[0][0]
        if abs(sum(self.board[i][2 - i] for i in range(3))) == 3:
            return self.board[0][2]

        if all(cell != self.EMPTY for row in self.board for cell in row):
            return 0

        return None

    def available_moves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == self.EMPTY]

class MinimaxPlayer:
    def evaluate(self, game):
        winner = game.check_winner()
        if winner == game.X:
            return 1
        elif winner == game.O:
            return -1
        else:
            return 0

    def minimax(self, game, depth, maximizing):
        score = game.check_winner()
        if score is not None:
            return self.evaluate(game)

        if maximizing:
            max_eval = -math.inf
            for row, col in game.available_moves():
                game.make_move(row, col)
                eval = self.minimax(game, depth + 1, False)
                game.undo_move(row, col)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for row, col in game.available_moves():
                game.make_move(row, col)
                eval = self.minimax(game, depth + 1, True)
                game.undo_move(row, col)
                min_eval = min(min_eval, eval)
            return min_eval

    def choose_move(self, game):
        best_score = -math.inf
        best_move = None
        for row, col in game.available_moves():
            game.make_move(row, col)
            score = self.minimax(game, 0, False)
            game.undo_move(row, col)
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_move

class TicTacToeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        
        self.game = TicTacToe()
        self.ai = MinimaxPlayer()

        self.buttons = [[tk.Button(root, text="", font=("Arial", 24), width=5, height=2, command=lambda r=r, c=c: self.player_move(r, c)) for c in range(3)] for r in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].grid(row=r, column=c)

    def player_move(self, row, col):
        if self.game.board[row][col] != self.game.EMPTY or self.game.check_winner() is not None:
            return

        self.game.make_move(row, col)
        self.update_ui()

        if self.game.check_winner() is None:
            self.root.after(500, self.ai_move)
        else:
            self.end_game()

    def ai_move(self):
        move = self.ai.choose_move(self.game)
        if move:
            self.game.make_move(*move)
        self.update_ui()
        if self.game.check_winner() is not None:
            self.end_game()

    def update_ui(self):
        for r in range(3):
            for c in range(3):
                text = "X" if self.game.board[r][c] == self.game.X else "O" if self.game.board[r][c] == self.game.O else ""
                self.buttons[r][c].config(text=text)

    def end_game(self):
        winner = self.game.check_winner()
        if winner == self.game.X:
            messagebox.showinfo("Game Over", "You win!")
        elif winner == self.game.O:
            messagebox.showinfo("Game Over", "AI wins!")
        else:
            messagebox.showinfo("Game Over", "It's a draw!")
        self.reset_game()

    def reset_game(self):
        self.game = TicTacToe()
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeUI(root)
    root.mainloop()
