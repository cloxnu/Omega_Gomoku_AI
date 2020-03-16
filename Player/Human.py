from Game.Board import Board
from Player.Player import Player


class Human(Player):

    def __init__(self, name="Human"):
        self.name = name

    def take_action(self, board: Board, is_output_action=True):
        """
        电脑前的玩家应该采取动作了。 It's turn to you.
        :param board: 当前局面。 Current board.
        :param is_output_action:
        :return: <tuple (i, j)> 采取行动时，落子的坐标。 Coordinate of the action.
        """
        print("该 {0} 落子了，它是人类选手。 It's turn to {0}, human player.".format(self.name))
        while True:
            # 输入。 Input.
            input_str = input(
                "请输入 {0} 想要落子的坐标，格式为 \"[行],[列]\"：\n"
                "Please input the coordinates {0} wants to move, "
                "the format is \"[Row],[Column]\":\n".format(self.name))

            # 验证。 Validate.
            try:
                if input_str.isdigit():
                    print("请输入完整坐标。\nPlease enter full coordinates.\n")
                    continue
                action = [int(index) for index in input_str.split(",")]
            except:
                print("输入格式有误，请重新输入。\nThe input format is incorrect. Please try again.\n")
                continue

            # 执行。 Execute.
            if not board.step(action):
                print("无法在此落子，请重新输入。\nCannot move here. Please try again.\n")
                continue

            print("人类选手 {0} 落子于 ({1}, {2})\nHuman player {0} moves ({1}, {2})\n".format(self.name, action[0], action[1]))
            break
