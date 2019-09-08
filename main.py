from Game import Game
from Player import Player
from Strategies import Strategy

player1 = Player('X', Strategy('groups_same'))
player2 = Player('O', Strategy('groups_oppo'))
game = Game(player1, player2)


victory_dict = {0: 0, 1: 0, None: 0}
for _ in range(1000):
    winner = game.full_game(log=False)
    game.reset()
    victory_dict[winner] += 1

print(victory_dict)

