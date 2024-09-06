from games.base import Game
import numpy as np

class HanabiGame(Game):
    def __init__(self, num_players):
        self.np_random = np.random
        self.num_players = num_players
    
    def init_game(self):
        pass
    def step(self, action):
        pass
    def get_state(self):
        pass
    def get_legal_actions(self):
        pass
    def get_num_players(self):
        return self.num_players
    def get_player_id(self):
        self.round.current_player_id