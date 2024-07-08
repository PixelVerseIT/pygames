import tkinter as tk
from tkinter import messagebox
import random

class MemoryGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Memory Card Game")
        self.master.geometry("400x450")
        
        self.symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.board_size = 16
        self.buttons = []
        self.cards = []
        self.revealed = []
        self.first_card = None
        self.matches = 0
        self.attempts = 0

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack(pady=20)

        self.info_label = tk.Label(self.master, text="Attempts: 0 | Matches: 0")
        self.info_label.pack(pady=10)

        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game)
        self.new_game_button.pack(pady=10)

        for i in range(self.board_size):
            button = tk.Button(self.game_frame, text="", width=5, height=2,
                               command=lambda x=i: self.on_card_click(x))
            button.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.buttons.append(button)

    def new_game(self):
        self.cards = list(self.symbols[:self.board_size//2] * 2)
        random.shuffle(self.cards)
        self.revealed = [False] * self.board_size
        self.first_card = None
        self.matches = 0
        self.attempts = 0
        self.update_info_label()

        for button in self.buttons:
            button.config(text="", state=tk.NORMAL)

    def on_card_click(self, index):
        if self.revealed[index]:
            return

        self.buttons[index].config(text=self.cards[index])
        self.revealed[index] = True

        if self.first_card is None:
            self.first_card = index
        else:
            self.attempts += 1
            if self.cards[self.first_card] == self.cards[index]:
                self.matches += 1
                if self.matches == self.board_size // 2:
                    messagebox.showinfo("Congratulations!", f"You won in {self.attempts} attempts!")
                    self.new_game()
            else:
                self.master.after(1000, self.hide_cards, self.first_card, index)
            self.first_card = None

        self.update_info_label()

    def hide_cards(self, index1, index2):
        self.buttons[index1].config(text="")
        self.buttons[index2].config(text="")
        self.revealed[index1] = False
        self.revealed[index2] = False

    def update_info_label(self):
        self.info_label.config(text=f"Attempts: {self.attempts} | Matches: {self.matches}")

def main():
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()