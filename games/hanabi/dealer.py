from utils import init_deck
from games.base import Dealer

class HanabiDealer(Dealer):
    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_deck()
        self.shuffle()
    def shuffle(self):
        self.np_random.shuffle(self.deck)
    def deal_cards(self, player, num):
        for _ in range(num):
            player.hand.append(self.deck.pop())