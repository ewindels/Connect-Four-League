from Strategies import MinMaxStrategy
from Player import Player
from Game import Game
import numpy as np
from random import choice, choices
from copy import deepcopy


class GeneticMinMax(MinMaxStrategy):
    def __init__(self, depth):
        super().__init__(depth)
        self.values = np.random.randint(10, size=(6, 7))
        self.mutation_rate = 2.5

    def neutral(self):
        self.values = np.zeros((6, 7))

    def crossover(self, genetic_min_max):
        self.values = np.mean([self.values, genetic_min_max.values], axis=0).round()

    def mutate(self):
        self.values += ((np.random.random(size=(6, 7)) - 0.5) * self.mutation_rate).astype(int)

    def evaluate(self, game, depth):
        value = 0
        history = game.board.move_history[-depth::2]
        offset = [1 for _ in range(7)]

        while history:
            col = history.pop()
            row = game.board.heights[col] + offset[col]
            value += self.values[row, col]
            offset[col] += 1
        return value


class Population:
    def __init__(self, pop_size=20, depth=4):
        self.population = [Player(strategy=GeneticMinMax(depth)) for _ in range(pop_size)]
        neutral_player = Player(GeneticMinMax(depth))
        neutral_player.strategy.neutral()
        self.best_players = [neutral_player]
        self.depth = depth

    def match(self):
        for player1 in self.population:
            for player2 in self.population:
                game = Game(player1, player2)
                game.full_game()

        self.best_players.append(deepcopy(max(self.population, key=lambda p: p.score)))
        self.best_players[-1].reset_score()
        print('\n\nMean :')
        self.print_mean()
        print('\n\nStd :')
        self.print_std()
        print('Best :')
        self.print_best()

    def print_mean(self):
        print(np.mean([player.strategy.values for player in self.population], axis=0).round(1))

    def print_std(self):
        print(np.std([player.strategy.values for player in self.population], axis=0).round(1))

    def print_best(self):
        print(self.best_players[-1].strategy.values)

    def evolve(self):
        new_population = [deepcopy(pl) for pl in choices(self.population,
                                                         weights=[player.score ** 2 for player in self.population],
                                                         k=len(self.population))]
        new_population_cross = [deepcopy(pl) for pl in new_population]
        for player in new_population:
            player.strategy.crossover(choice(new_population_cross).strategy)
            player.reset_score()
            player.strategy.mutate()
        del new_population_cross
        self.population = new_population[:-1] + [self.best_players[-1]]

    def best_vs_previous(self):
        game = Game(self.best_players[-2], self.best_players[-1])
        for _ in range(50):
            game.full_game()
            game.reset()
            game.switch_players()
        print('\nBest player vs Previous best :')
        self.best_players[-1].print_score()
        self.best_players[-1].reset_score()
        self.best_players[-2].reset_score()

'''
pop = Population()
for i in range(5):
    print('\nGeneration', i)
    pop.match()
    pop.evolve()
    pop.best_vs_previous()

pop.best_players[-2].strategy.show_values = True
pop.best_players[-1].strategy.show_values = True
game = Game(pop.best_players[-2], pop.best_players[-1])
for _ in range(2):
    game.full_game(log=True)
    game.reset()
    game.switch_players()
'''



