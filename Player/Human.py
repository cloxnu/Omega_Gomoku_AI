from Game.Game import Game
from Player.Player import Player


class Human(Player):

    def __init__(self, name="Human"):
        self.name = name

    def take_action(self, board: Game):
        """
        电脑前的玩家应该采取动作了。 It's turn to you.
        :param board: 当前局面。 Current board.
        :return: <tuple (i, j)> 采取行动时，落子的坐标。 Coordinate of the action.
        """
        print("该 {} 落子了，它是人类选手。 It's turn to {}, human player.".format(self.name, self.name))
        while True:
            # 输入。 Input.
            input_str = input(
                "请输入 {} 想要落子的坐标，格式为 \"[行],[列]\"：\n"
                "Please input the coordinates {} wants to move, "
                "the format is \"[Row],[Column]\":\n".format(self.name, self.name))

            # 验证。 Validate.
            try:
                action = [int(index) for index in input_str.split(",")]
            except:
                print("输入格式有误，请重新输入。\nThe input format is incorrect. Please try again.\n")
                continue

            # 执行。 Execute.
            if not board.step(action):
                print("无法在此落子，请重新输入。\nCannot move here. Please try again.\n")
                continue

            break
