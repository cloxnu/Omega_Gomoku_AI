import numpy as np
import copy

from Game.Game import Game
import Game.Game as GAME
from Player.AI.MonteCarloTreeSearch import MonteCarloTreeSearch
from Player.AI.MonteCarloTreeNode import TreeNode
from Player.Player import Player
from configure import Configure

conf = Configure()
conf.get_conf()
AI_search_times = conf.conf_dict["AI_search_times"]
is_output_analysis = conf.conf_dict["AI_is_output_analysis"]


class AI_MCTS(MonteCarloTreeSearch, Player):

    def __init__(self, name="AI_MCTS"):
        super().__init__()
        self.name = name
        self.time = []

    def reset(self, board: Game):
        self.root = TreeNode(board, prior_prob=1.0)

    def take_action(self, board: Game):
        """
        下一步 AI 玩家应该执行的动作。
        What the AI player should do next.
        :param board: 当前棋盘。 Current board.
        :return: <tuple (i, j)> 采取行动时，落子的坐标。 Coordinate of the action.
        """
        print("该 {0} 落子了，它是 AI 选手。 It's turn to {0}, AI player.".format(self.name))
        print("思考中。。。 Thinking...")

        self.reset(board)
        self.run(AI_search_times)
        action, _ = self.root.choose_best_child(0)
        board.step(action)

        if is_output_analysis:
            self.output_analysis()

        print("AI 选手 {0} 落子于 ({1}, {2})\nAI player {0} moves ({1}, {2})".format(self.name, action[0], action[1]))

    def output_analysis(self):
        """
        输出棋子胜率分析。
        Analysis of winning ratio of output pieces.
        """
        print("----------------------------\n"
              "AI 分析： AI analysis:\n"
              "格式：[胜率(%) | 计算次数]  Format: [odds(%) | #calculations]")
        # 建立一个 16 * 16 的二维数组。 Build a 16 * 16 array.
        print_array = [["" for _ in range(GAME.board_size + 1)] for _ in range(GAME.board_size + 1)]

        index_string = [""] + [str(i) for i in range(GAME.board_size)]

        # 行列序号赋值。 Row & Column Index.
        print_array[0] = index_string
        for row in range(GAME.board_size):
            print_array[row + 1][0] = str(row)

        for i in range(GAME.board_size):
            for j in range(GAME.board_size):
                if (i, j) in self.root.children:
                    visited_times = float(self.root.children[(i, j)].visited_times)
                    reward = float(self.root.children[(i, j)].reward)
                    print_array[i + 1][j + 1] = "{0:.1f}%".format(-reward / visited_times * 100) + "|" + str(int(visited_times))
                # if self.board[i, j] == GAME.o:
                #     print_array[i + 1][j + 1] = "O"
                # elif self.board[i, j] == GAME.x:
                #     print_array[i + 1][j + 1] = "X"
                # else:
                #     print_array[i + 1][j + 1] = "."

        # 输出。 Print.
        for i in range(GAME.board_size + 1):
            for j in range(GAME.board_size + 1):
                print("{:<15}".format(print_array[i][j]), end="")
            print("")
        print("----------------------------")

    def run(self, times):
        """
        蒙特卡洛树，开始搜索...
        Monte Carlo Tree, start searching...
        :param times: 运行次数。run times.
        :return: 最佳的执行动作。 the best action.
        """
        for i in range(times):
            if i % 20 == 0:
                print("\rrunning: {} / {}".format(i, times), end="")
            expanded_node = self.traverse(self.root)
            winner = self.rollout(expanded_node)
            self.backpropagate(expanded_node, winner)
        print("")

    def traverse(self, node: TreeNode):
        """
        扩展子节点。
        Expand node.
        :param node: 当前节点。 Current node.
        :return: <TreeNode> 扩展出的节点。 Expanded nodes.
        """
        while True:
            is_over, _ = node.board.result()
            if is_over:
                break
            if node.is_full_expand():
                _, node = node.choose_best_child()
            else:
                prob = 1.0 / len(node.board.available_actions)
                return node.expand(prob)
        return node

    def rollout(self, node: TreeNode):
        """
        模拟。
        Simulation.
        :param node: 当前节点。 Current node.
        :return: winner<int> 获胜者。 winner.
        """
        while True:
            is_over, winner = node.board.result()
            if is_over:
                break
            node = self.rollout_policy(node)
        return winner

    def rollout_policy(self, node: TreeNode):
        """
        决策函数，选择子节点的概率决策。
        Policy function, a probabilistic decision to select child nodes.
        :param node: 当前节点。 Current node.
        :return: <TreeNode> 决策出的节点。 The decision node.
        """

        # 所有执行动作的概率相同。 All actions have the same probability.
        actions = list(node.board.available_actions)
        probs = np.ones(len(actions)) / len(actions)

        # 获得动作和概率。 Get action and probability.
        action_index = np.random.choice(range(len(actions)), p=probs)
        action = actions[action_index]
        prob = probs[action_index]

        # 执行。 Action.
        next_board = copy.deepcopy(node.board)
        next_board.step(action)

        return TreeNode(next_board, prob, parent=node)

    def backpropagate(self, node: TreeNode, winner):
        """
        反向传输，将结果返回父节点。
        Backpropagate, passing the result to the parent node.
        :param node: 当前节点。 Current node.
        :param winner: 获胜的玩家。 Winning player.
        """
        node.visited_times += 1

        if winner == node.board.current_player:
            node.reward += 1
        elif winner == -node.board.current_player:
            node.reward -= 1

        if not node.is_root():
            node.backpropagate(winner)
