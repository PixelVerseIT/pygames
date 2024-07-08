import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import json
import os

class MemoryGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Memory Card Game")
        self.master.geometry("600x700")
        
        self.symbols = '🐶🐱🐭🐹🐰🦊🐻🐼🐨🐯🦁🐮🐷🐸🐵🐔🐧🐦🐤🦆🦅🦉🦇🐺🐗🐴🦄🐝🐛🦋🐌🦎🦖🦕🦍🦓🦒🐘🦏🦛🐂🐃🦌🐎🐖🐑🐏🐐🐪'
        self.board_sizes = {
            'Easy': 16,
            'Medium': 24,
            'Hard': 36,
            'Expert': 64
        }
        self.board_size = self.board_sizes['Easy']
        self.buttons = []
        self.cards = []
        self.revealed = []
        self.first_card = None
        self.matches = 0
        self.attempts = 0
        self.start_time = None
        self.timer_running = False
        self.pause_time = 0
        self.high_scores = self.load_high_scores()

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 14))
        self.style.configure('Game.TButton', font=('Helvetica', 18))

        self.menu_frame = ttk.Frame(self.master, padding="10")
        self.menu_frame.pack(fill='x')

        self.new_game_button = ttk.Button(self.menu_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(side='left', padx=(0, 10))

        self.difficulty_var = tk.StringVar(value='Easy')
        self.difficulty_menu = ttk.OptionMenu(self.menu_frame, self.difficulty_var, 'Easy', *self.board_sizes.keys(), command=self.change_difficulty)
        self.difficulty_menu.pack(side='left', padx=(0, 10))

        self.pause_button = ttk.Button(self.menu_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(side='left', padx=(0, 10))

        self.high_scores_button = ttk.Button(self.menu_frame, text="High Scores", command=self.show_high_scores)
        self.high_scores_button.pack(side='left')

        self.info_frame = ttk.Frame(self.master, padding="10")
        self.info_frame.pack(fill='x')

        self.attempts_label = ttk.Label(self.info_frame, text="Attempts: 0")
        self.attempts_label.pack(side='left', padx=(0, 10))

        self.matches_label = ttk.Label(self.info_frame, text="Matches: 0")
        self.matches_label.pack(side='left', padx=(0, 10))

        self.timer_label = ttk.Label(self.info_frame, text="Time: 00:00")
        self.timer_label.pack(side='left')

        self.game_frame = ttk.Frame(self.master, padding="10")
        self.game_frame.pack(expand=True, fill='both')

    def new_game(self):
        self.board_size = self.board_sizes[self.difficulty_var.get()]
        self.cards = list(self.symbols[:self.board_size//2] * 2)
        random.shuffle(self.cards)
        self.revealed = [False] * self.board_size
        self.first_card = None
        self.matches = 0
        self.attempts = 0
        self.start_time = time.time()
        self.timer_running = True
        self.pause_time = 0
        self.update_timer()
        self.update_info_labels()

        for widget in self.game_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        rows = int(self.board_size**0.5)
        cols = self.board_size // rows
        for i in range(self.board_size):
            button = ttk.Button(self.game_frame, text="", width=3, style='Game.TButton',
                                command=lambda x=i: self.on_card_click(x))
            button.grid(row=i // cols, column=i % cols, padx=2, pady=2, sticky='nsew')
            self.buttons.append(button)

        for i in range(rows):
            self.game_frame.grid_rowconfigure(i, weight=1)
        for i in range(cols):
            self.game_frame.grid_columnconfigure(i, weight=1)

    def on_card_click(self, index):
        if not self.timer_running or self.revealed[index]:
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
                    self.timer_running = False
                    elapsed_time = time.time() - self.start_time - self.pause_time
                    self.update_high_scores(elapsed_time)
                    messagebox.showinfo("Congratulations!", f"You won in {self.attempts} attempts and {self.format_time(elapsed_time)}!")
                    self.new_game()
            else:
                self.master.after(1000, self.hide_cards, self.first_card, index)
            self.first_card = None

        self.update_info_labels()

    def hide_cards(self, index1, index2):
        self.buttons[index1].config(text="")
        self.buttons[index2].config(text="")
        self.revealed[index1] = False
        self.revealed[index2] = False

    def update_info_labels(self):
        self.attempts_label.config(text=f"Attempts: {self.attempts}")
        self.matches_label.config(text=f"Matches: {self.matches}")

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time - self.pause_time
            self.timer_label.config(text=f"Time: {self.format_time(elapsed_time)}")
            self.master.after(1000, self.update_timer)

    def format_time(self, seconds):
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes:02d}:{seconds:02d}"

    def change_difficulty(self, _):
        self.new_game()

    def toggle_pause(self):
        if self.timer_running:
            self.timer_running = False
            self.pause_start_time = time.time()
            self.pause_button.config(text="Resume")
            for button in self.buttons:
                button.config(state='disabled')
        else:
            self.timer_running = True
            self.pause_time += time.time() - self.pause_start_time
            self.pause_button.config(text="Pause")
            for button in self.buttons:
                button.config(state='normal')
            self.update_timer()

    def load_high_scores(self):
        if os.path.exists('high_scores.json'):
            with open('high_scores.json', 'r') as f:
                return json.load(f)
        return {difficulty: [] for difficulty in self.board_sizes.keys()}

    def save_high_scores(self):
        with open('high_scores.json', 'w') as f:
            json.dump(self.high_scores, f)

    def update_high_scores(self, time):
        difficulty = self.difficulty_var.get()
        score = (time, self.attempts)
        self.high_scores[difficulty].append(score)
        self.high_scores[difficulty].sort(key=lambda x: (x[0], x[1]))
        self.high_scores[difficulty] = self.high_scores[difficulty][:5]
        self.save_high_scores()

    def show_high_scores(self):
        high_scores_window = tk.Toplevel(self.master)
        high_scores_window.title("High Scores")

        notebook = ttk.Notebook(high_scores_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        for difficulty in self.board_sizes.keys():
            frame = ttk.Frame(notebook, padding="10")
            notebook.add(frame, text=difficulty)

            ttk.Label(frame, text="Time").grid(row=0, column=0, padx=5, pady=5)
            ttk.Label(frame, text="Attempts").grid(row=0, column=1, padx=5, pady=5)

            for i, (time, attempts) in enumerate(self.high_scores[difficulty], start=1):
                ttk.Label(frame, text=self.format_time(time)).grid(row=i, column=0, padx=5, pady=2)
                ttk.Label(frame, text=str(attempts)).grid(row=i, column=1, padx=5, pady=2)

def main():
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()