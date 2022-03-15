# %%
from __future__ import annotations

import sys


def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

class Board:
    def __init__(self, members: list[Player]):
        self.members = members
        self.members_name = [member.name for member in members]

class Land:
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price
        self.is_own = False
        self.owner = None

    def be_bought(self, plyer: Player ):
        answer = query_yes_no(f'Would you buy this land for {self.price} ?')
        if answer:
            plyer.land.append()
            plyer.money -= self.price
        else:
            self.auction()
    def auction(self, board: Board):
        while True:
            sys.stdout.write(f'{self.name} is now for sale. Please include your user name and  the amount you can offer')
            username = input('Enter your name: ')
            while username in board.members_name:
                print('Please enter the correct username')


class Player:
    def __init__(self, name: str):
        self.name = name
        self.land  = []
        self.money = 1500


class Building:
    def __init__(self):


class Train:
    def __init__(self):

class Waterworks:
    def __init__(self):

class Electric:
    def __init__(self):

class Chance:
    def __init__(self):

class Pool:
    def __init__(self):
#%%
def yes_no_input():
    while True:
        choice = input("Please respond with 'yes' or 'no' [y/N]: ").lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
yes_no_input()
# %%
query_yes_no('ok')
# %%
