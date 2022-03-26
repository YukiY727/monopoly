# %%
from __future__ import annotations


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


class Go:

    def __init__(self):
        self.name = 'Go'

    def __call__(self, player: Player, board: Board):
        player.money += 200

class Incometax:
    def __init__(self):
        self.name = 'Income tax'

    def __call__(self, player: Player, board: Board):
        player.money -= 200
class Luxurytax:
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
        self.is_mortgage = False
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
                player.train.append(self)
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


class Street:

    def __init__(self):
        pass


class Train(Land):

    def __init__(self, name: str, kind: str):
        super().__init__(name, 200, 50, kind)

    def be_bought(self, player: Player, board: Board):
        super().be_bought(player, board)
        for owner_train in self.owner.train:
            owner_train.change_rental()

    def change_rental(self):
        self.rental_price = 50 * len(self.owner.train)


class Public:

    def __init__(self):
        pass


class Chance:

    def __init__(self):
        pass


class Pool:

    def __init__(self):
        pass


# %%
# test
yusaku = Player('yusaku')
takeshun = Player('takeshun')
board = Board([yusaku, takeshun])
# land = Land('test', 200, 50)
train1 = Train('train1', 'train')
train2 = Train('train2', 'train')
#%%
# land(yusaku, board)
# land(takeshun, board)
train1(yusaku, board)
train2(yusaku, board)
train1(takeshun, board)
# %%
