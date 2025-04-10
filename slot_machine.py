# import necessary modules, os, time, random which are used for clearing the console, waiting for a certain amount of time, and generating random numbers
import os
import time
import random

# define lambda functions, clear_console clears the terminal, format_money formats the money (which is a parameter) to a string
# eg. format_money(1000) -> "$1000.00"
# format_money was found on Stack Overflow
# https://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
clear_console = lambda: os.system('cls') if os.name == 'nt' else os.system('clear')
format_money = lambda money: "${:.{}f}".format(money, 2)


def display_slot_machine(emojis: list) -> list:
    """Simulates a slot machine spin by randomly selecting emojis."""
    # repeat the spin 15 times to simulate the slot machine and print the selected emojis with a delay of 0.15 seconds between each spin
    for _ in range(15):
        clear_console()
        # randomly select 3 emojis from the list
        selected_emojis = [random.choice(emojis) for _ in range(3)]
        # if the emojis are the same, print them with "!!!" at the end with "|" between them
        # else print them normally with "|" between them
        if selected_emojis[0] == selected_emojis[1] == selected_emojis[2]:
            print(" |".join(selected_emojis) + " !!!")
        else:
            print(" |".join(selected_emojis))
        time.sleep(0.15)

    return selected_emojis 

def get_bet(money: float, previous_bet: float) -> tuple:
    """Prompts the user for a bet amount, supporting raw values and percentages."""
    # loop until a valid bet is entered
    while True:
        # get the bet input from the user
        bet_input = input(f"How much would you like to bet? (Available: {format_money(money)}) Input a number or percentage: ")
        # if the input is empty, use the previous bet
        if bet_input == "":
            # if there is no previous bet, print an error message and continue
            if previous_bet is None:
                print(f"Invalid input. You must place an initial bet. (Available: {format_money(money)})")
                continue
            # if the previous bet is greater than the money, print an error message and continue
            elif previous_bet > money:
                print(f"Invalid input. You don't have enough money for the previous bet of {previous_bet}. (Available: {format_money(money)})")
                continue
            # else use the previous bet
            else:
                bet = previous_bet
                print(f"Using previous bet: {format_money(bet)}")
                return bet
            
        # try to convert the input to a float and calculate the bet amount
        try:
            bet = float(bet_input[:-1]) / 100 * money if bet_input[-1] == "%" else float(bet_input[1:]) if bet_input[0] == "$" else float(bet_input)
            if bet <= 0: 
                print(f"Invalid bet. Please enter a valid bet. (Available: {format_money(money)})")
            elif bet > money:
                print(f"Insufficient funds. Please enter a valid bet. (Available: {format_money(money)})")
            else:
                return bet
        # if the input is not a number, print an error message
        except:
            print("Invalid input. Please enter a number.")

def welcome_message():
    """Displays the welcome message and game instructions."""
    # clear the console and display the welcome message
    clear_console()
    print("Welcome to the slot machine game! You start with $1000. The emojis are as follows:")
    print("🍀 🎲 💰 💸 🍒 🍐")
    print("Match 3 emojis to win 5x your bet. Match 2 emojis to win 2x your bet.")
    input("Press enter to start. ")
    clear_console()

def play_game():
    """Main game loop for the slot machine."""
    # initialize variables
    money = 1000
    emojis = ["🍀", "🎲", "💰", "💸", "🍒", "🍐"]
    previous_bet = None
    win_streak = 0
    highest_balance = money

    # loop until the player runs out of money
    while money > 0 and format_money(money) != "$0.00":
        # clear the console, get the bet amount, and display the slot machine
        clear_console()
        bet = get_bet(money, previous_bet)
        money -= bet
        selected_emojis = display_slot_machine(emojis)

        # calculate the winnings and update the winnings and win streak
        if selected_emojis[0] == selected_emojis[1] == selected_emojis[2]:
            winnings = bet * 5
            win_streak += 1
        elif len(set(selected_emojis)) == 2:
            winnings = bet * 2
            win_streak += 1
        else:
            winnings = 0
            win_streak = 0

        # update the money and print the results
        money += winnings
        highest_balance = max(highest_balance, money)

        # print the results
        if winnings > 0:
            print(f"You won {format_money(winnings)}! Your new balance is {format_money(money)}.")
            print(f"Win streak: {win_streak}")
        else:
            print(f"You did\'t win anything. You now have {format_money(money)}.")

        # update the previous bet and wait for the user to continue
        previous_bet = bet
        input("Press enter to continue. ")
    
    # print the final message
    print(f"You have run out of money. Your highest balance reached was {format_money(highest_balance)}.")

# if the script is run directly, display the welcome message and play the game
if __name__ == "__main__":
    welcome_message()
    while True:
        play_game()
        # ask the user if they want to play again and break if they don't
        if input("Would you like to play again? (y/n) ").lower() != "y":
            break
