from abc import ABCMeta, abstractmethod


class BoardRenderer(metaclass=ABCMeta):

    @abstractmethod
    def render(self, board):
        """
        棋盘渲染。
        The board rendering.
        :param board: 棋盘。 The checkerboard.
        """