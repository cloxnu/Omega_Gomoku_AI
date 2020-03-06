from abc import ABCMeta, abstractmethod
from Game.Game import Game


class Player(metaclass=ABCMeta):

    @abstractmethod
    def take_action(self, board: Game):
        """
        下一步玩家应该执行的动作。
        What the player should do next.
        :param board: 当前棋盘。 Current board.
        :return: <tuple (i, j)> 采取行动时，落子的坐标。 Coordinate of the action.
        """
