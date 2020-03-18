from Game.BoardRenderer import BoardRenderer
import Game.Board as BOARD
from Game.Board import Board


class ConsoleRenderer(BoardRenderer):

    def render(self, board: Board):
        """
        以控制台方式渲染当前棋盘。
        Render the current board in console mode
        :param board: 棋盘。 The board.
        """
        # 建立一个 16 * 16 的二维数组。 Build a 16 * 16 array.
        print_array = [["" for _ in range(BOARD.board_size + 1)] for _ in range(BOARD.board_size + 1)]

        index_string = [""] + [str(i) for i in range(BOARD.board_size)]

        # 行列序号赋值。 Row & Column Index.
        print_array[0] = index_string
        for row in range(BOARD.board_size):
            print_array[row + 1][0] = str(row)

        for i in range(BOARD.board_size):
            for j in range(BOARD.board_size):
                if board.board[i, j] == BOARD.o:
                    print_array[i + 1][j + 1] = "O"
                elif board.board[i, j] == BOARD.x:
                    print_array[i + 1][j + 1] = "X"
                else:
                    print_array[i + 1][j + 1] = "."

        # 输出。 Print.
        for i in range(BOARD.board_size + 1):
            for j in range(BOARD.board_size + 1):
                print("{:^3}".format(print_array[i][j]), end="")
            print("")
