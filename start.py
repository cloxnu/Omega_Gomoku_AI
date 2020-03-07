import Game.Game as GAME
from Game.ConsoleBoard import ConsoleBoard
from Player.Human import Human
from Player.AI.AI_MCTS import AI_MCTS


def start():
    player1 = Human(name="Human1")
    player2 = Human(name="Human2")
    ai1 = AI_MCTS(name="AI_MCTS")
    ai2 = AI_MCTS(name="AI_MCTS")
    board = ConsoleBoard()

    while True:
        # 渲染。 Render.
        board.render()

        # 采取动作。 Take action.
        if board.current_player == GAME.x:
            # player1.take_action(board)
            ai2.take_action(board, is_output_analysis=True)
        else:
            ai1.take_action(board, is_output_analysis=True)

        # 游戏是否结束。 Game over?
        is_over, winner = board.result()
        if is_over:
            board.render()
            if winner == GAME.o:
                print("恭喜！\"O\" 获胜。 Congrats! \"O\" wins.")
            elif winner == GAME.x:
                print("恭喜！\"X\" 获胜。 Congrats! \"X\" wins.")
            else:
                print("平局！ Draw!")
            break


if __name__ == '__main__':
    start()
