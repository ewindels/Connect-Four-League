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
            fullest = min([height for height in game.board.heights if height >= 0])
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
                    weight = 1 / (2 ** (dist - 1))
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
            color = game.players[(game.player_turn_n + 1) % 2].color
            scores = [0 for _ in range(7)]
            for col in range(7):
                score = 0
                row = game.board.heights[col]
                if row < 0:
                    continue
                for dist in range(1, 4):
                    weight = 1 / (2 ** (dist - 1))
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


class MinMaxNode:
    def __init__(self):
        self.value = None
        self.children = None


class MinMaxTree:
    def __init__(self):
        self.origin = MinMaxNode()


class MinMaxStrategy:
    def __init__(self, depth):
        self.depth = depth

    def play(self, game):

        def minimax(game_tmp, node, depth, maximizing_player=True):
            color = game_tmp.players[(game_tmp.player_turn_n + maximizing_player + 1) % 2].color
            if depth == 0:
                node.value = 0
                return 0
            if maximizing_player:
                value = -1e9
                node.children = [MinMaxNode() if game_tmp.board.heights[col] >= 0 else None for col in range(7)]
                for col, child in enumerate(node.children):
                    if child:
                        game_tmp.board.update(col, color)
                        if game_tmp.board.check_victory:
                            child.value = 1e9
                            value = 1e9
                        elif game_tmp.board.is_full:
                            value = max(0, value)
                            child.value = 0
                        else:
                            value = max(value, minimax(game_tmp, child, depth - 1, False))
                        game_tmp.board.cancel()
                node.value = value
                return value
            else:
                value = 1e9
                node.children = [MinMaxNode() if game_tmp.board.heights[col] >= 0 else None for col in range(7)]
                for col, child in enumerate(node.children):
                    if child:
                        game_tmp.board.update(col, color)
                        if game_tmp.board.check_victory:
                            value = -1e9
                            child.value = -1e9
                        elif game_tmp.board.is_full:
                            value = min(0, value)
                            child.value = 0
                        else:
                            value = min(value, minimax(game_tmp, child, depth - 1, True))
                        game_tmp.board.cancel()
                node.value = value
                return value

        min_max_tree = MinMaxTree()
        minimax(game, min_max_tree.origin, self.depth)
        values = [node.value if node is not None else -1e9 for node in min_max_tree.origin.children]
        max_val = max(values)
        return choice([col for col, val in enumerate(values) if val == max_val])

