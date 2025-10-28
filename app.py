from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# --------------------------
# CARD CLASS
# --------------------------
class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return f"{self.rank} of {self.suit} (Value: {self.value})"


# --------------------------
# DECK CLASS
# --------------------------
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
                card = Card(suit, r["rank"], r["value"])
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, number):
        cards_dealt = []
        for i in range(number):
            cards_dealt.append(self.cards.pop())
        return cards_dealt


# --------------------------
# PLAYER CLASS
# --------------------------
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

    def show_hand(self):
        return [f"{card.rank} of {card.suit}" for card in self.hand]


# --------------------------
# GAME LOGIC
# --------------------------
deck = Deck()
deck.shuffle()
player = Player("Player")
dealer = Player("Dealer")

player.add_card(deck.deal(2))
dealer.add_card(deck.deal(2))


@app.route('/')
def index():
    return render_template('index.html',
                           player_hand=player.show_hand(),
                           dealer_hand=[str(dealer.hand[0]), "Hidden Card"],
                           player_score=player.calculate_score())


@app.route('/hit')
def hit():
    player.add_card(deck.deal(1))
    score = player.calculate_score()

    if score > 21:
        return jsonify({
            "player_hand": player.show_hand(),
            "player_score": score,
            "message": "💥 You busted! Dealer wins.",
            "game_over": True
        })

    return jsonify({
        "player_hand": player.show_hand(),
        "player_score": score,
        "message": "You drew a new card.",
        "game_over": False
    })


@app.route('/stand')
def stand():
    while dealer.calculate_score() < 17:
        dealer.add_card(deck.deal(1))

    dealer_score = dealer.calculate_score()
    player_score = player.calculate_score()

    if dealer_score > 21:
        message = "🎉 Dealer busted! You win."
    elif player_score > dealer_score:
        message = "🏆 You win!"
    elif player_score < dealer_score:
        message = "😢 Dealer wins!"
    else:
        message = "🤝 It's a tie!"

    return jsonify({
        "dealer_hand": dealer.show_hand(),
        "dealer_score": dealer_score,
        "player_score": player_score,
        "message": message,
        "game_over": True
    })


if __name__ == "__main__":
    app.run(debug=True)
