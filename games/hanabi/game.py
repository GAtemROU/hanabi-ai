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
    
    
    def step(self, action):
        '''
        Args: action (tuple): (target_player_id, action_type, action)
        '''
        player = self.round.current_player
        target_player = self.players[action[0]]
        match action[1]:
            case 0:
                action_type = 'play'
            case 1:
                action_type = 'discard'
            case 2:
                action_type = 'hint'
        action = action[2]
        self.round.proceed_round(player, target_player, action_type, action)
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
        self.round.current_player_id
    
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