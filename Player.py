class Player:
    def __init__(self, strategy):
        self.strategy = strategy

    def play(self, game):
        return self.strategy.play(game)
