from abc import ABCMeta, abstractmethod


class Network(metaclass=ABCMeta):

    @abstractmethod
    def create_net(self):
        """
        创建网络。
        Create the network.
        """

    @abstractmethod
    def train(self, x_label, y_label, learning_rate):
        """
        训练网络。
        Train the network.
        :param x_label: 输入神经网络的标签。 Input neural network labels.
        :param y_label: 正确的输出标签。 Correct output label.
        :param learning_rate: 学习率。 Learning rate.
        """