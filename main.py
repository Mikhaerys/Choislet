import random


def roulette_winner(text):
    options = text.splitlines()
    scores = {key: 0 for key in options}

    while True:
        winner = random.choice(options)
        scores[winner] += 1
        if scores[winner] == 3:
            return winner


def flip_coin(head, tail):
    return random.choice([head, tail])


def dice_game(text):
    options = text.splitlines()
    scores = {key: 0 for key in options}

    while True:
        for option in options:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            scores[option] = dice1 + dice2

        max_value = max(scores.values())
        winners = [jugador for jugador,
                   value in scores.items() if value == max_value]

        if len(winners) == 1:
            return winners, max_value

        options = winners
