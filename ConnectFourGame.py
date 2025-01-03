import math
import random
import tkinter as tk
from tkinter import messagebox

class ConnectFour:
    RED = 1
    YELLOW = -1
    EMPTY = 0
    RED_WIN = 1
    YELLOW_WIN = -1
    DRAW = 0
    ONGOING = -17

    def __init__(self):
        self.board = [[self.EMPTY] * 6 for _ in range(7)]
        self.heights = [0] * 7
        self.player = self.RED
        self.status = self.ONGOING
        self.last_move = None

    def legal_moves(self):
        return [i for i in range(7) if self.heights[i] < 6]

    def make(self, move):
        row = self.heights[move]
        self.board[move][row] = self.player
        self.heights[move] += 1
        self.last_move = move

        if self.winning_move(move, row):
            self.status = self.player
        elif len(self.legal_moves()) == 0:
            self.status = self.DRAW
        else:
            self.player = self.other(self.player)

    def other(self, player):
        return self.RED if player == self.YELLOW else self.YELLOW

    def unmake(self, move):
        row = self.heights[move] - 1
        self.board[move][row] = self.EMPTY
        self.heights[move] -= 1
        self.player = self.other(self.player)
        self.status = self.ONGOING
        self.last_move = None

    def clone(self):
        clone = ConnectFour()
        clone.board = [col[:] for col in self.board]
        clone.heights = self.heights[:]
        clone.player = self.player
        clone.status = self.status
        clone.last_move = self.last_move
        return clone

    def winning_move(self, col, row):
        player = self.board[col][row]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dx, dy in directions:
            count = 1
            for direction in [1, -1]:
                x, y = col, row
                while 0 <= x + direction * dx < 7 and 0 <= y + direction * dy < 6 and self.board[x + direction * dx][y + direction * dy] == player:
                    count += 1
                    x += direction * dx
                    y += direction * dy
            if count >= 4:
                return True
        return False

    def __str__(self):
        rows = []
        for r in range(5, -1, -1):
            row = ['R' if self.board[c][r] == self.RED else 'Y' if self.board[c][r] == self.YELLOW else '.' for c in range(7)]
            rows.append(" ".join(row))
        return "\n".join(rows)

class MCTSPlayer:
    def __init__(self, simulations=1000, exploration_weight=2):
        self.simulations = simulations
        self.exploration_weight = exploration_weight

    def choose_move(self, game):
        root = MCTSNode(game.clone())
        for _ in range(self.simulations):
            node = self._select(root)
            result = self._simulate(node.state)
            self._backpropagate(node, result)

        best_child = root.get_best_child()
        return best_child.state.last_move

    def _select(self, node):
        while not node.state.status in [ConnectFour.RED_WIN, ConnectFour.YELLOW_WIN, ConnectFour.DRAW]:
            if len(node.children) < len(node.state.legal_moves()):
                return self._expand(node)
            else:
                node = self._uct_select(node)
        return node

    def _uct_select(self, node):
        best_value = -float('inf')
        best_child = None
        for child in node.children:
            uct_value = child.value / (child.visits + 1) + self.exploration_weight * math.sqrt(math.log(node.visits + 1) / (child.visits + 1))
            if uct_value > best_value:
                best_value = uct_value
                best_child = child
        return best_child

    def _expand(self, node):
        legal_moves = node.state.legal_moves()
        for move in legal_moves:
            child = node.clone()
            child.state.make(move)
            node.add_child(child)
        return node.children[-1]

    def _simulate(self, game):
        while game.status == ConnectFour.ONGOING:
            legal_moves = game.legal_moves()
            if game.player == ConnectFour.YELLOW:
                for move in legal_moves:
                    temp_game = game.clone()
                    temp_game.make(move)
                    if temp_game.status == ConnectFour.YELLOW_WIN:
                        game.make(move)
                        break
                else:
                    for move in legal_moves:
                        temp_game = game.clone()
                        temp_game.make(move)
                        if temp_game.status == ConnectFour.RED_WIN:
                            game.make(move)
                            break
                    else:
                        game.make(random.choice(legal_moves))
            else:
                for move in legal_moves:
                    temp_game = game.clone()
                    temp_game.make(move)
                    if temp_game.status == ConnectFour.RED_WIN:
                        game.make(move)
                        break
                else:
                    game.make(random.choice(legal_moves))
        return game.status

    def _backpropagate(self, node, result):
        while node:
            node.visits += 1
            if result == node.state.player:
                node.value += 1
            elif result == ConnectFour.DRAW:
                node.value += 0.5
            node = node.parent

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_best_child(self):
        best_child = None
        best_value = -float('inf')
        for child in self.children:
            win_rate = child.value / (child.visits + 1)
            if win_rate > best_value:
                best_value = win_rate
                best_child = child
        return best_child

    def clone(self):
        return MCTSNode(self.state.clone(), parent=self)

