from games.base import Round
class HanabiRound(Round):
    def __init__(self, dealer, num_players, np_random):
        self.np_random = np_random
        self.dealer = dealer
        self.current_player = 0
        self.num_players = num_players
        self.played_cards = []
        self.is_over = False

    def proceed_round(self, player, target_player, action):
        pass
    def get_legal_actions(self):
        pass
    def get_state(self):
        pass
    