from Game import Game
from Player import Player
from Strategies import *
from GeneticMinMax import *


player1 = Player(MinMaxLvl1(depth=7, show_values=True))
player2 = Player(MinMaxLvl0(depth=7, show_values=True))
game = Game(player1, player2)

games = 1
for _ in range(games):
    winner = game.full_game(log=True)
    game.reset()
    game.switch_players()

player1.print_score()
player2.print_score()

print('Player 1:', player1.score, '/ Player 2:', player2.score)
