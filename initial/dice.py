"""
# Dice game
"""


import random
import time


def dice():
    t = 0.5

    player = random.randint(1, 6)
    print("You rolled...", player, sep=3*'\t')

    ai = random.randint(1, 6)
    print("The computer rolls", end='')
    for i in range(3):
        time.sleep(t)
        print(".", end='')
    time.sleep(t)
    print('\t', ai, sep='')

    if player > ai:
        print("You win! \U0001F973")
    elif player == ai:
        print("Tie game! \U0001F610")
    else:
        print("You lose! \U0001F62C")


def another() -> bool:
    while True:
        print("Quit? Y/N")
        answer = input().lower()

        if answer == "y":
            return False
        elif answer == "n":
            return True
        else:
            print("I did not understand that. \U0001F914")


def main():
    go = True

    while go:
        dice()
        go = another()
        print()

    print("Thank you for playing. \U0001F596")


if __name__ == '__main__':
    main()
