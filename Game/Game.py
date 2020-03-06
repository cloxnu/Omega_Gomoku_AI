from abc import ABCMeta, abstractmethod, abstractproperty
import numpy as np

from Function import coordinates_set

# 固定配置。 Fixed Configuration.
o = 1
x = -1
empty = 0

# 可变配置。 Changeable Configuration.
n_in_a_row = 5   # 几子连珠。 How many pieces in a row.
o_win = n_in_a_row
x_win = -n_in_a_row
start_player = o  # start player
board_size = 8   # 棋盘大小。 The size of the board.


class Game(metaclass=ABCMeta):

    def __init__(self):
        self.board = np.zeros((board_size, board_size), dtype=np.int32)
        self.available_actions = coordinates_set(board_size, board_size)
        self.current_player = start_player  # current player

    @abstractmethod
    def reset(self):
        """
        重置棋盘。
        Reset board.
        """

    @abstractmethod
    def render(self):
        """
        渲染当前棋盘。
        Render current board.
        """

    @abstractmethod
    def step(self, action):
        """
        执行下一步动作，调用后棋盘状态改变。
        The next action is performed, and the state of the board changes after calling.
        :param action: <tuple (i, j)> 落子的坐标。 Coordinates of the action.
        :return: <Bool> 落子是否合法。 Validity of the action.
        """

    @abstractmethod
    def result(self):
        """
        分析当前局面是否有玩家胜利，或者平局，或者未结束。
        Analyze whether the current situation has a player victory, or a draw, or is not over.
        :return: <tuple (is_over, winner)>
        """
