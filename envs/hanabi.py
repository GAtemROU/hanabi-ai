from games.hanabi.game import HanabiGame 
from envs.env import Env   

DEFAULT_GAME_CONFIG = {
        'game_num_players': 2,
    }

class HanabiEnv(Env):
    def __init__(self, config={}):
        self.name = 'hanabi'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = HanabiGame()
        super().__init__(config)
        # self.state_shape = [[4, 4, 15] for _ in range(self.num_players)]
        # self.action_shape = [None for _ in range(self.num_players)]
