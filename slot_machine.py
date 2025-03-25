import os
import time
import random

clear_console = lambda: os.system('cls') if os.name == 'nt' else os.system('clear')
format_money = lambda money: "${:.{}f}".format(money, 2)

def display_slot_machine(emojis):
    for _ in range(15):
        clear_console()
        selected_emojis = [random.choice(emojis) for _ in range(3)]
        print(" |".join(selected_emojis))
        time.sleep(0.15)
    return selected_emojis

def get_bet(money, previous_bet):
    while True:
        bet_input = input(f"How much would you like to bet? (Available: {format_money(money)}) Input a number or percentage: ")
        if bet_input == "":
            if previous_bet is None:
                print(f"Invalid input. You must place an initial bet. (Available: {format_money(money)})")
                continue
            else:
                bet = previous_bet
                print(f"Using previous bet: {format_money(bet)}")
                return bet
        try:
            bet = float(bet_input[:-1]) / 100 * money if bet_input[-1] == "%" else float(bet_input[1:]) if bet_input[0] == "$" else float(bet_input)
            if bet <= 0: 
                print(f"Invalid bet. Please enter a valid bet. (Available: {format_money(money)})")
                clear_console()
            elif bet > money:
                print(f"Insufficient funds. Please enter a valid bet. (Available: {format_money(money)})")
                clear_console()
            else:
                return bet
        except:
            print("Invalid input. Please enter a number.")

def welcome_message():
    print("Welcome to the slot machine game! You start with $1000. The emojis are as follows:")
    print("🍆 🍀 🎲 💰 💸 🍒 🍐 🍊")
    print("Match 3 emojis to win 5x your bet. Match 2 emojis to win 2x your bet.")
    input("Press enter to start. ")
    clear_console()

def play_game():
    money = 1000
    emojis = ["🍆", "🍀", "🎲", "💰", "💸", "🍒", "🍐", "🍊"]
    previous_bet = None

    while money > 0 and format_money(money) != "$0.00":
        clear_console()
        bet = get_bet(money, previous_bet)
        money -= bet
        selected_emojis = display_slot_machine(emojis)
        winnings = bet * (5 if selected_emojis[0] == selected_emojis[1] == selected_emojis[2] else 2 if len(set(selected_emojis)) == 2 else 0)
        money += winnings

        if winnings > 0:
            print(f"You won {format_money(winnings)}! Your new balance is {format_money(money)}.")
        else:
            print(f"You did\'t win anything. You now have {format_money(money)}.")

        previous_bet = bet
        input("Press enter to continue. ")
    
    print("You have run out of money. Game over.")

if __name__ == "__main__":
    welcome_message()
    while True:
        play_game()
        if input("Would you like to play again? (y/n) ").lower() != "y":
            break
