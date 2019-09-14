from Game import Game
from Player import Player
from Strategies import Strategy, MinMaxStrategy

player1 = Player('X', MinMaxStrategy(1))
player2 = Player('O', MinMaxStrategy(1))
game = Game(player1, player2)


victory_dict = {0: 0, 1: 0, None: 0}
for _ in range(200):
    winner = game.full_game(log=False)
    game.reset()
    victory_dict[winner] += 1

print(victory_dict)

