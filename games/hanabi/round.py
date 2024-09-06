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
        self.is_over = False
        self.hints = 8
        self.lives = 3
        self.actions_history = []
        self.field = [0, 0, 0, 0, 0]
        self.cards_left = dealer.cards_left()
        self.turns_left = num_players
        self.discard = np.zeros(25)
        self.players = players
        self.max_hints = 8
        self.payoffs = np.zeros(num_players)
        
    def get_payoffs(self):
        return self.payoffs

    def proceed_round(self, action):
        player = self.players[self.current_player]
        if self.cards_left == 0:
            self.turns_left -= 1
        if self.turns_left == 0:
            self.is_over = True
        match action['type']:
            case 'play':
                self._play(player, action['target_card'])
            case 'discard':
                self._discard(player, action['target_card'])
            case 'hint':
                self._hint(player, action['hint_type'], action['target_player'], action['hint'])
        self.current_player = (self.current_player + 1) % self.num_players
    
    def _play(self, player, target_card):
        card = player.hand[target_card]
        if card.num == self.field[COLOR_TO_INDEX[card.color]]+1:
            self.field[COLOR_TO_INDEX[card.color]] += 1
            if card.num == 5:
                self.hints += 1
            self.actions_history.append((player.get_player_id(), 'play', card.__str__(), "success"))
            self.payoffs[player.get_player_id()] += 1
        else:
            self.lives -= 1
            self.discard[card.get_id()] += 1
            self.actions_history.append((player.get_player_id(), 'play', card.__str__(), "fail"))
            self.payoffs[player.get_player_id()] -= (card.num == 5) if 5 else 1*(5-card.num)
            if self.lives == 0:
                self.is_over = True
                # self.print_history()

                # print("Game Over. Final Score: ", sum(self.field))

        player.hand.pop(target_card)
        self.cards_left = self.dealer.draw_card(player)
        if self.cards_left == 0:
            self.deck_finished = True

    def print_history(self):
        for action in self.actions_history:
            print(action)

    def _discard(self, player, target_card):
        self.hints += 1
        card = player.hand[target_card]
        self.discard[card.get_id()] += 1
        player.hand.pop(target_card)
        self.cards_left = self.dealer.draw_card(player)
        if self.cards_left == 0:
            self.deck_finished = True
        self.actions_history.append((player.get_player_id(), 'discard', card.__str__()))
        if (self.field[COLOR_TO_INDEX[card.color]] < card.num):
            self.payoffs[player.get_player_id()] -= (card.num == 5) if 5 else 1*(5-card.num)
        else:
            self.payoffs[player.get_player_id()] += 1


    def _hint(self, player, action_type, target_player, hint):
        self.hints -= 1
        if (action_type == 'color'):
            self._hint_color(player, target_player, hint)
        else:
            self._hint_num(player, target_player, hint)
        self.payoffs[player.get_player_id()] += 0.1  
    
    def _hint_color(self, player, target_player, color):
        for (i, card) in enumerate(self.players[target_player].hand):
            if card.color == color:
                card.hinted[COLOR_TO_INDEX[color]] = 1
            else:
                card.hinted[10 + COLOR_TO_INDEX[color]] = 1
        self.actions_history.append((player.get_player_id(), 'hint-color', target_player, color))
    
    def _hint_num(self, player, target_player, num):
        for (i, card) in enumerate(self.players[target_player].hand):
            if card.num == num:
                card.hinted[5 + NUM_TO_INDEX[num]] = 1
            else:
                card.hinted[15 + NUM_TO_INDEX[num]] = 1
        self.actions_history.append((player.get_player_id(), 'hint-num', target_player, num))

    def get_actions(self):
        actions = []
        for (i, card) in enumerate(self.players[self.current_player].hand):
            actions.append(f'play-{i}')
            if self.hints < self.max_hints:
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
        state['legal_actions'] = self.get_actions()
        hand_dict = {}
        for player in self.players:
            hand_dict[player.id] = player.hand
        state['hands'] = hand_dict
        return state
    
