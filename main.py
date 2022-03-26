# %%
from __future__ import annotations

from typing import Dict, Iterable


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

    def giveup_or_continue(self):
        if self.land:
            put_in_mortgage = query_yes_no('Would you put your land to mortgage?')
            if put_in_mortgage:
                pass
                # TODO:continueする処理
        else:
            pass
            # TODO:やめる処理の追加


class Street(Land):

    def __init__(self, color: str, name: str, price: int,
                 rental_price_house: Iterable(int), rental_price_hotel: int):
        """
        color: 通りのカードの色
        name: 通りの名前
        price: 通りの値段
        rental_price_house: 家の個数に対する通行料
        rental_price_hotel: ホテルの個数に対する通行料
        """
        super().__init__(name, price)
        self.num_houses = 0
        self.num_hotels = 0
        self.color = color
        self.rental_price = {
            'house': rental_price_house,
            'hotel': rental_price_hotel
        }

    def add_building(self):
        if self.num_houses <= 4:
            self.num_houses += 1

        else:
            self.num_houses = 0
            self.num_hotels += 1

    def charge_rental(self, player: Player):
        if self.num_hotels:
            rental_price = self.rental_price['hotel']
        else:
            rental_price = self.rental_price['house']
        player.money -= rental_price
        print(f'charged {rental_price} to {player.name}!')

    def show_state(self):
        print(f'houses: {self.num_houses}')
        print(f'hotels: {self.num_hotels}')


class Color():

    def __init__(self, streets: Iterable[Street]):
        self.streets = streets
        self.color = None

    def can_buy_building(self, street_name: str):
        street_names = [street.name for street in self.streets]
        if not street_name in street_names:
            raise ValueError('不正なstreet名')
        owners = set(street.owner for street in self.streets)
        monopolied = len(owners) == 1 and not None in owners
        # その土地とほかの土地の建物数の差が1以下なら購入可能
        num_houses = [street.num_houses for street in self.streets]
        num_hotels = [street.num_hotels for street in self.streets]
        is_valid_nums = max(num_houses) - min(num_houses) <= 1 and max(
            num_hotels) - min(num_hotels) <= 1
        can_buy = monopolied and is_valid_nums
        return can_buy


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
<<<<<<< HEAD
street1 = Street('red', 'test1', 200, 50)
street2 = Street('red', 'test2', 100, 25)

street1.owner = yusaku
street2.owner = takeshun
color = Color([street1, street2])
if color.can_buy_building('test1'):
    print('can_buy')
else:
    print('can\'t buy')
street2.owner = yusaku
if color.can_buy_building('test1'):
    print('can_buy')

=======


# land = Land('test', 200, 50)
train1 = Train('train1', 'train')
train2 = Train('train2','train')
#%%
>>>>>>> 61bf11346d7ceb3b243652cc6130937a7a15d0ba
# land.be_bought(yusaku, board)
train1.be_bought(yusaku, board)
train2.be_bought(yusaku, board)
train1.charge_rental(takeshun)
# %%
