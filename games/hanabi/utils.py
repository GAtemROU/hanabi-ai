from card import Card

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