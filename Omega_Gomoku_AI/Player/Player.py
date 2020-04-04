from abc import ABCMeta, abstractmethod
from Game.Board import Board


class Player(metaclass=ABCMeta):

    @abstractmethod
    def take_action(self, board: Board, is_output_action=True, running_output_function=None, is_stop=None):
        """
        下一步玩家应该执行的动作。
        What the player should do next.
        :param board: 当前棋盘。 Current board.
        :param is_output_action: 是否输出 action 信息。 Whether to output action information.
        :param running_output_function: 输出 running 的函数。 running output function.
        :param is_stop: 询问是否停止。 Ask whether to stop.
        :return: <tuple (i, j)> 采取行动时，落子的坐标。 Coordinate of the action.
        """
