class Board:
    def __init__(self):
        self.grid = [[None for _ in range(7)] for _ in range(7)]
        self.heights = [6 for _ in range(7)]
        self.move_history = list()
        self.colors = ['X', 'O']

    def update(self, column):
        assert(self.heights[column] >= 0)
        self.grid[self.heights[column]][column] = self.color
        self.heights[column] -= 1
        self.move_history.append(column)

    def cancel(self):
        last_move = self.move_history.pop()
        self.grid[self.heights[last_move] + 1][last_move] = None
        self.heights[last_move] += 1

    @property
    def color(self):
        return self.colors[len(self.move_history) % 2]

    @property
    def is_full(self):
        return all([height == -1 for height in self.heights])

    @property
    def check_victory(self):
        last_row, last_col = self.heights[self.last_move] + 1, self.last_move
        color = self.grid[last_row][last_col]
        # horizontal
        total = 1
        i = 1
        while last_col - i >= 0 and self.grid[last_row][last_col - i] == color:
            total += 1
            i += 1
        i = 1
        while last_col + i < 7 and self.grid[last_row][last_col + i] == color:
            total += 1
            i += 1
        if total == 4:
            return True
        # vertical
        total = 1
        i = 1
        while last_row - i >= 0 and self.grid[last_row - i][last_col] == color:
            total += 1
            i += 1
        i = 1
        while last_row + i < 7 and self.grid[last_row + i][last_col] == color:
            total += 1
            i += 1
        if total == 4:
            return True
        # diagonal 1
        total = 1
        i = 1
        while last_row - i >= 0 and last_col - i >= 0 and self.grid[last_row - i][last_col - i] == color:
            total += 1
            i += 1
        i = 1
        while last_row + i < 7 and last_col + i < 7 and self.grid[last_row + i][last_col + i] == color:
            total += 1
            i += 1
        if total == 4:
            return True
        # diagonal 2
        total = 1
        i = 1
        while last_row - i >= 0 and last_col + i < 7 and self.grid[last_row - i][last_col + i] == color:
            total += 1
            i += 1
        i = 1
        while last_row + i < 7 and last_col - i >= 0 and self.grid[last_row + i][last_col - i] == color:
            total += 1
            i += 1
        if total == 4:
            return True
        return False

    @property
    def last_move(self):
        return self.move_history[-1]



