import numpy as np

from Game.BoardRenderer import BoardRenderer
from Function import coordinates_set
from configure import Configure


conf = Configure()
conf.get_conf()

# 固定配置。 Fixed Configuration.
o = conf.conf_dict["o"]
x = conf.conf_dict["x"]
empty = conf.conf_dict["empty"]

# 可变配置。 Changeable Configuration.
n_in_a_row = conf.conf_dict["n_in_a_row"]   # 几子连珠。 How many pieces in a row.
o_win = n_in_a_row
x_win = -n_in_a_row
start_player = conf.conf_dict["start_player"]  # start player
board_size = conf.conf_dict["board_size"]   # 棋盘大小。 The size of the board.


class Board:

    def __init__(self):
        self.board = np.zeros((board_size, board_size))
        self.available_actions = coordinates_set(board_size, board_size)
        self.last_action = None  # 上次的落子。 Last move.
        self.current_player = start_player  # current player

    def __copy__(self):
        new_board = Board()
        new_board.board = self.board.copy()
        new_board.available_actions = self.available_actions.copy()
        new_board.last_action = self.last_action
        new_board.current_player = self.current_player
        return new_board

    def reset(self):
        """
        重置棋盘。
        Reset board.
        """
        self.board = np.zeros((board_size, board_size))
        self.available_actions = coordinates_set(board_size, board_size)
        self.last_action = None
        self.current_player = start_player  # current player

    def render(self, board_renderer: BoardRenderer):
        """
        渲染当前棋盘。
        Render current board.
        :param board_renderer: 棋盘渲染器。 The board renderer.
        """
        board_renderer.render(self)

    def step(self, action):
        """
        执行下一步动作，调用后棋盘状态改变。
        The next action is performed, and the state of the board changes after calling.
        :param action: <tuple (i, j)> 落子的坐标。 Coordinates of the action.
        :return: <Bool> 落子是否合法。 Validity of the action.
        """
        i = action[0]
        j = action[1]
        if (i, j) not in self.available_actions:
            return False
        self.board[i, j] = self.current_player
        self.available_actions.remove((i, j))
        self.last_action = (i, j)
        self.current_player = -self.current_player  # 该对方了。 It's turn to opponent.
        return True

    def result(self):
        """
        分析当前局面是否有玩家胜利，或者平局，或者未结束。
        Analyze whether the current situation has a player victory, or a draw, or is not over.
        :return: <tuple (is_over, winner)>
        """
        # 没地儿下了。 Nowhere to move.
        if len(self.available_actions) == 0:
            return True, empty

        for piece in coordinates_set(board_size, board_size) - self.available_actions:
            i = piece[0]
            j = piece[1]

            # 横向扫描。 Horizontal scan.
            if j in range(board_size - n_in_a_row + 1):
                s = sum([self.board[i, j + v] for v in range(n_in_a_row)])
                if s == o_win or s == x_win:
                    return True, s / n_in_a_row

            # 纵向扫描。 Vertical scan.
            if i in range(board_size - n_in_a_row + 1):
                s = sum([self.board[i + v, j] for v in range(n_in_a_row)])
                if s == o_win or s == x_win:
                    return True, s / n_in_a_row

            # 斜向右下扫描。 Scan diagonally right.
            if i in range(board_size - n_in_a_row + 1) and j in range(board_size - n_in_a_row + 1):
                s = sum([self.board[i + v, j + v] for v in range(n_in_a_row)])
                if s == o_win or s == x_win:
                    return True, s / n_in_a_row

            # 斜向左下扫描。 Scan diagonally left.
            if i not in range(n_in_a_row - 1) and j in range(board_size - n_in_a_row + 1):
                s = sum([self.board[i - v, j + v] for v in range(n_in_a_row)])
                if s == o_win or s == x_win:
                    return True, s / n_in_a_row

        return False, empty
