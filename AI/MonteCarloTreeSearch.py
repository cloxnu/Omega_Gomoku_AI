from abc import ABCMeta, abstractmethod

from Game.Board import Board


class MonteCarloTreeSearch(metaclass=ABCMeta):

    def __init__(self):
        self.root = None

    @abstractmethod
    def run(self, board: Board, times):
        """
        蒙特卡洛树，开始搜索...
        Monte Carlo Tree, start searching...
        :param board:
        :param times: 运行次数。run times.
        :return: 最佳的执行动作。 the best action.
        """
