import random  

class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

class Deck:
    def __init__(self):  
        self.cards = []  
        self.suits = ["spades", "clubs", "hearts", "diamonds"]
        self.ranks = [
            {"rank": "A", "value": 11},
            {"rank": "2", "value": 2},
            {"rank": "3", "value": 3},
            {"rank": "4", "value": 4},
            {"rank": "5", "value": 5},
            {"rank": "6", "value": 6},
            {"rank": "7", "value": 7},
            {"rank": "8", "value": 8},
            {"rank": "9", "value": 9},
            {"rank": "10", "value": 10},
            {"rank": "J", "value": 10},
            {"rank": "Q", "value": 10},
            {"rank": "K", "value": 10},
        ]
        for suit in self.suits:
            for r in self.ranks:
                self.cards.append(Card(suit, r["rank"], r["value"]))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, number):
        cards_dealt = []
        for i in range(number):
            cards_dealt.append(self.cards.pop())
        return cards_dealt


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []  

    def add_card(self, card):
        if isinstance(card, list):
            self.hand.extend(card)
        else:
            self.hand.append(card)

    def calculate_score(self):
        total = 0
        aces = 0 
        for card in self.hand:
            total += card.value
            if card.rank == "A":
                aces += 1
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player("Player")
        self.dealer = Player("Dealer")
        self.player.add_card(self.deck.deal(2))
        self.dealer.add_card(self.deck.deal(2))
