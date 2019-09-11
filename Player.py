class Player:
    def __init__(self, color, strategy):
        self.color = color
        self.strategy = strategy

    def play(self, game):
        return self.strategy.play(game, self.color)
