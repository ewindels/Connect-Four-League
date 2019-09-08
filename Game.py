from Board import Board


class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]
        self.player_turn_n = 0
        self.turn = 1
        self.last_choice = None
        self.winner = None
        self.draw = False

    def print_turn(self):
        print('Turn {} - Player {}'.format(self.turn, self.player_turn_n))

    def print_board(self):
        print('╔' + '═══╤' * 6 + '═══╗')
        for row in self.board.grid[:-1]:
            print('║ ' + ' │ '.join([color if color else ' ' for color in row]) + ' ║')
            print('╟' + '───┼' * 6 + '───╢')
        print('║ ' + ' │ '.join([color if color else ' ' for color in self.board.grid[-1]]) + ' ║')
        print('╚' + '═══╧' * 6 + '═══╝')

    def check_victory(self, last_row, last_col):
        color = self.board.grid[last_row][last_col]
        # horizontal
        total = 1
        i = 1
        while last_col - i >= 0 and self.board.grid[last_row][last_col - i] == color:
            total += 1
            i += 1
        i = 1
        while last_col + i < 7 and self.board.grid[last_row][last_col + i] == color:
            total += 1
            i += 1
        if total == 4:
            return True
        # vertical
        total = 1
        i = 1
        while last_row - i >= 0 and self.board.grid[last_row - i][last_col] == color:
            total += 1
            i += 1
        i = 1
        while last_row + i < 7 and self.board.grid[last_row + i][last_col] == color:
            total += 1
            i += 1
        if total == 4:
            return True
        # diagonal 1
        total = 1
        i = 1
        while last_row - i >= 0 and last_col - i >= 0 and self.board.grid[last_row - i][last_col - i] == color:
            total += 1
            i += 1
        i = 1
        while last_row + i < 7 and last_col + i < 7 and self.board.grid[last_row + i][last_col + i] == color:
            total += 1
            i += 1
        if total == 4:
            return True
        # diagonal 2
        total = 1
        i = 1
        while last_row - i >= 0 and last_col + i < 7 and self.board.grid[last_row - i][last_col + i] == color:
            total += 1
            i += 1
        i = 1
        while last_row + i < 7 and last_col - i >= 0 and self.board.grid[last_row + i][last_col - i] == color:
            total += 1
            i += 1
        if total == 4:
            return True
        return False

    def play_turn(self):
        player = self.players[self.player_turn_n]
        player_choice = player.play(self)
        self.board.update(player_choice, player.color)
        self.turn += 1
        self.last_choice = player_choice
        self.player_turn_n = (self.player_turn_n + 1)%2

    def full_game(self, log=False):

        while not (self.winner is not None or self.draw):
            if log:
                self.print_turn()
                self.print_board()
            self.play_turn()
            victory = self.check_victory(self.board.heights[self.last_choice] + 1, self.last_choice)
            if victory:
                self.winner = (self.player_turn_n + 1)%2
                if log:
                    self.print_turn()
                    self.print_board()
                    print('Player {} won !'.format(self.player_turn_n))
            self.draw = self.board.is_full()
            if self.draw:
                if log:
                    print('Draw')
        return self.winner

    def reset(self):
        self.board = Board()
        self.player_turn_n = 0
        self.turn = 1
        self.last_choice = None
        self.winner = None
        self.draw = False
