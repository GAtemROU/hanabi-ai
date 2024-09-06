from games.base import Card
class HanabiCard(Card):
    info = {'num': [1, 2, 3, 4, 5],
            'color': ['red', 'green', 'blue', 'yellow', 'white'],}
    
    def __init__(self, num, color):
        self.num = num
        self.color = color

    def get_str(self):
        return f'{self.color}-{self.num}'
    