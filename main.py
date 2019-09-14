from Game import Game
from Player import Player
from Strategies import *

player1 = Player(MinMaxLvl1(2))
player2 = Player(MinMaxLvl0(2))
game = Game(player1, player2)


victory_dict = {0: 0, 1: 0, None: 0}

games = 1
for _ in range(games):
    winner = game.full_game(log=True)
    game.reset()
    game.switch_players()
    victory_dict[winner] += 1

print(victory_dict)
