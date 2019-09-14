from Board import Board


class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]
        self.player_turn_n = 0
        self.turn = 1
        self.winner = None
        self.draw = False

    def print_turn(self):
        print('Turn {} - Player {} ({})'.format(self.turn, self.player_turn_n, self.board.color))

    def print_board(self):
        print('╔' + '═══╤' * 6 + '═══╗')
        for row in self.board.grid[:-1]:
            print('║ ' + ' │ '.join([color if color else ' ' for color in row]) + ' ║')
            print('╟' + '───┼' * 6 + '───╢')
        print('║ {0} ║'.format(' │ '.join([color if color else ' ' for color in self.board.grid[-1]])))
        print('╚' + '═══╧' * 6 + '═══╝')

    def switch_players(self):
        self.players.reverse()

    def play_turn(self):
        player = self.players[self.player_turn_n]
        player_choice = player.play(self)
        self.board.update(player_choice)
        self.turn += 1
        self.player_turn_n = (self.player_turn_n + 1) % 2

    def full_game(self, log=False):

        while not (self.winner is not None or self.draw):
            if log:
                self.print_turn()
                self.print_board()
            self.play_turn()
            if self.turn >= 7 and self.board.check_victory:
                self.winner = (self.player_turn_n + 1) % 2
                if log:
                    self.print_board()
                    print('Player {} won !'.format(self.winner))
            if self.board.is_full:
                self.draw = True
                if log:
                    print('Draw')
        return self.winner

    def reset(self):
        self.board = Board()
        self.player_turn_n = 0
        self.turn = 1
        self.winner = None
        self.draw = False
