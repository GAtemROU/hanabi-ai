from games.base import Player 
class HanabiPlayer(Player):
    def __init__(self, player_id):
        self.player_id = player_id
        self.hand = []
    def get_player_id(self):
        return self.player_id