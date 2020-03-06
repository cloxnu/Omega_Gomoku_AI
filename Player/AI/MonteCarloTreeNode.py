import numpy as np
import random

from Game.Game import Game
import copy


class TreeNode(object):

    def __init__(self, board: Game, prior_prob, parent=None):
        self.board = copy.deepcopy(board)
        self.parent = parent
        self.children = {}  # key=action, value=TreeNode
        self.will_expand_action = copy.deepcopy(board.available_actions)  # 将要扩展的执行动作。 Action to be extended.
        self.reward = 0  # 该节点的奖励。 Total simulation reward of the node.
        self.visited_times = 0  # 该节点访问的次数。 Total number of visits of the node.
        self.prior_prob = prior_prob  # 父节点选到此节点的概率。 prior probability of the move.

    def is_full_expand(self):
        """
        节点是否完全扩展。
        Is node fully expanded?
        :return: <Bool> 是否完全扩展。 whether Full expand or not.
        """
        return len(self.will_expand_action) == 0

    def is_root(self):
        """
        节点是否根节点。
        Whether the node is the root node.
        :return: <Bool>
        """
        return self.parent is None

    def expand(self, prior_prob):
        """
        扩展节点。
        Expand node.
        :return: <TreeNode> 扩展出的节点
        """
        # 扩展一个执行动作。 Expand an action.
        action = self.will_expand_action.pop()

        # 执行动作。 Execute the action.
        next_board = copy.deepcopy(self.board)
        next_board.step(action)

        # 添加子节点。 Add child node.
        child_node = TreeNode(next_board, prior_prob=prior_prob, parent=self)
        self.children[action] = child_node

        return child_node

    def UCT_function(self, c=1.4):
        if self.visited_times == 0:
            return 0
        # return -self.reward / self.visited_times + c * np.sqrt(np.log(self.parent.visited_times)/(self.visited_times))
        return -self.reward / self.visited_times + c * self.prior_prob * np.sqrt(self.parent.visited_times/(1 + self.visited_times))

    def choose_best_child(self, c=1.4):
        """
        依据 UCT 函数，选择一个最佳的子节点。
        According to the UCT function, select an optimal child node.
        :return: <(action(x_axis, y_axis), TreeNode)> 最佳的子节点。 An optimal child node.
        """
        return max(self.children.items(), key=lambda child_node: child_node[1].UCT_function(c))

    def backpropagate(self, winner):
        """
        反向传输，将结果返回父节点。
        Backpropagate, passing the result to the parent node.
        :param winner: 获胜的玩家。 Winning player.
        """
        self.visited_times += 1

        if winner == self.board.current_player:
            self.reward += 1
        elif winner == -self.board.current_player:
            self.reward -= 1

        if not self.is_root():
            self.parent.backpropagate(winner)
