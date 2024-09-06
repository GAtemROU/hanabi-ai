import numpy as np
from games.base import Card

COLOR_TO_INDEX = {'red': 0, 'green': 1, 'blue': 2, 'yellow': 3, 'white': 4}

class HanabiCard(Card):
    info = {'num': [1, 2, 3, 4, 5],
            'color': ['red', 'green', 'blue', 'yellow', 'white']}
    
    def __init__(self, num, color):
        self.num = num
        self.color = color
        # first 5 positive hints for colors, next 5 for numbers
        # 10-15 negative hints for colors, 15-20 for numbers
        self.hinted = np.zeros(20)

    def get_str(self):
        return f'{self.color}-{self.num}'        
    
    def get_id(self):
        return COLOR_TO_INDEX[self.color] * 5 + self.num - 1
    
    def get_hinted(self):
        return self.hinted

    # to_string
    def __str__(self):
        return f'{self.color}-{self.num}'
    
    def encode(self):
        feature_vector = np.zeros(10)
        feature_vector[5 + COLOR_TO_INDEX[self.color]] = 1
        feature_vector[self.num - 1] = 1
        return feature_vector
        
    

    