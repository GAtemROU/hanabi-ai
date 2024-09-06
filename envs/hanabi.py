from games.hanabi.game import HanabiGame 
from collections import OrderedDict
from envs.env import Env   
import numpy as np
# from games.hanabi.utils import encode_hand, encode_target
from games.hanabi.utils import ACTION_SPACE, ACTION_LIST

import games.hanabi.utils as utils

DEFAULT_GAME_CONFIG = {
        'game_num_players': 2,
        'allow_step_back': False,
    }

class HanabiEnv(Env):
    def __init__(self, config=DEFAULT_GAME_CONFIG):
        self.name = 'hanabi'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = HanabiGame(config['game_num_players'])
        super().__init__(config)
        # self.state_shape = [[4, 4, 15] for _ in range(self.num_players)]
        # self.action_shape = [None for _ in range(self.num_players)]
    
    def _extract_state(self, state):
        print("extracting state")
        print(state)
        # obs = np.zeros((4, 4, 15), dtype=int)
        # utils.encode_hand(obs[:3], state['hand'])
        # utils.encode_target(obs[3], state['target'])
        # legal_action_id = self._get_legal_actions()
        # extracted_state = {'obs': obs, 'legal_actions': legal_action_id}
        # extracted_state['raw_obs'] = state
        # extracted_state['raw_legal_actions'] = [a for a in state['legal_actions']]
        # extracted_state['action_record'] = self.action_recorder
        return state
    
    def get_payoffs(self):
        return np.array(self.game.get_payoffs())
    
    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        if action_id in legal_ids:
            return ACTION_LIST[action_id]
        # if (len(self.game.dealer.deck) + len(self.game.round.played_cards)) > 17:
        #    return ACTION_LIST[60]
        return ACTION_LIST[np.random.choice(legal_ids)]

    def _get_legal_actions(self):
        legal_actions = self.game.get_legal_actions()
        legal_ids = {ACTION_SPACE[action]: None for action in legal_actions}
        return OrderedDict(legal_ids)

    def get_perfect_information(self):
        return ""

