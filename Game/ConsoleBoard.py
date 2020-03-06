import numpy as np
import Game.Game as GAME
from Game.Game import Game
from Function import coordinates_set


class ConsoleBoard(Game):

    def __init__(self):
        super().__init__()

    def reset(self):
        """
        重置棋盘。
        Reset board.
        """
        self.board = np.zeros((GAME.board_size, GAME.board_size), dtype=np.int32)
        self.available_actions = coordinates_set(GAME.board_size, GAME.board_size)
        self.current_player = GAME.start_player  # current player

    def render(self):
        """
        渲染当前棋盘。
        Render current board.
        """
        # 建立一个 16 * 16 的二维数组。 Build a 16 * 16 array.
        print_array = [["" for _ in range(GAME.board_size + 1)] for _ in range(GAME.board_size + 1)]

        index_string = [""] + [str(i) for i in range(GAME.board_size)]

        # 行列序号赋值。 Row & Column Index.
        print_array[0] = index_string
        for row in range(GAME.board_size):
            print_array[row + 1][0] = str(row)

        for i in range(GAME.board_size):
            for j in range(GAME.board_size):
                if self.board[i, j] == GAME.o:
                    print_array[i + 1][j + 1] = "O"
                elif self.board[i, j] == GAME.x:
                    print_array[i + 1][j + 1] = "X"
                else:
                    print_array[i + 1][j + 1] = "."

        # 输出。 Print.
        for i in range(GAME.board_size + 1):
            for j in range(GAME.board_size + 1):
                print("{:^3}".format(print_array[i][j]), end="")
            print("")

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
        self.current_player = -self.current_player  # 该对方了。 It's turn to opponent.
        return True

    def result(self):
        """
        分析当前局面是否有玩家胜利，或者平局，或者未结束。
        Analyze whether the current situation has a player victory, or a draw, or is not over.
        :return: <tuple (is_over, winner)>
        """
        for piece in coordinates_set(GAME.board_size, GAME.board_size) - self.available_actions:
            i = piece[0]
            j = piece[1]

            # 横向扫描。 Horizontal scan.
            if j in range(GAME.board_size - GAME.n_in_a_row + 1):
                s = sum([self.board[i, j + v] for v in range(GAME.n_in_a_row)])
                if s == GAME.o_win or s == GAME.x_win:
                    return True, s / GAME.n_in_a_row

            # 纵向扫描。 Vertical scan.
            if i in range(GAME.board_size - GAME.n_in_a_row + 1):
                s = sum([self.board[i + v, j] for v in range(GAME.n_in_a_row)])
                if s == GAME.o_win or s == GAME.x_win:
                    return True, s / GAME.n_in_a_row

            # 斜向右下扫描。 Scan diagonally right.
            if i in range(GAME.board_size - GAME.n_in_a_row + 1) and j in range(GAME.board_size - GAME.n_in_a_row + 1):
                s = sum([self.board[i + v, j + v] for v in range(GAME.n_in_a_row)])
                if s == GAME.o_win or s == GAME.x_win:
                    return True, s / GAME.n_in_a_row

            # 斜向左下扫描。 Scan diagonally left.
            if i not in range(GAME.n_in_a_row - 1) and j in range(GAME.board_size - GAME.n_in_a_row + 1):
                s = sum([self.board[i - v, j + v] for v in range(GAME.n_in_a_row)])
                if s == GAME.o_win or s == GAME.x_win:
                    return True, s / GAME.n_in_a_row

        # 没地儿下了。 Nowhere to move.
        if len(self.available_actions) == 0:
            return True, GAME.empty

        return False, GAME.empty


