import numpy as np
from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax, SSS
"""
Authors: Krzysztof Skwira & Tomasz Lemke
"""


class ConnectFour(TwoPlayerGame):
    """
    The game of Connect Four, as described on wikipedia:
    https://en.wikipedia.org/wiki/Connect_Four
    """

    def __init__(self, players, board=None):
        self.players = players
        self.board = board if (board is not None) else (
            np.array([[0 for i in range(7)] for j in range(6)]))
        self.current_player = 1  # player 1 starts.

    def possible_moves(self):
        """Repeat the draw if invalid column selected"""
        return [i for i in range(7) if (self.board[:, i].min() == 0)]

    def make_move(self, column):
        """Adding piece to selected column"""
        line = np.argmin(self.board[:, column] != 0)
        self.board[line, column] = self.current_player

    def show(self):
        """Showing board with current pieces played"""
        print('\n' + '\n'.join(
            ['0 1 2 3 4 5 6', 13 * '-'] +
            [' '.join([['.', 'O', 'X'][self.board[5 - j][i]]
                       for i in range(7)]) for j in range(6)]))

    def lose(self):
        """Checking if opponent has won"""
        return find_four(self.board, self.opponent_index)

    def is_over(self):
        """Checking if the game ended either by lack of moves or winning condition met"""
        return (self.board.min() > 0) or self.lose()

    def scoring(self):
        """Simple logic to prevent the algorithm to select a losing move if other options are available"""
        return -100 if self.lose() else 0


def find_four(board, current_player):
    """Returns True if the player has connected 4 (or more) in a line"""
    for pos, direction in POS_DIR:
        streak = 0
        while (0 <= pos[0] <= 5) and (0 <= pos[1] <= 6):
            if board[pos[0], pos[1]] == current_player:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
            pos = pos + direction
    return False


POS_DIR = np.array([[[i, 0], [0, 1]] for i in range(6)] +
                   [[[0, i], [1, 0]] for i in range(7)] +
                   [[[i, 0], [1, 1]] for i in range(1, 3)] +
                   [[[0, i], [1, 1]] for i in range(4)] +
                   [[[i, 6], [1, -1]] for i in range(1, 3)] +
                   [[[0, i], [1, -1]] for i in range(3, 7)])


ai_algo_neg = Negamax(5)
ai_algo_sss = SSS(5)
game = ConnectFour([AI_Player(ai_algo_neg), AI_Player(ai_algo_sss)])
game.play()
if game.lose():
    print(f"Player {game.opponent_index} wins.")
else:
    print("It's a draw.")
