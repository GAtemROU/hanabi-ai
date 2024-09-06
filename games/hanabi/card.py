import numpy as np
from games.base import Card
class HanabiCard(Card):
    info = {'num': [1, 2, 3, 4, 5],
            'color': ['red', 'green', 'blue', 'yellow', 'white'],
            'hinted': np.zeros(10)}
    
    def __init__(self, num, color):
        self.num = num
        self.color = color
        self.hinted = np.zeros(10)

    def get_str(self):
        return f'{self.color}-{self.num}'        
    
    def encode(self):
        value = [0] * 25
        value[self.color * 5 + self.num - 1] = 1
        value.append(self.hinted)
        return value
    

    