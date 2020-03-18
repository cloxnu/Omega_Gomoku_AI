import numpy as np
import copy

from Game.Board import Board
import Game.Board as BOARD
from AI.MonteCarloTreeSearch import MonteCarloTreeSearch
from AI.MonteCarloTreeNode import TreeNode
from Player.Player import Player

from AI.Network.PolicyValueNet_from_junxiaosong import board_to_xlabel


class AI_MCTS_Net(MonteCarloTreeSearch, Player):

    def __init__(self, policy_value_function, name="AI_MCTS_Net",
                 is_training=False, search_times=2000, is_output_analysis=True, greedy_value=5.0):
        """
        AI_MCTS_Net 是一个实现 MonteCarloTreeSearch 的 Player，并通过 policy_value_function 进行落子概率决策。
        AI_MCTS_Net is a Player that implements MonteCarloTreeSearch,
         and makes policy of probability of action through the policy_value_function.
        :param policy_value_function: 策略价值函数。 Policy value function.
        :param name: 此 AI 的名字。 The name of this AI.
        :param is_training: 是否是训练模式。 Whether it is training mode.
        :param search_times: 蒙特卡洛树搜索次数。 Monte Carlo Tree Search times.
        :param is_output_analysis: 是否输出 AI 分析。 Whether to output AI analysis.
        """
        super().__init__()
        self.name = name

        self.policy_value_function = policy_value_function
        self.is_training = is_training
        self.search_times = search_times  # 树搜索次数。 The search times of tree.
        self.is_output_analysis = is_output_analysis  # 是否输出 AI 分析。 Whether to output AI analysis.
        self.greedy_value = greedy_value

    def reset(self):
        self.root = TreeNode(prior_prob=1.0)

    def take_action(self, board: Board, is_output_action=True):
        """
        下一步 AI 玩家执行动作。
        The AI player take action next step.
        :param board: 当前棋盘。 Current board.
        :param is_output_action: 是否输出执行动作。 Whether to output execution actions.
        """
        if is_output_action:
            print("该 {0} 落子了，它是 AI 选手。 It's turn to {0}, AI player.".format(self.name))
            print("思考中。。。 Thinking...")

        self.reset()
        self.run(board, self.search_times)

        # 取得落子动作和概率。 Get actions and probabilities.
        actions, probs = self.get_action_probs()

        # action -> flatten_action
        flatten_actions = []
        for one_action in actions:
            flatten_actions.append(one_action[0] * BOARD.board_size + one_action[1])

        if self.is_training:
            # 训练时，增加 dirichlet 噪声。 add Dirichlet Noise for exploration in training.
            flatten_action = np.random.choice(flatten_actions,
                                              p=0.75 * probs + 0.25 * np.random.dirichlet(0.3 * np.ones(len(probs))))
        else:
            flatten_action = np.random.choice(flatten_actions, p=probs)

        # flatten_action -> action
        action = (flatten_action // BOARD.board_size, flatten_action % BOARD.board_size)

        board.step(action)

        if self.is_output_analysis:
            action_probs = np.zeros((BOARD.board_size, BOARD.board_size), dtype=np.float64)
            # probs -> action_probs
            for one_action, one_prob in zip(actions, probs):
                action_probs[one_action[0], one_action[1]] = one_prob

            self.output_analysis(action_probs)

        if is_output_action:
            print("AI 选手 {0} 落子于 ({1}, {2})\nAI player {0} moves ({1}, {2})".format(self.name, action[0], action[1]))

    def self_play(self, temp=1e-3):
        """
        自我对局，游戏结束后返回所有局面，所有局面的落子概率，及胜利或失败的回报。
        Self-play, return to all boards after the game,
        the probability of losing all positions,
        and reward of victory or lose.
        :param temp: 温度参数（探索程度）。 Temperature parameter (Degree of exploration).
        :return: [(boards, all_action_probs, values)]
        """
        board_inputs, all_action_probs, current_player = [], [], []
        board = Board()

        while True:
            self.reset()
            self.run(board, self.search_times)

            # 取得落子动作和概率。 Get actions and probabilities.
            actions, probs = self.get_action_probs(temp=temp)
            action_probs = np.zeros((BOARD.board_size, BOARD.board_size), dtype=np.float64)

            # actions, probs -> action_probs
            for action, prob in zip(actions, probs):
                action_probs[action[0], action[1]] = prob

            # 收集自我对局数据。 Collect self play data.
            board_inputs.append(board_to_xlabel(board))
            all_action_probs.append(action_probs)
            current_player.append(board.current_player)

            # action -> flatten_action
            flatten_actions = []
            for one_action in actions:
                flatten_actions.append(one_action[0] * BOARD.board_size + one_action[1])

            # 训练时，增加 dirichlet 噪声。 Add Dirichlet Noise for exploration in training.
            flatten_action = np.random.choice(flatten_actions,
                                              p=0.75 * probs + 0.25 * np.random.dirichlet(0.3 * np.ones(len(probs))))

            # flatten_action -> action
            action = (flatten_action // BOARD.board_size, flatten_action % BOARD.board_size)

            board.step(action)

            is_over, winner = board.result()
            if is_over:
                values = np.zeros(len(current_player), dtype=np.float64)
                if winner != 0:
                    values[np.array(current_player) == winner] = 1
                    values[np.array(current_player) != winner] = -1
                return board_inputs, all_action_probs, values

    def get_action_probs(self, temp=1e-3):
        """
        获得所有的落子动作及概率。
        Get all the actions and probabilities.
        :param temp: 温度参数（探索程度）。 Temperature parameter (Degree of exploration).
        :return: (action<tuple>, probabilities[])
        """
        action_visits = [(action, node.visited_times) for action, node in self.root.children.items()]
        actions, visits = zip(*action_visits)

        def softmax(x):
            y = np.exp(x - np.max(x))
            y /= np.sum(y)
            return y

        probs = softmax(1.0 / temp * np.log(np.array(visits) + 1e-10))
        return actions, probs

    def output_analysis(self, action_probs):
        """
        输出棋子胜率分析。
        Analysis of winning ratio of output pieces.
        :param action_probs: 落子动作和概率。 Moving actions and probabilities.
        """
        print("----------------------------\n"
              "AI 分析： AI analysis:\n"
              "格式：[决策概率(%) | 计算次数]  Format: [Decision probability(%) | #calculations]")
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
                    print_array[i + 1][j + 1] = "{0:.1f}%".format(action_probs[i][j] * 100) + "|" + str(
                        int(visited_times))

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
        :param start_board: 开始的棋盘。 The start state of the board.
        :param times: 运行次数。run times.
        """
        for i in range(times):
            board = copy.deepcopy(start_board)
            if i % 20 == 0:
                print("\rrunning: {} / {}".format(i, times), end="")

            # 扩展子节点。 Expand node.
            node, value = self.traverse(self.root, board)

            # 反向传输。 Backpropagate.
            node.backpropagate(-value)
        print("\r                      ", end="\r")

    def traverse(self, node: TreeNode, board: Board):
        """
        扩展子节点。
        Expand node.
        :param node: 当前节点。 Current node.
        :param board: 棋盘。 The board.
        :return: (<TreeNode>, value<int>) 扩展出的节点和需要反向传输的 value。
        Expanded nodes, and the value to be backpropagated.
        """
        while True:
            if len(node.children) == 0:
                break
            action, node = node.choose_best_child(c=self.greedy_value)
            board.step(action)

        # 是否结束。 game over?
        is_over, winner = board.result()
        if is_over:
            if winner == board.current_player:
                value = 1
            elif winner == -board.current_player:
                value = -1
            else:
                value = 0
            return node, value

        # 使用策略价值函数决策当前动作概率及评估价值。
        # Use the strategy value function to decide the current action probability and evaluate the value.
        action_probs, value = self.policy_value_function(board)

        for action, probability in action_probs:
            _ = node.expand(action, probability)

        return node, value
