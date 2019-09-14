class Player:
    def __init__(self, strategy):
        self.strategy = strategy
        self.victories = 0
        self.defeats = 0
        self.draws = 0

    @property
    def score(self):
        return self.victories + self.draws / 2

    def reset_score(self):
        self.victories = self.draws = self.defeats = 0

    def print_score(self):
        print('Victories : {}, Draws : {}, Defeats : {}'.format(self.victories, self.draws, self.defeats))

    def play(self, game):
        return self.strategy.play(game)
