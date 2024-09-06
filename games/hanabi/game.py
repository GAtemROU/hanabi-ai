from games.base import Game
import numpy as np

from games.hanabi.dealer import HanabiDealer
from games.hanabi.player import HanabiPlayer
from games.hanabi.round import HanabiRound

class HanabiGame(Game):
    def __init__(self, num_players=2):
        self.np_random = np.random
        self.num_players = num_players
        self.current_payoffs = [0 for _ in range(self.num_players)]
    
    def init_game(self):
        # Initialize a dealer that can deal cards
        self.dealer = HanabiDealer(self.np_random)

        # Initialize four players to play the game
        self.players = [HanabiPlayer(i, self.np_random) for i in range(self.num_players)]

        # Deal cards to each player to prepare for the game
        player_to_num_cards = {2: 5, 3: 5, 4: 4, 5: 4}
        for player in self.players:
            self.dealer.deal_cards(player, player_to_num_cards[self.num_players])

        # Initialize a Round
        self.round = HanabiRound(self.dealer, self.num_players, self.np_random, self.players)

        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id        

    def decode_action(self, action):
        action_list = action.split('-')
        action_type = action_list[0]
        action = {'type': action_type}
        if action_type != 'hint':
            action['target_card'] = int(action_list[1])
            return action
        action['hint_type'] = action_list[1]
        action['target_player'] = int(action_list[2])
        if action['hint_type'] == 'color':
            action['hint'] = action_list[3]
        else:
            action['hint'] = int(action_list[3])
        return action 



    def step(self, action):
        '''
        Args: action (tuple): (target_player_id, action_type, action)
        '''
        # match action string as 'action_type-target_player-action'
        action_dict = self.decode_action(action)
        
        self.round.proceed_round(action_dict)
        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id
    
    def get_state(self, player_id):
        return self.round.get_state(player_id)
    
    def get_legal_actions(self):
        return self.round.get_actions()
    
    def get_num_players(self):
        return self.num_players
    
    def get_player_id(self):
        self.round.current_player
    
    def get_payoffs(self):
        return self.current_payoffs
    
    
    def get_num_actions(self):
        return 2 * 5 * self.num_players + 2 * 5 

    def is_over(self):
        ''' Check if the game is over

        Returns:
            (boolean): True if the game is over
        '''
        return self.round.is_over