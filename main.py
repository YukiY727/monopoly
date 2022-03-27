
# %%
from __future__ import annotations
from multiprocessing.connection import answer_challenge
from random import random

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
        self.cell = (
            Go,
            Street(),
            Pool(),
            Street(),
            Incometax(),
            Train(),
            Street(),
            Chance(),
            Street(),
            Street(),
            Jail(),
            Street(),
            Public(),
            Street(),
            Street(),
            Train(),
            Street(),
            Pool(),
            Street(),
            Street(),
            Park(),
            Street(),
            Chance(),
            Street(),
            Street(),
            Train(),
            Street(),
            Street(),
            Public(),
            Street(),
            Gojail(),
            Street(),
            Street(),
            Pool(),
            Street(),
            Train(),
            Chance(),
            Street(),
            Luxurytax(),
            Street(),
        )

class Go: # スタート、ゴール

    def __init__(self):
        self.name = 'Go'

    def __call__(self, player: Player, board: Board):
        player.money += 200

class Incometax:  # 税金
    def __init__(self):
        self.name = 'Income tax'

    def __call__(self, player: Player, board: Board):
        player.money -= 200

class Luxurytax:  # 税金
    def __init__(self):
        self.name = 'Luxury tax'

    def __call__(self, player: Player, board: Board):
        player.money -= 100

class Land:

    def __init__(self, name: str, price: int, rental_price: int, kind: str):
        self.name = name
        self.price = price
        self.is_own = False
        self.owner = None
        self.is_mortgage = False
        self.rental_price = rental_price
        self.kind = kind

    def __call__(self, player: Player, board: Board):
        if self.owner:
            self.charge_rental(player)
        else:
            self.be_bought(player, board)


    def be_bought(self, player: Player, board: Board):
        answer = query_yes_no(f'Would you buy this land for {self.price} ?')
        if answer:
            if self.kind == 'building':
                player.buildings.append(self)
            elif self.kind == 'train':
                player.train.append(self)
            elif self.kind == 'public_business':
                player.public_business.append(self)
            self.owner = player
            player.money -= self.price
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
            continue_auction = query_yes_no(f'Is there anyone who buys {self.name} at a higher price?\n')
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
        self.public_business: list[Public] = []
        self.money: int = 1500
        self.zorome: int = 0
        self.dice: int = 0

    def throw_dice(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        self.dice = dice1 + dice2
        if dice1 == dice2:
            self.zorome += 1
        else:
            self.zorome = 0
        
        if self.zorome == 3:  # ゾロ目連続3回で刑務所
            jail()


# class Street:
#     def __init__(self):

class Train(Land):

    def __init__(self, name: str, kind: str):
        super().__init__(name, 200, 50, kind)

    def be_bought(self, player: Player, board: Board):
        super().be_bought(player, board)
        for owner_train in self.owner.train:
            owner_train.change_rental()

    def change_rental(self):
        self.rental_price = 50 * len(self.owner.train)


class Public(Land):

    def __init__(self, name: str, price: int, kind: str):
        super().__init__(name, price, 0, kind)

    def __call__(self, player: Player, board: Board):
        if self.owner:
            self.pay_rental(player)
        else:
            self.be_bought(player, board)

    def be_bought(self, plyer: Player, board: Board):
        super().be_bought(plyer, board)

    def auction(self, board: Board):
        super().be_bought(board)

    def cancel_mortgage(self):
        super().cancel_mortgage()
        
    def put_in_mortgage(self):
        super().put_in_mortgage()

    def pay_rental(self, user: Player):
        dice = user.dice
        #if chance:
        #    self.rental_price = dice * 10
        #else:
        if len(self.owner.public_business) == 2:  # ElectricとWaterworksの所有者が同じ  
            self.rental_price = dice * 10
        elif len(self.owner.public_business) == 1: # どちらか一つ所有
            self.rental_price = dice * 4
        user.money -= self.rental_price
        self.owner.money += self.rental_price

# class Chance:
#     def __init__(self):

# class Pool:
#     def __init__(self):

class jail:  
        
    def jail_in(self, player: Player):
        self.count = 0

        answer1 = query_yes_no(f'Would you use (or buy) card and exit the jail ?')
            
        if answer1: # カードの使用
            player.money += 0
            # 釈放

        answer2 = query_yes_no(f'Would you pay $50 and exit the jail ?')

        if answer2: # サイコロを振る前に50$払う
            player.money -= 50
            # 釈放
        else: # diceを振る　# 3ターン以内にゾロ目を出す。出なかったら強制50$支払い
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            if dice1 == dice2:
                player.money += 0
                 #釈放　
            else:
                self.count += 1
           
        if self.count == 3:
            player.money -= 50
            # 釈放



# test
yusaku = Player('yusaku')
takeshun = Player('takeshun')
board = Board([yusaku, takeshun])

water = Public('test1', 200, 'public_business')
elect = Public('test2', 200, 'public_business')

water.be_bought(yusaku, board)
elect.be_bought(yusaku, board)

water.pay_rental(takeshun)