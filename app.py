from flask import Flask, render_template, jsonify
from blackjack_logic import BlackjackGame

app = Flask(__name__)
game = BlackjackGame()  # Single game instance


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/state')
def state():
    return jsonify({
        "player_hand": [str(c) for c in game.player.hand],
        "dealer_hand": [str(c) for c in game.dealer.hand],
        "message": "🎮 Game started! Your move.",
        "game_over": False
    })


@app.route('/hit')
def hit():
    game.player.add_card(game.deck.deal(1))
    score = game.player.calculate_score()
    if score > 21:
        return jsonify({
            "player_hand": [str(c) for c in game.player.hand],
            "dealer_hand": [str(c) for c in game.dealer.hand],
            "message": "💥 You busted! Dealer wins.",
            "game_over": True
        })
    return jsonify({
        "player_hand": [str(c) for c in game.player.hand],
        "dealer_hand": [str(c) for c in game.dealer.hand],
        "message": "You drew a card!",
        "game_over": False
    })


@app.route('/stand')
def stand():
    while game.dealer.calculate_score() < 17:
        game.dealer.add_card(game.deck.deal(1))
    player_score = game.player.calculate_score()
    dealer_score = game.dealer.calculate_score()

    if dealer_score > 21 or player_score > dealer_score:
        message = "🎉 You win!"
    elif dealer_score < player_score:
        message = "🎉 You win!"
    elif dealer_score > player_score:
        message = "💀 Dealer wins!"
    else:
        message = "🤝 It's a tie!"

    return jsonify({
        "player_hand": [str(c) for c in game.player.hand],
        "dealer_hand": [str(c) for c in game.dealer.hand],
        "message": message,
        "game_over": True
    })


@app.route('/restart')
def restart():
    global game
    game = BlackjackGame()
    return jsonify({
        "player_hand": [str(c) for c in game.player.hand],
        "dealer_hand": [str(c) for c in game.dealer.hand],
        "message": "🔄 New game started!",
        "game_over": False
    })


if __name__ == "__main__":
    app.run(debug=True)
