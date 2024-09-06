import numpy as np
from games.base import Card

COLOR_TO_INDEX = {'red': 0, 'green': 1, 'blue': 2, 'yellow': 3, 'white': 4}

class HanabiCard(Card):
    info = {'num': [1, 2, 3, 4, 5],
            'color': ['red', 'green', 'blue', 'yellow', 'white']}
    
    def __init__(self, num, color):
        self.num = num
        self.color = color
        self.hinted = [0] * 10

    def get_str(self):
        return f'{self.color}-{self.num}'        
    
    def get_id(self):
        return COLOR_TO_INDEX[self.color] * 5 + self.num - 1

    # to_string
    def __str__(self):
        return self.num + ' ' + self.color
    

    