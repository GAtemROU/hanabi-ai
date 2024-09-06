from games.hanabi.utils import init_deck
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
    def draw_card(self, player):
        if len(self.deck) == 0:
            return 0
        player.hand.append(self.deck.pop())
        return self.cards_left()
    def cards_left(self):
        return len(self.deck)