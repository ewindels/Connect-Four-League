from Game import Game
from Player import Player
from Strategies import *

player1 = Player(MinMaxLvl1(3))
player2 = Player(MinMaxLvl0(3))
game = Game(player1, player2)


victory_dict = {0: 0, 1: 0, None: 0}

games = 200
for _ in range(games):
    winner = game.full_game(log=False)
    game.reset()
    game.switch_players()
    victory_dict[winner] += 1

print(victory_dict)
