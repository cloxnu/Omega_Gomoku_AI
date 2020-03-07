import Game.Game as GAME
from Game.ConsoleBoard import ConsoleBoard
from Player.Human import Human
from Player.AI.AI_MCTS import AI_MCTS
from choose_player import choose


def start():
    player1, name1 = choose("请输入先落子玩家。(人类: 1, AI: 2)\n"
                            "Please input first player. (human: 1, AI: 2)\n"
                            ": ")
    player2, name2 = choose("请输入后落子玩家。(人类: 1, AI: 2)\n"
                            "Please input second player. (human: 1, AI: 2)\n"
                            ": ")
    player1 = Human(name=name1) if player1 else AI_MCTS(name=name1)
    player2 = Human(name=name2) if player2 else AI_MCTS(name=name2)

    board = ConsoleBoard()

    while True:
        # 渲染。 Render.
        board.render()

        # 采取动作。 Take action.
        if board.current_player == GAME.o:
            player1.take_action(board)
        else:
            player2.take_action(board)

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
