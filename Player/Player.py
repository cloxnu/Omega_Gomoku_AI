from abc import ABCMeta, abstractmethod
from Game.Board import Board


class Player(metaclass=ABCMeta):

    @abstractmethod
    def take_action(self, board: Board, is_output_action=True):
        """
        下一步玩家应该执行的动作。
        What the player should do next.
        :param board: 当前棋盘。 Current board.
        :param is_output_action:
        :return: <tuple (i, j)> 采取行动时，落子的坐标。 Coordinate of the action.
        """
