from Player.Player import Player
from Game.Board import Board
import Game.Board as BOARD
from Game.BoardRenderer import BoardRenderer


def start_until_game_over(player1: Player, player2: Player, board_renderer: BoardRenderer = None):
    """
    玩家 player1 和玩家 player2 在 board 上进行游戏直到游戏结束，并输出获胜者。
    Player player1 and player2 play on the board until the game is over, and output the winner.
    :param player1: 玩家 1。 Player 1.
    :param player2: 玩家 2。 Player 2.
    :param board_renderer: 棋盘渲染器。 Checkerboard renderer.
    :return: <int> board 返回的获胜者。 The winner returned by board.
    """
    board = Board()
    while True:
        # 渲染。 Render.
        if board_renderer is not None:
            board.render(board_renderer)

        # 执行动作。 Take action.
        if board.current_player == BOARD.o:
            player1.take_action(board, is_output_action=board_renderer is not None)
        else:
            player2.take_action(board, is_output_action=board_renderer is not None)

        # 游戏是否结束。 Game over?
        is_over, winner = board.result()
        if is_over:
            if board_renderer is not None:
                board.render(board_renderer)
            return winner
