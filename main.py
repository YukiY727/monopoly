# %%
from __future__ import annotations

import sys


def query_yes_no(question, default="yes"):
    """_summary_
    Args:
        question (str): 標準出力する質問文
        default (str, optional): 回答のデフォルト. Defaults to "yes".
    Raises:
        ValueError: 変数defaultにNone, "yes", "no"以外の値が入ったときのエラー
    Returns:
        bool: 質問への回答yes/noをTrue/Falseとして返す
    """
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
        if "yes".startswith(choice):
            return True
        elif "no".startswith(choice):
            return False
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
            while username not in board.members_name:
                print('Please enter the correct username')
                username = input('Enter your name: ')
            #競売のコード


class Player:
    def __init__(self, name: str):
        self.name = name
        self.land  = []
        self.money = 1500


# class Building:
#     def __init__(self):


# class Train:
#     def __init__(self):

class publiccompany:
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price
        self.is_own = False
        self.owner = None
    # class Land を入れる(売買と競売について)(ownerとis_ownの記述を書く)
    def rental(self, plyer: Player ):
        if self.is_own == False and self.owner != None:
            rental_cost = # 所有数による場合分け、チャンスカードできた場合の場合分け
            plyer.money -= rental_cost
            self.owner.money += rental_cost

            

# class Chance:
#     def __init__(self):

# class Pool:
#     def __init__(self):

def yes_no_input():
    while True:
        choice = input("Please respond with 'yes' or 'no' [y/N]: ").lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False

yes_no_input()

query_yes_no('ok')

sys.stdout.write("**")
