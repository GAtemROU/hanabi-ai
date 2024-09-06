from games.base import Round

COLOR_TO_INDEX = {'red': 0, 'green': 1, 'blue': 2, 'yellow': 3, 'white': 4}
NUM_TO_INDEX = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
INDEX_TO_COLOR = {0: 'red', 1: 'green', 2: 'blue', 3: 'yellow', 4: 'white'}
INDEX_TO_NUM = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}

class HanabiRound(Round):
    def __init__(self, dealer, num_players, np_random):
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
        self.deck_finished = False
        self.turns_left = num_players
        


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
        self.deck_finished = self.dealer.draw_card(player)
        
    def _discard_card(self, player, action):
        discarded = player.hand[action]
        player.hand.remove(discarded)
        self.hints += 1
        self.actions_history.append((player, 'discard', discarded))
        self.deck_finised = self.dealer.draw_card(player)
    
    def _hint(self, player, target_player, action):
        if (INDEX_TO_COLOR.get(action) is not None):
            self._hint_color(player, target_player, action)
        else:
           self. _hint_num(player, target_player, action)
        
    def _hint_color(self, player, target_player, action):
        for i in range(len(target_player.hand)):
            if target_player.hand[i].color == action:
                target_player.hand[i].hinted = True
        self.hints -= 1
        self.actions_history.append((player, 'hint', action))

    def _hint_num(self, player, target_player, action):
        for i in range(len(target_player.hand)):
            if target_player.hand[i].num == action:
                target_player.hand[i].hinted = True
        self.hints -= 1
        self.actions_history.append((player, 'hint', action))

    def get_actions(self):
        return self.actions
    
    def get_state(self):
        pass
    