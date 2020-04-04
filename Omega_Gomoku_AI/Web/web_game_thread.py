import threading

import Game.Board as BOARD
from Game.Board import Board
from Player.Player import Player
from Player.Human import Human


class web_game_thread(threading.Thread):

    def __init__(self, player1: Player, player2: Player, turn_to, send_board_step,
                 send_player1_running, send_player2_running, wait_human_action, game_over):
        super().__init__()
        self.is_stop = False
        self.player1 = player1
        self.player2 = player2
        self.turn_to = turn_to
        self.send_board_step = send_board_step
        self.send_player1_running = send_player1_running
        self.send_player2_running = send_player2_running
        self.wait_human_action = wait_human_action
        self.game_over = game_over

    def run(self) -> None:
        play_web_game(self.is_stop_fn, self.player1, self.player2, self.turn_to, self.send_board_step,
                      self.send_player1_running, self.send_player2_running,
                      self.wait_human_action, self.game_over)

    def stop(self):
        self.is_stop = True

    def is_stop_fn(self) -> bool:
        return self.is_stop


def play_web_game(is_stop, player1: Player, player2: Player, turn_to, send_board_step,
                  send_player1_running, send_player2_running, wait_human_action, game_over):
    board = Board()
    while not is_stop():
        turn_to(board.current_player)

        if board.current_player == BOARD.o:
            if isinstance(player1, Human):
                action = wait_human_action(1, is_stop)
                if is_stop():
                    return
                board.step(action)
            else:
                action = player1.take_action(board, is_output_action=False,
                                             running_output_function=send_player1_running, is_stop=is_stop)
            send_board_step(1, action)
        else:
            if isinstance(player2, Human):
                action = wait_human_action(2, is_stop)
                if is_stop():
                    return
                board.step(action)
            else:
                action = player2.take_action(board, is_output_action=False,
                                             running_output_function=send_player2_running, is_stop=is_stop)
            send_board_step(2, action)

        # 游戏是否结束。 Game over?
        is_over, winner = board.result()
        if is_over:
            game_over(winner)
            return
