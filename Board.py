class Board:
    def __init__(self):
        self.grid = [[None for _ in range(7)] for _ in range(7)]
        self.heights = [6 for _ in range(7)]
        self.last_col = None

    def update(self, column, color):
        if self.heights[column] == -1:
            print('Column already full, please choose another')
            return False
        self.grid[self.heights[column]][column] = color
        self.heights[column] -= 1
        self.last_col = column
        return True

    def cancel(self):
        self.grid[self.heights[self.last_col] + 1][self.last_col] = None
        self.heights[self.last_col] += 1

    def is_full(self):
        return all([height == -1 for height in self.heights])



