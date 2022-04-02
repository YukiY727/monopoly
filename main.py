# %%
from __future__ import annotations

from typing import Dict, Iterable

# Streetごとの家の賃貸料変化表
# 行：Street番号, 列：[rent_1_house, rent_2_house, rent_3_house, rent_4_house, rent_hotel]
rental_price_matrix = [
    [4, 20, 60, 180, 320, 450],  # BALTIC
    [2, 10, 30, 90, 160, 250],  # MEDITERRANEAN
    [6, 30, 90, 270, 400, 550],  # ORIENTAL
    [6, 30, 90, 270, 400, 550],  # VERMONT
    [8, 40, 100, 300, 450, 600],  # CONNRCTICUT
    [10, 50, 150, 450, 625, 750],  # ST.CHARLES
    [10, 50, 150, 450, 625, 750],  # STATES
    [12, 60, 180, 500, 700, 900],  # VIRGINIA
    [16, 80, 220, 600, 800, 1000],  # NEW YORK
    [14, 70, 200, 550, 750, 950],  # TENNESSEE
    [14, 70, 200, 550, 750, 950],  # ST.JAMES
    [18, 90, 250, 700, 875, 1050],  # INDIANA
    [20, 100, 300, 750, 925, 1100],  # ILLINOIS
    [18, 90, 250, 700, 875, 1050],  # KENTUCKY
    [24, 120, 360, 850, 1025, 1200],  # MARVIN
    [22, 110, 330, 800, 975, 1150],  # ATLANTIC
    [22, 110, 330, 800, 975, 1150],  # VENTNOR
    [28, 150, 450, 1000, 1200, 1400],  # PENNSYLVANIA
    [26, 130, 390, 900, 1100, 1275],  # NORTH CAROLINA
    [26, 130, 390, 900, 1100, 1275],  # PACIFIC
    [35, 175, 500, 1100, 1300, 1500],  # PARK
    [50, 200, 600, 1400, 1700, 2000]  # BOARDWALK
]
streets = ('baltic', 'mediterranean', 'oriental', 'vermont', 'connrcticut',
           'st.charles', 'states', 'virginia', 'new york', 'tennessee', 'st.james',
           'indiana', 'illinois', 'kentucky', 'marvin', 'atlantic', 'ventnor',
           'pennsylvania', 'north caroliana', 'pacific', 'park', 'boardwalk')

street_to_idx = {}
for idx, street in enumerate(streets):
    street_to_idx[street] = idx


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
        self.buildings: list[Street] = []
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
    # TODO: Landと実装を合わせる
    def __init__(self, color: str, name: str, price: int):
        """
        color: 通りのカードの色
        name: 通りの名前
        price: 通りの値段
        """
        super().__init__(name, price)
        self.num_houses = 0
        self.num_hotels = 0
        self.color = color
        self.name = name.lower()
        street_idx = street_to_idx[self.name]
        self.rental_price_idx = 0
        self.rental_prices = rental_price_matrix[street_idx]

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
            # TODO: 家の数でレンタル料変わるようにする
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
        monopolied = (len(owners) == 1 and not None in owners)
        # その土地とほかの土地の建物数の差が1以下なら購入可能
        num_houses = [street.num_houses for street in self.streets]
        num_hotels = [street.num_hotels for street in self.streets]
        is_valid_nums = max(num_houses) - min(num_houses) <= 1 and max(
            num_hotels) - min(num_hotels) <= 1
        can_buy = monopolied and is_valid_nums
        return can_buy


# TODO:実行スクリプトを作ってみる(建物の数につじつまを合わせて購入)


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

# %%
