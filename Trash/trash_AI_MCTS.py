import numpy as np
import copy
import datetime

from Game.Board import Board
import Game.Board as BOARD
from AI.MonteCarloTreeSearch import MonteCarloTreeSearch
from AI.MonteCarloTreeNode import TreeNode
from Player.Player import Player


class AI_MCTS(MonteCarloTreeSearch, Player):

    def __init__(self, name="AI_MCTS", search_times=2000, is_output_analysis=True):
        super().__init__()
        self.name = name

        self.search_times = search_times  # 树搜索次数。 The search times of tree.
        self.is_output_analysis = is_output_analysis  # 是否输出 AI 分析。 Whether to output AI analysis.

    def reset(self):
        self.root = TreeNode(prior_prob=1.0)

    def take_action(self, board: Board):
        """
        下一步 AI 玩家执行动作。
        The AI player take action next step.
        :param board: 当前棋盘。 Current board.
        """
        print("该 {0} 落子了，它是 AI 选手。 It's turn to {0}, AI player.".format(self.name))
        print("思考中。。。 Thinking...")

        self.reset()
        self.run(board, self.search_times)
        action, _ = self.root.choose_best_child(0)
        board.step(action)

        if self.is_output_analysis:
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
        print_array = [["" for _ in range(BOARD.board_size + 1)] for _ in range(BOARD.board_size + 1)]

        index_string = [""] + [str(i) for i in range(BOARD.board_size)]

        # 行列序号赋值。 Row & Column Index.
        print_array[0] = index_string
        for row in range(BOARD.board_size):
            print_array[row + 1][0] = str(row)

        # 填充内容。 Fill Content.
        for i in range(BOARD.board_size):
            for j in range(BOARD.board_size):
                if (i, j) in self.root.children:
                    visited_times = float(self.root.children[(i, j)].visited_times)
                    reward = float(self.root.children[(i, j)].reward)
                    print_array[i + 1][j + 1] = "{0:.1f}%".format(-reward / visited_times * 100) + "|" + str(
                        int(visited_times)) if visited_times != 0 else "0"

        # 输出。 Print.
        for i in range(BOARD.board_size + 1):
            for j in range(BOARD.board_size + 1):
                print("{:<15}".format(print_array[i][j]), end="")
            print("")
        print("----------------------------")

    def run(self, start_board: Board, times):
        """
        蒙特卡洛树，开始搜索...
        Monte Carlo Tree, start searching...
        :param start_board:
        :param times: 运行次数。run times.
        :return: 最佳的执行动作。 the best action.
        """
        time = []
        for i in range(times):
            c1 = datetime.datetime.now()
            board = copy.copy(start_board)
            c2 = datetime.datetime.now()
            if i % 20 == 0:
                print("\rrunning: {} / {}".format(i, times), end="")
            node, board = self.traverse(self.root, board)
            node_player = board.current_player
            c3 = datetime.datetime.now()

            winner = self.rollout(board)
            c4 = datetime.datetime.now()

            value = 0
            if winner == node_player:
                value = 1
            elif winner == -node_player:
                value = -1

            node.backpropagate(-value)
            c5 = datetime.datetime.now()

            time.append(
                ((c2 - c1).microseconds, (c3 - c2).microseconds, (c4 - c3).microseconds, (c5 - c4).microseconds))
            pass
        print("")

    def traverse(self, node: TreeNode, board: Board):
        """
        扩展子节点。
        Expand node.
        :param node: 当前节点。 Current node.
        :param board:
        :return: <TreeNode> 扩展出的节点。 Expanded nodes.
        """
        while True:
            is_over, _ = board.result()
            if is_over:
                break
            if len(node.children) != 0:
                action, node = node.choose_best_child(c=5)
                board.step(action)
            else:
                actions = board.available_actions
                probs = np.ones(len(actions)) / len(actions)

                # 扩展所有子节点。 Expand all child node.
                for action, prob in zip(actions, probs):
                    _ = node.expand(action, prob)
                break
        return node, board

    def rollout(self, board: Board):
        """
        模拟。
        Simulation.
        :param node: 当前节点。 Current node.
        :param board:
        :return: winner<int> 获胜者。 winner.
        """
        time = []
        while True:
            is_over, winner = board.result()
            if is_over:
                break
            c1 = datetime.datetime.now()
            self.rollout_policy(board)
            c2 = datetime.datetime.now()
            time.append((c2-c1).microseconds)
            pass
        return winner

    def rollout_policy(self, board: Board):
        """
        决策函数，选择子节点的概率决策。
        Policy function, a probabilistic decision to select child nodes.
        :param node: 当前节点。 Current node.
        :param board:
        :return: <TreeNode> 决策出的节点。 The decision node.
        """

        c1 = datetime.datetime.now()
        # 所有执行动作的概率相同。 All actions have the same probability.
        actions = list(board.available_actions)
        probs = np.ones(len(actions)) / len(actions)

        c2 = datetime.datetime.now()
        # 获得动作和概率。 Get action and probability.
        action_index = np.random.choice(range(len(actions)))
        action = actions[action_index]
        prob = probs[action_index]

        c3 = datetime.datetime.now()
        # 执行。 Action.
        board.step(action)

        c4 = datetime.datetime.now()
        time = ((c2 - c1).microseconds, (c3 - c2).microseconds, (c4 - c3).microseconds)

    def backpropagate(self, node: TreeNode, value):
        """
        反向传输，将结果返回父节点。
        Backpropagate, passing the result to the parent node.
        :param node: 当前节点。 Current node.
        :param value: 玩家获胜或失败的回报。 Players win or lose values.
        """

        node.backpropagate(value)
