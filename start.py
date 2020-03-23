import Game.Board as BOARD
import Game.Game as Game
from Game.ConsoleRenderer import ConsoleRenderer

from console_select import select_player, select_network, set_AI_conf

from Player.Human import Human
from Player.AI_MCTS import AI_MCTS
from Player.AI_MCTS_Net import AI_MCTS_Net

from configure import Configure


def start():
    conf = Configure()
    conf.get_conf()

    def player_init(player_selected, name):
        if player_selected == 1:
            return Human(name=name)
        elif player_selected == 2:
            search_times, greedy_value = set_AI_conf(search_times=2000, greedy_value=5.0)
            return AI_MCTS(name=name,
                           search_times=search_times,
                           greedy_value=greedy_value,
                           is_output_analysis=conf.conf_dict["AI_is_output_analysis"])
        elif player_selected == 3:
            network = select_network()
            search_times, greedy_value = set_AI_conf(search_times=400, greedy_value=5.0)
            return AI_MCTS_Net(name=name,
                               policy_value_function=network.predict,
                               is_training=False,
                               search_times=search_times,
                               greedy_value=greedy_value,
                               is_output_analysis=conf.conf_dict["AI_is_output_analysis"])

    player1_selected, name1 = select_player("请输入先落子玩家。\n"
                                            "1: 人类\n"
                                            "2: 纯蒙特卡洛树搜索的 AI\n"
                                            "3: 带有神经网络的蒙特卡洛树搜索 AI\n"
                                            "Please input first player.\n"
                                            "1: Human\n"
                                            "2: AI with pure Monte Carlo tree search\n"
                                            "3: AI with Monte Carlo tree search & neural network\n"
                                            ": ", allowed_input=[1, 2, 3])

    player1 = player_init(player1_selected, name1)

    player2_selected, name2 = select_player("请输入后落子玩家。\n"
                                            "1: 人类\n"
                                            "2: 纯蒙特卡洛树搜索的 AI\n"
                                            "3: 带有神经网络的蒙特卡洛树搜索 AI\n"
                                            "Please input second player.\n"
                                            "1: Human\n"
                                            "2: AI with pure Monte Carlo tree search\n"
                                            "3: AI with Monte Carlo tree search & neural network\n"
                                            ": ", allowed_input=[1, 2, 3])

    player2 = player_init(player2_selected, name2)

    console_renderer = ConsoleRenderer()

    print("############### 游戏开始 Game Start ###############")
    winner = Game.start_until_game_over(player1, player2, board_renderer=console_renderer)
    if winner == BOARD.o:
        print("恭喜！\"O\" 获胜。 Congrats! \"O\" wins.")
    elif winner == BOARD.x:
        print("恭喜！\"X\" 获胜。 Congrats! \"X\" wins.")
    else:
        print("平局！ Draw!")
    print("############### 游戏结束 Game Over ###############")


if __name__ == '__main__':
    start()
