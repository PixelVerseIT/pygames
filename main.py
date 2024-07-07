import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.geometry("400x550")
        self.master.resizable(False, False)
        self.master.configure(bg='#2C3E50')
        
        self.players = ['X', 'O']
        self.current_player = random.choice(self.players)
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.scores = {player: 0 for player in self.players}
        self.ai_mode = False
        
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        # Custom fonts
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        button_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
        status_font = tkfont.Font(family="Helvetica", size=16)
        score_font = tkfont.Font(family="Helvetica", size=14)

        # Title
        title_label = tk.Label(self.master, text="Tic Tac Toe", font=title_font, bg='#2C3E50', fg='#ECF0F1')
        title_label.pack(pady=(20, 10))

        # Status label
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self.master, textvariable=self.status_var, font=status_font, bg='#2C3E50', fg='#ECF0F1')
        self.status_label.pack(pady=10)

        # Game board
        board_frame = tk.Frame(self.master, bg='#34495E', padx=10, pady=10)
        board_frame.pack()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(board_frame, text="", font=button_font, width=3, height=1,
                                               command=lambda row=i, col=j: self.make_move(row, col),
                                               bg='#ECF0F1', activebackground='#BDC3C7')
                self.buttons[i][j].grid(row=i, column=j, padx=3, pady=3)

        # Score display
        score_frame = tk.Frame(self.master, bg='#2C3E50')
        score_frame.pack(pady=10)
        self.score_labels = {}
        for player in self.players:
            label = tk.Label(score_frame, text=f"{player}: 0", font=score_font, bg='#2C3E50', fg='#ECF0F1')
            label.pack(side=tk.LEFT, padx=20)
            self.score_labels[player] = label

        # Control buttons
        control_frame = tk.Frame(self.master, bg='#2C3E50')
        control_frame.pack(pady=10)

        reset_button = tk.Button(control_frame, text="New Game", command=self.reset_game, font=status_font, bg='#3498DB', fg='white', activebackground='#2980B9')
        reset_button.pack(side=tk.LEFT, padx=10)

        self.ai_button_var = tk.StringVar(value="Enable AI")
        ai_button = tk.Button(control_frame, textvariable=self.ai_button_var, command=self.toggle_ai, font=status_font, bg='#E74C3C', fg='white', activebackground='#C0392B')
        ai_button.pack(side=tk.LEFT, padx=10)

    def make_move(self, row, col):
        if self.board[row][col] == "" and not self.game_over:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, 
                                          fg='#E74C3C' if self.current_player == 'X' else '#3498DB',
                                          state=tk.DISABLED)
            
            if self.check_winner():
                self.game_over = True
                self.status_var.set(f"Player {self.current_player} wins!")
                self.scores[self.current_player] += 1
                self.update_score_display()
                self.highlight_winning_line()
            elif all(self.board[i][j] != "" for i in range(3) for j in range(3)):
                self.game_over = True
                self.status_var.set("It's a tie!")
            else:
                self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
                self.status_var.set(f"Player {self.current_player}'s turn")
                if self.ai_mode and self.current_player == 'O':
                    self.master.after(500, self.ai_move)

    def check_winner(self):
        lines = (
            ((0,0), (0,1), (0,2)),
            ((1,0), (1,1), (1,2)),
            ((2,0), (2,1), (2,2)),
            ((0,0), (1,0), (2,0)),
            ((0,1), (1,1), (2,1)),
            ((0,2), (1,2), (2,2)),
            ((0,0), (1,1), (2,2)),
            ((0,2), (1,1), (2,0))
        )
        for line in lines:
            if self.board[line[0][0]][line[0][1]] == self.board[line[1][0]][line[1][1]] == self.board[line[2][0]][line[2][1]] != "":
                self.winning_line = line
                return True
        return False

    def highlight_winning_line(self):
        for i, j in self.winning_line:
            self.buttons[i][j].config(bg='#2ECC71')

    def update_score_display(self):
        for player in self.players:
            self.score_labels[player].config(text=f"{player}: {self.scores[player]}")

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.current_player = random.choice(self.players)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state=tk.NORMAL, bg='#ECF0F1')
        self.status_var.set(f"Player {self.current_player}'s turn")
        if self.ai_mode and self.current_player == 'O':
            self.master.after(500, self.ai_move)

    def toggle_ai(self):
        self.ai_mode = not self.ai_mode
        self.ai_button_var.set("Disable AI" if self.ai_mode else "Enable AI")
        if self.ai_mode and self.current_player == 'O':
            self.master.after(500, self.ai_move)

    def ai_move(self):
        if not self.game_over:
            empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
            if empty_cells:
                row, col = random.choice(empty_cells)
                self.make_move(row, col)

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()