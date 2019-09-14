from Strategies import MinMaxStrategy
from Player import Player
from Game import Game
import numpy as np
from random import choice, choices
from tqdm import tqdm
from copy import deepcopy


class GeneticMinMax(MinMaxStrategy):
    def __init__(self, depth):
        super().__init__(depth)
        self.values = np.random.randint(10, size=(6, 7))
        self.mutation_rate = 0.1

    def neutral(self):
        self.values = np.zeros((6, 7))

    def crossover(self, genetic_min_max):
        self.values = np.mean([self.values, genetic_min_max.values], axis=0)

    def mutate(self):
        for row in range(6):
            for col in range(7):
                self.values[row][col] += 2 * (np.random.random() - 0.5) * self.mutation_rate

    def evaluate(self, game, depth):
        value = 0
        history = game.board.move_history[-depth:2]
        offset = [1 for _ in range(7)]

        while history:
            col = history.pop()
            row = game.board.heights[col] + offset[col]
            if depth % 2 == 1:
                value += self.values[row, col]
            offset[col] += 1
        return value


class Population:
    def __init__(self, pop_size=30):
        self.population = [Player(strategy=GeneticMinMax(2)) for _ in range(pop_size)]
        self.best_player = None

    def match(self, n=30):
        with tqdm(total=len(self.population)) as pbar:
            for player1 in self.population:
                for i in range(n):
                    player2 = choice(self.population)
                    game = Game(player1, player2)
                    if i % 2 == 0:
                        game.switch_players()
                    game.full_game()
                pbar.update(1)

        self.best_player = deepcopy(max(self.population, key=lambda p: p.score))
        self.best_player.reset_score()
        print('\n\nMean :')
        self.print_mean()
        print('Best :')
        self.print_best()

    def print_mean(self):
        print(np.mean([player.strategy.values for player in self.population], axis=0).round(2))

    def print_best(self):
        print(self.best_player.strategy.values.round(2))

    def evolve(self):
        new_population = choices(self.population,
                                 weights=[player.score for player in self.population],
                                 k=len(self.population))
        for player in new_population:
            player.strategy.crossover(choice(new_population).strategy)
            player.strategy.mutate()
            player.reset_score()
        self.population = new_population

    def best_vs_neutral(self):
        neutral_strategy = GeneticMinMax(2)
        neutral_strategy.neutral()
        neutral_player = Player(neutral_strategy)

        game = Game(neutral_player, self.best_player)
        for _ in range(100):
            game.full_game()
            game.reset()
            game.switch_players()
        print('Best player vs Neutral :')
        self.best_player.print_score()


pop = Population()
for i in range(10):
    print('\nGeneration', i)
    pop.match()
    pop.evolve()
    pop.best_vs_neutral()
