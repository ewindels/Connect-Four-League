from Board import Board


class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]
        self.turn = 0
        self.winner = None
        self.loser = None
        self.draw = False

    @property
    def player_turn(self):
        return self.players[self.turn % 2]

    def print_turn(self):
        print('Turn {} - Player {} ({})'.format(self.turn, self.turn % 2, self.board.color))

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
        player_choice = self.player_turn.play(self)
        self.board.update(player_choice)
        self.turn += 1

    def full_game(self, log=False):

        while not (self.winner is not None or self.draw):
            if log:
                self.print_turn()
                self.print_board()
            self.play_turn()
            if self.turn >= 7 and self.board.check_victory:
                self.loser = self.player_turn
                self.turn -= 1
                self.winner = self.player_turn
                self.winner.victories += 1
                self.loser.defeats += 1
                if log:
                    self.print_board()
                    print('Player {} won !'.format(self.turn % 2))
            if self.board.is_full:
                self.draw = True
                self.players[0].draws += 1
                self.players[1].draws += 1
                if log:
                    print('Draw')
        return self.winner

    def reset(self):
        self.board = Board()
        self.turn = 0
        self.winner = None
        self.loser = None
        self.draw = False
