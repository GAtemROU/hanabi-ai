from games.hanabi.card import HanabiCard as Card
import os 
import json 
import games
from collections import OrderedDict
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
