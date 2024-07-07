import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board(size):
    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cards = list(symbols[:size//2] * 2)
    random.shuffle(cards)
    return cards

def print_board(board, revealed):
    for i in range(len(board)):
        if revealed[i]:
            print(f" {board[i]} ", end='')
        else:
            print(f" {i:2d}", end='')
        if (i + 1) % 4 == 0:
            print()
    print()

def get_card_input(prompt, board_size, revealed, other_card=None):
    while True:
        try:
            card = int(input(prompt))
            if 0 <= card < board_size and not revealed[card] and card != other_card:
                return card
            print("Invalid input. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def play_game():
    board_size = 16  # Must be even
    board = create_board(board_size)
    revealed = [False] * board_size
    attempts = 0
    matches = 0

    while matches < board_size // 2:
        clear_screen()
        print(f"Attempts: {attempts}, Matches: {matches}")
        print_board(board, revealed)
        
        card1 = get_card_input("Enter the position of the first card: ", board_size, revealed)
        revealed[card1] = True
        
        clear_screen()
        print(f"Attempts: {attempts}, Matches: {matches}")
        print_board(board, revealed)
        
        card2 = get_card_input("Enter the position of the second card: ", board_size, revealed, card1)
        revealed[card2] = True
        
        clear_screen()
        print(f"Attempts: {attempts}, Matches: {matches}")
        print_board(board, revealed)

        attempts += 1

        if board[card1] == board[card2]:
            print("Match found!")
            matches += 1
        else:
            print("No match. Try again.")
            revealed[card1] = False
            revealed[card2] = False
        
        input("Press Enter to continue...")

    print(f"Congratulations! You completed the game in {attempts} attempts.")

def main():
    while True:
        play_game()
        if input("Play again? (y/n): ").lower() != 'y':
            break
    print("Thanks for playing!")

if __name__ == "__main__":
    main()