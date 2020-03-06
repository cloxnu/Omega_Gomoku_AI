from abc import ABCMeta, abstractmethod

from Game.Game import Game
from Player.AI.MonteCarloTreeNode import TreeNode


class MonteCarloTreeSearch(metaclass=ABCMeta):

    def __init__(self):
        self.root = None

    @abstractmethod
    def run(self, times):
        """
        蒙特卡洛树，开始搜索...
        Monte Carlo Tree, start searching...
        :param times: 运行次数。run times.
        :return: 最佳的执行动作。 the best action.
        """

    @abstractmethod
    def traverse(self, node: TreeNode):
        """
        扩展子节点。
        Expand node.
        :param node: 当前节点。 Current node.
        :return: <TreeNode> 扩展出的节点。 Expanded nodes.
        """

    @abstractmethod
    def rollout(self, node: TreeNode):
        """
        模拟。
        Simulation.
        :param node: 当前节点。 Current node.
        :return: winner<int> 获胜者。 winner.
        """

    @abstractmethod
    def rollout_policy(self, node: TreeNode):
        """
        决策函数，选择子节点的概率决策。
        Policy function, a probabilistic decision to select child nodes.
        :param node: 当前节点。 Current node.
        :return: <TreeNode> 决策出的节点。 The decision node.
        """

    @abstractmethod
    def backpropagate(self, node: TreeNode, winner):
        """
        反向传输，将结果返回父节点。
        Backpropagate, passing the result to the parent node.
        :param node: 当前节点。 Current node.
        :param winner: 获胜的玩家。 Winning player.
        """
    #
    # @abstractmethod
    # def best_child(self):
    #     """
    #     根据子节点的价值，最终选择子节点。
    #     According to the value of the child node, the child node is finally selected.
    #     :return: <TreeNode> 最佳的子节点。 The best child node.
    #     """
