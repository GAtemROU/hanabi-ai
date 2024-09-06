from games.hanabi.card import HanabiCard as Card
import os 
import json 
import games
from collections import OrderedDict

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