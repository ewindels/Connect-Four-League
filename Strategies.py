from random import choice
from numpy import argmax
from sys import maxsize


class BasicStrategy:
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
            color = game.board.color
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
    def __init__(self, depth, show_values=False):
        self.depth = depth
        self.show_values = show_values

    def evaluate(self, game, depth):
        return 0

    def minimax(self, game_tmp, node, depth, maximizing_player=True):
        if depth == self.depth:
            value = self.evaluate(game_tmp, depth)
            node.value = value
            return value
        if maximizing_player:
            value = -maxsize
            node.children = [MinMaxNode() if game_tmp.board.heights[col] >= 0 else None for col in range(7)]
            for col, child in enumerate(node.children):
                if child:
                    game_tmp.board.update(col)
                    if game_tmp.turn >= 6 and game_tmp.board.check_victory:
                        child.value = maxsize + depth
                        value = maxsize + depth
                    elif game_tmp.board.is_full:
                        value = max(0, value)
                        child.value = 0
                    else:
                        value = max(value, self.minimax(game_tmp, child, depth + 1, False))
                    game_tmp.board.cancel()
            node.value = value
            return value
        else:
            value = maxsize
            node.children = [MinMaxNode() if game_tmp.board.heights[col] >= 0 else None for col in range(7)]
            for col, child in enumerate(node.children):
                if child:
                    game_tmp.board.update(col)
                    if game_tmp.turn >= 6 and game_tmp.board.check_victory:
                        value = -maxsize - depth
                        child.value = -maxsize - depth
                    elif game_tmp.board.is_full:
                        value = min(0, value)
                        child.value = 0
                    else:
                        value = min(value, self.minimax(game_tmp, child, depth + 1, True))
                    game_tmp.board.cancel()
            node.value = value
            return value

    def play(self, game):
        min_max_tree = MinMaxTree()
        self.minimax(game, min_max_tree.origin, 0)
        values = [node.value if node is not None else None for node in min_max_tree.origin.children]
        if self.show_values:
            print('|' + '|'.join([str(int(val)).center(3) if val else 'X'.center(3) for val in values]) + '|')
        max_val = max([node.value for node in min_max_tree.origin.children if node])
        return choice([col for col, val in enumerate(values) if val == max_val])


class MinMaxLvl0(MinMaxStrategy):
    def __init__(self, depth):
        super().__init__(depth)


class MinMaxLvl1(MinMaxStrategy):
    def __init__(self, depth):
        super().__init__(depth)
        self.column_value = {col: 2 ** (3 - abs(int(3 - col))) for col in range(7)}
        self.row_value = {row: 2 ** (2 - abs(int(2.5 - row))) for row in range(6)}

    def evaluate(self, game, depth):
        value = 0
        history = game.board.move_history[-depth::2]
        offset = [1 for _ in range(7)]
        while history:
            col = history.pop()
            value += self.column_value[col] * self.row_value[game.board.heights[col] + offset[col]]
            offset[col] += 1
        return value
