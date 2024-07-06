import tkinter as tk
from tkinter import font as tkfont

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.geometry("300x400")
        self.master.resizable(False, False)
        
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        # Custom fonts
        button_font = tkfont.Font(family="Arial", size=24, weight="bold")
        status_font = tkfont.Font(family="Arial", size=16)

        # Status label
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self.master, textvariable=self.status_var, font=status_font, bg='#f0f0f0', pady=10)
        self.status_label.pack(fill=tk.X)

        # Game board
        board_frame = tk.Frame(self.master, bg='#d0d0d0')
        board_frame.pack(padx=10, pady=10)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(board_frame, text="", font=button_font, width=3, height=1,
                                               command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2)

        # Reset button
        reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_game, font=status_font)
        reset_button.pack(pady=10)

    def make_move(self, row, col):
        if self.board[row][col] == "" and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state=tk.DISABLED, 
                                          disabledforeground='black' if self.current_player == 'X' else 'red')
            
            if self.check_winner():
                self.status_var.set(f"Player {self.current_player} wins!")
                self.disable_all_buttons()
            elif all(self.board[i][j] != "" for i in range(3) for j in range(3)):
                self.status_var.set("It's a tie!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_var.set(f"Player {self.current_player}'s turn")

    def check_winner(self):
        for i in range(3):
            if (self.board[i][0] == self.board[i][1] == self.board[i][2] != "" or
                self.board[0][i] == self.board[1][i] == self.board[2][i] != ""):
                return True
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != "" or
            self.board[0][2] == self.board[1][1] == self.board[2][0] != ""):
            return True
        return False

    def disable_all_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)

    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state=tk.NORMAL)
        self.status_var.set("Player X's turn")

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()