from random import choice
from numpy import argmax


class Strategy:
    def __init__(self, strategy):
        self.strategy = strategy

    def play(self, game):
        if self.strategy == 'random':
            available = [col for col in range(7) if game.board.heights[col] >= 0]
            return choice(available)

        elif self.strategy == 'least_full':
            least_full = max(game.board.heights)
            available = [col for col in range(7) if game.board.heights[col] == least_full]
            return choice(available)

        elif self.strategy == 'fullest':
            fullest = min([height for height in  game.board.heights if height >= 0])
            available = [col for col in range(7) if game.board.heights[col] == fullest]
            return choice(available)

        elif self.strategy == 'groups_same':
            color = game.players[game.player_turn_n].color
            scores = [0 for _ in range(7)]
            for col in range(7):
                score = 0
                row = game.board.heights[col]
                if row < 0:
                    continue
                for dist in range(1, 4):
                    weight = 1/(2**(dist-1))
                    # up
                    if row - dist >= 0:
                        for c in range(max(0, col - dist), min(7, col + dist + 1)):
                            if game.board.grid[row - dist][c] == color:
                                score += weight
                    # down
                    if row + dist <= 6:
                        for c in range(max(0, col - dist), min(7, col + dist + 1)):
                            if game.board.grid[row + dist][c] == color:
                                score += weight
                    # left
                    if col - dist >= 0:
                        for r in range(max(1, row - dist + 1), min(6, row + dist)):
                            if game.board.grid[r][col - dist] == color:
                                score += weight
                    # right
                    if col + dist < 7:
                        for r in range(max(1, row - dist + 1), min(6, row + dist)):
                            if game.board.grid[r][col + dist] == color:
                                score += weight
                scores[col] = score
            return argmax(scores)

        elif self.strategy == 'groups_oppo':
            color = game.players[(game.player_turn_n + 1)%2].color
            scores = [0 for _ in range(7)]
            for col in range(7):
                score = 0
                row = game.board.heights[col]
                if row < 0:
                    continue
                for dist in range(1, 4):
                    weight = 1/(2**(dist-1))
                    # up
                    if row - dist >= 0:
                        for c in range(max(0, col - dist), min(7, col + dist + 1)):
                            if game.board.grid[row - dist][c] == color:
                                score += weight
                    # down
                    if row + dist <= 6:
                        for c in range(max(0, col - dist), min(7, col + dist + 1)):
                            if game.board.grid[row + dist][c] == color:
                                score += weight
                    # left
                    if col - dist >= 0:
                        for r in range(max(1, row - dist + 1), min(6, row + dist)):
                            if game.board.grid[r][col - dist] == color:
                                score += weight
                    # right
                    if col + dist < 7:
                        for r in range(max(1, row - dist + 1), min(6, row + dist)):
                            if game.board.grid[r][col + dist] == color:
                                score += weight
                scores[col] = score
            max_score = max(scores)
            return choice([col for col in range(7) if scores[col] == max_score])
        else:
            print("Strategy doesn't exist !")
