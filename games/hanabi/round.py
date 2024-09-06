import numpy as np
from games.base import Round

COLOR_TO_INDEX = {'red': 0, 'green': 1, 'blue': 2, 'yellow': 3, 'white': 4}
NUM_TO_INDEX = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
INDEX_TO_COLOR = {0: 'red', 1: 'green', 2: 'blue', 3: 'yellow', 4: 'white'}
INDEX_TO_NUM = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}
COLORS = ['red', 'green', 'blue', 'yellow', 'white']
NUMS = [1, 2, 3, 4, 5]
class HanabiRound(Round):
    def __init__(self, dealer, num_players, np_random, players):
        self.np_random = np_random
        self.dealer = dealer
        self.current_player = 0
        self.num_players = num_players
        self.played_cards = []
        self.is_over = False
        self.hints = 8
        self.lives = 3
        self.actions_history = []
        self.field = [0, 0, 0, 0, 0]
        self.cards_left = dealer.cards_left()
        self.turns_left = num_players
        self.discard = np.zeros(25)
        self.players = players
        


    def proceed_round(self, player, target_player, action_type, action):
        if self.deck_finished:
            self.turns_left -= 1
        if self.turns_left == 0:
            self.is_over = True
        match action_type:
            case 'play':
                self._play_card(player, action)
            case 'discard':
                self._discard_card(player, action)
            case 'hint':
                self._hint(player, target_player, action)
    
    def _play_card(self, player, action):
        played = player.hand[action]
        if played.num == self.field[COLOR_TO_INDEX[played.color]] + 1:
            self.field[COLOR_TO_INDEX[played.color]] += 1
            self.played_cards.append(played)
            player.hand.remove(played)
            self.actions_history.append((player, 'play', played))
        else:
            self.lives -= 1
            self.actions_history.append((player, 'play', played, 'fail'))
            if self.lives == 0:
                self.is_over = True
        if played.num == 5:
            self.hints += 1
        self.cards_left = self.dealer.draw_card(player)
        if self.cards_left == 0:
            self.deck_finished = True
        
    def _discard_card(self, player, action):
        discarded = player.hand[action]
        self.discard[COLOR_TO_INDEX[discarded.color] * 5 + NUM_TO_INDEX[discarded.num] - 1] += 1
        player.hand.remove(discarded)
        self.hints += 1
        self.actions_history.append((player, 'discard', discarded))
        self.cards_left = self.dealer.draw_card(player)
        if self.cards_left == 0:
            self.deck_finished = True
    
    def _hint(self, player, target_player, action):
        self.hints -= 1
        if (INDEX_TO_COLOR.get(action) is not None):
            self._hint_color(player, target_player, action)
        else:
            self._hint_num(player, target_player, action)

        
    def _hint_color(self, player, target_player, action):
        hinted = np.zeros(len(target_player.hand))
        for i in range(len(target_player.hand)):
            if COLOR_TO_INDEX[target_player.hand[i].color] == action:
                hinted[i] = 1
                player.hand[i].hinted[action] = 1
            else :
                hinted[i] = 0
        self.actions_history.append((player, 'hint', hinted))

    def _hint_num(self, player, target_player, action):
        hinted = np.zeros(len(target_player.hand))
        for i in range(len(target_player.hand)):
            if NUM_TO_INDEX[target_player.hand[i].num] == action:
                hinted[i] = 1
                player.hand[i].hinted[action] = 1
            else :
                hinted[i] = 0
        self.actions_history.append((player, 'hint', hinted))   

    def get_legal_actions(self):
        actions = []
        for (i, card) in enumerate(self.players[self.current_player].hand):
            actions.append(f'play-{i}')
            actions.append(f'discard-{i}')
        if self.hints > 0:
            for player in self.players:
                if player.id != self.current_player:
                    for color in COLORS:
                        actions.append(f'hint-color-{player.id}-{color}')
                    for num in NUMS:
                        actions.append(f'hint-num-{player.id}-{num}')
        return actions
    
    def get_state(self, player_id):
        state = {}
        # state.append(self.field)
        # state.append(self.hints)
        # state.append(self.lives)
        # state.append(self.cards_left)
        # state.append(self.discard)
        # for player in self.players:
        #     for (i, card) in enumerate(player.hand):
        #         state.append(card.encode())
        state['field'] = self.field
        state['hints'] = self.hints
        state['lives'] = self.lives
        state['cards_left'] = self.cards_left
        state['discard'] = self.discard
        state['current_player'] = self.current_player
        state['legal_actions'] = self.get_legal_actions()
        hand_dict = {}
        for player in self.players:
            hand_dict[player.id] = player.hand
        state['hands'] = hand_dict
        return state
    
