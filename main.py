# %%
from __future__ import annotations

from typing import Iterable


def query_yes_no(question, default="yes"):
    """質問(yes/no)の回答をBool値で出力

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
        print(question + prompt)
        choice = input().lower()
        if "yes".startswith(choice):
            return True
        elif "no".startswith(choice):
            return False
        else:
            print("Please respond with 'yes' or 'no' "
                  "(or 'y' or 'n').\n")


class Board:

    def __init__(self, members: list[Player]):
        self.members = members
        self.members_name = [member.name for member in members]
        self.name_member_mapping = {
            name: player
            for name, player in zip(self.members_name, self.members)
        }


class Land:

    def __init__(self, name: str, price: int, rental_price: int, kind: str):
        self.name = name
        self.price = price
        self.is_own = False
        self.owner = None
        self.is_mortgage = False
        self.rental_price = rental_price
        self.is_mortgage = False
        self.kind = kind

    def be_bought(self, plyer: Player, board: Board):
        answer = query_yes_no(f'Would you buy this land for {self.price} ?')
        if answer:
            if self.kind == 'building':
                plyer.buildings.append(self)
            elif self.kind == 'train':
                plyer.train.append(self)
            elif self.kind == 'public_business':
                plyer.train.append(self)
            self.owner = plyer
            plyer.money -= self.price
        else:
            self.auction(board)

    def auction(self, board: Board):
        auction_price = None
        while True:
            print(
                f'{self.name} is now for sale. Please include your user name and the amount you can offer\n'
            )
            username = input('Enter your name: ')
            # TODO:usernameを間違えると'Please enter...が出続ける点の修正'
            while username not in board.members_name:
                username = input('Please enter the correct username')
            user = board.name_member_mapping[username]
            offered_price = int(input("Enter a price you can offer: "))
            if auction_price:
                if offered_price > auction_price:
                    auction_price = offered_price
                    self.owner = user
                else:
                    print(
                        'offered price is not higher than the amount offered before\n'
                    )
            else:
                auction_price = offered_price
                self.owner = user
            print(
                f'{self.name}\'s price is {auction_price} now (offered by {self.owner.name})\n'
            )
            continue_auction = query_yes_no(
                f'Is there anyone who buys {self.name} at a higher price?\n')
            if not continue_auction:
                print(
                    f'{self.name} is bought by {self.owner.name} for {auction_price}!'
                )
                if self.kind == 'building':
                    self.owner.buildings.append(self)
                elif self.kind == 'train':
                    self.owner.train.append(self)
                elif self.kind == 'public_business':
                    self.owner.public_business.append(self)
                self.is_own = True
                self.owner.money -= auction_price
                break

    def cancel_mortgage(self):
        self.is_mortgage = False
        self.is_own = True
        self.owner.money -= round(self.price / 2 * 1.1)

    def put_in_mortgage(self):
        self.owner.money += self.price / 2
        self.is_own = False
        self.is_mortgage = True

    def charge_rental(self, user: Player):
        user.money -= self.rental_price
        self.owner.money += self.rental_price


class Player:

    def __init__(self, name: str):
        self.name = name
        self.train: list[Train] = []
        self.buildings: list[Buildings] = []
        self.train: list[Train] = []
        self.public_business: list[Public] = []
        self.money: int = 1500


class Street(Land):

    def __init__(self, color: str, name: str, price: int, rental_price: int):
        super().__init__(name, price, rental_price)
        self.num_houses = 0
        self.num_hotels = 0
        self.color = color

    def add_building(self):
        if self.num_houses <= 4:
            self.num_houses += 1

        else:
            self.num_houses = 0
            self.num_hotels += 1
        

    def show_state(self):
        print(f'houses: {self.num_houses}')
        print(f'hotels: {self.num_hotels}')


class Color():

    def __init__(self, streets: Iterable[Street]):
        self.streets = streets
        self.color = None



class Train(Land):

    def __init__(self, name: str, kind: str):
        super().__init__(name, 200, 50, kind)

    def be_bought(self, plyer: Player, board: Board):
        super().be_bought(plyer, board)
        for owner_train in self.owner.train:
            owner_train.change_rental()

    def change_rental(self):
        self.rental_price = 50 * len(self.owner.train)


# class Waterworks:
#     def __init__(self):

# class Electric:
#     def __init__(self):

# class Chance:
#     def __init__(self):

# class Pool:
#     def __init__(self):

# test
yusaku = Player('yusaku')
takeshun = Player('takeshun')
board = Board([yusaku, takeshun])


# land = Land('test', 200, 50)
train1 = Train('train1', 'train')
train2 = Train('train2','train')
#%%
# land.be_bought(yusaku, board)
train1.be_bought(yusaku, board)
train2.be_bought(yusaku, board)
train1.charge_rental(takeshun)
# %%
