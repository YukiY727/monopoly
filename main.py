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


class Land:

    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price
        self.is_own = False
        self.owner = None
        self.is_mortgage = False

    def be_bought(self, plyer: Player, board: Board):
        answer = query_yes_no(f'Would you buy this land for {self.price} ?<>')
        if answer:
            plyer.land.append()
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
                self.is_own = True
                self.owner.money -= auction_price
                break
    def cancel_mortgage(self):
        self.is_mortgage = False
        self.is_own = True
        self.owner.money -= round(self.price / 2 * 1.1)
        


class Player:

    def __init__(self, name: str):
        self.name = name
        self.land = []
        self.money = 1500


# class Building:
#     def __init__(self):

# class Train:
#     def __init__(self):

# class Waterworks:
#     def __init__(self):

# class Electric:
#     def __init__(self):

# class Chance:
#     def __init__(self):

# class Pool:
#     def __init__(self):

# %%
# test
yusaku = Player('yusaku')
takeshun = Player('takeshun')
board = Board([yusaku, takeshun])
land = Land('test', 200)
#%%
land.be_bought(yusaku, board)