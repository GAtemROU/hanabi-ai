from games.hanabi.card import HanabiCard as Card
import os 
import json 
import games
from collections import OrderedDict
import numpy as np

ACTION_TYPE = ['play', 'discard', 'hint']
CARD_ID = [0, 1, 2, 3, 4]
HINT_TYPE = ['color', 'num']
COLORS = ['red', 'green', 'blue', 'yellow', 'white']
NUMS = [1, 2, 3, 4, 5]
CARDS_PER_PLAYER = {2: 5, 3: 5, 4: 4, 5: 4}

card_info = Card.info
def init_deck():
    deck = []
    for color in card_info['color']:
        for num in card_info['num']:
            if num == 1:
                deck.append(Card(num, color))
            deck.append(Card(num, color))
            if num != 5:
                deck.append(Card(num, color))
    return deck

ROOT_PATH = games.__path__[0]
# a map of abstract action to its index and a list of abstract action
with open(os.path.join(ROOT_PATH, 'hanabi/jsondata/action_space.json'), 'r') as file:
    ACTION_SPACE = json.load(file, object_pairs_hook=OrderedDict)
    ACTION_LIST = list(ACTION_SPACE.keys())

def generate_action_space(num_players):
    # string to index
    action_space = {}
    for action_type in ACTION_TYPE:
        if action_type == 'hint':
            continue
        for card_id in CARD_ID[0:CARDS_PER_PLAYER[num_players]]:
            for target_player in range(num_players):
                action = f'{action_type}-{card_id}'
                action_space[action] = len(action_space)
    for hint_type in HINT_TYPE:
        for target_player in range(num_players):
            for hint in range(5):
                if hint_type == 'color':
                    hint = COLORS[hint]
                else:
                    hint = NUMS[hint]
                action = f'hint-{hint_type}-{target_player}-{hint}'
                action_space[action] = len(action_space)
    with open(os.path.join(ROOT_PATH, 'hanabi/jsondata/action_space.json'), 'w') as file:
        json.dump(action_space, file)


def get_action_list():
    return ACTION_LIST


        # utils.encode_hands(obs[:2, :, :], state)
        # utils.encode_card_colors(obs[2, :, :], state)
        # utils.encode_state_info(obs[3, :, :], state)
        # utils.encode_hinted(obs[4:8, :, :], state)

#     def get_state(self, player_id):
        # state = {}
        # # state.append(self.field)
        # # state.append(self.hints)
        # # state.append(self.lives)
        # # state.append(self.cards_left)
        # # state.append(self.discard)
        # # for player in self.players:
        # #     for (i, card) in enumerate(player.hand):
        # #         state.append(card.encode())
        # state['field'] = self.field
        # state['hints'] = self.hints
        # state['lives'] = self.lives
        # state['cards_left'] = self.cards_left
        # state['discard'] = self.discard
        # state['current_player'] = self.current_player
        # state['legal_actions'] = self.get_actions()
        # hand_dict = {}
        # for player in self.players:
        #     hand_dict[player.id] = player.hand
        # state['hands'] = hand_dict
        # return state
    
def encode_hands(obs, state):
    # print("encoded hands")
    for player_id in state['hands']:

        if player_id == state['current_player']: continue 
        # print(f"player_id: {player_id}")
        hand = state['hands'][player_id]
        for i, card in enumerate(hand):
            # print(f"card: {card}")
            obs[player_id, i, :] = card.encode()
    
    # print(obs)
    # print("----- ")

def encode_card_colors(obs, state):
    values = np.zeros(50)
    for item in state['field']:
        for i in range (item):
            values[(i) + item * 5] = 1

    values[25:] = state['discard']
    
    #reshape 
    obs[:, :] = values.reshape(5, 10)
    # print('encoded card colors')


def encode_state_info(obs, state):
    values = np.zeros(50)
    values[0] = state['hints']
    values[1] = state['lives']
    values[2] = state['cards_left']
    values[2 + state['current_player']] = 1
    #reshape
    obs[:, :] = values.reshape(5, 10)


def encode_hinted(obs, state):
    for player_id in state['hands']:
        hand = state['hands'][player_id]
        for i, card in enumerate(hand):
            obs[2 * player_id : 2 * player_id + 2, i, : ] = card.get_hinted().reshape(2, 10)
    # print('encoded hinted')
    # print(obs)

    return obs