def main():
    print("Welcome to Connect Four!\n")
    game = ConnectFour()
    mcts_player = MCTSPlayer(simulations=3000)

    while game.status == ConnectFour.ONGOING:
        print(game)
        print(f"\nCurrent Player: {'RED (You)' if game.player == ConnectFour.RED else 'YELLOW (MCTS)'}")

        if game.player == ConnectFour.RED:
            try:
                move = int(input("Enter a column (0-6): "))
                if move not in game.legal_moves():
                    print("Illegal move. Try again.")
                    continue
                game.make(move)
            except ValueError:
                print("Invalid input. Enter a number between 0 and 6.")
            except IndexError:
                print("Move out of bounds. Try again.")
        else:
            move = mcts_player.choose_move(game)
            print(f"MCTS chooses column {move}")
            game.make(move)

    print(game)
    if game.status == ConnectFour.RED:
        print("\nRED (You) wins!")
    elif game.status == ConnectFour.YELLOW:
        print("\nYELLOW (MCTS) wins!")
    else:
        print("\nIt's a draw!")

class ConnectFourGUI:
    def __init__(self, root):
        self.game = ConnectFour()
        self.mcts_player = MCTSPlayer(simulations=3000)
        self.root = root
        self.root.title("Connect Four")
        
        self.buttons = [tk.Button(root, text=f"\u2193", command=lambda c=i: self.make_move(c)) for i in range(7)]
        for i, button in enumerate(self.buttons):
            button.grid(row=0, column=i)
        
        self.cells = [[tk.Label(root, text=" ", width=4, height=2, borderwidth=1, relief="solid", bg="white") for _ in range(6)] for _ in range(7)]
        for c in range(7):
            for r in range(6):
                self.cells[c][r].grid(row=6 - r, column=c)

        self.update_board()

    def update_board(self):
        for c in range(7):
            for r in range(6):
                value = self.game.board[c][r]
                if value == ConnectFour.RED:
                    self.cells[c][r].config(bg="red")
                elif value == ConnectFour.YELLOW:
                    self.cells[c][r].config(bg="yellow")
                else:
                    self.cells[c][r].config(bg="white")

    def make_move(self, column):
        if self.game.status != ConnectFour.ONGOING:
            return

        if column not in self.game.legal_moves():
            messagebox.showerror("Illegal Move", "This column is full. Try another column.")
            return

        # Player's move
        self.game.make(column)
        self.update_board()
        if self.check_game_status():
            return

        # MCTS Player's move
        self.root.after(500, self.mcts_move)

    def mcts_move(self):
        move = self.mcts_player.choose_move(self.game)
        self.game.make(move)
        self.update_board()
        self.check_game_status()

    def check_game_status(self):
        if self.game.status == ConnectFour.RED:
            messagebox.showinfo("Game Over", "You win!")
            return True
        elif self.game.status == ConnectFour.YELLOW:
            messagebox.showinfo("Game Over", "MCTS wins!")
            return True
        elif self.game.status == ConnectFour.DRAW:
            messagebox.showinfo("Game Over", "It's a draw!")
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectFourGUI(root)
    root.mainloop()
