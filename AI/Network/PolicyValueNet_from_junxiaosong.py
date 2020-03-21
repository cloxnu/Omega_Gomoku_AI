from AI.Network.Network import Network
import console_select

import numpy as np
import keras
from keras import Input
from keras import layers
from keras import optimizers
from keras import regularizers
import keras.backend as K

import Game.Board as BOARD
from Function import get_data_augmentation


def board_to_xlabel(board):
    """
    将 Board 转化为作为神经网络输入的 x_label。
    Convert Board to x_label as input to the neural network.
    :param board: 棋盘。 The board.
    :return: x_label 需要输入到神经网络的 x_label。 Input of the neural network.
    """

    # board -> board_input (x_label)
    x_label = np.zeros((4, BOARD.board_size, BOARD.board_size))

    # 1: 我方棋子位置。 Position of our pieces.
    x_label[0][board.board == board.current_player] = 1

    # 2: 对方棋子位置。 Position of opponent pieces.
    x_label[1][board.board == -board.current_player] = 1

    # 3: 上次落子。 Last action.
    if board.last_action is not None:
        x_label[2][board.last_action[0], board.last_action[1]] = 1

    # 4: 当前 Player 是否先手。 Whether the current player is the first player.
    if board.current_player == BOARD.start_player:
        x_label[3][:, :] = 1

    # flip
    flipped_x_label = []
    for one_board in x_label:
        flipped_x_label.append(np.flipud(one_board))
    x_label = np.array(flipped_x_label)

    return x_label


def data_augmentation_new(x_label, y_label):
    """
    数据扩充。
    Data augmentation.
    :param x_label: 神经网络的输入 x_label。 Input of the neural network.
    :param y_label: 神经网络的输出 x_label。 Output of the neural network.
    :return: 数据扩充后的 data.  Data after data augmentation.
    """
    all_action_probs, values = y_label
    extend_data = []
    for board_input, action_probs, value in zip(x_label, all_action_probs, values):
        for i in [0, 1, 2, 3]:
            # rotate counterclockwise
            new_board_input = np.array([np.rot90(one_board_input, i) for one_board_input in board_input])
            new_action_probs = np.rot90(np.flipud(action_probs.reshape(BOARD.board_size, BOARD.board_size)), i)
            extend_data.append((new_board_input,
                                np.flipud(new_action_probs).flatten(),
                                value))
            # flip horizontally
            new_board_input = np.array([np.fliplr(one_board_input) for one_board_input in new_board_input])
            new_action_probs = np.fliplr(new_action_probs)
            extend_data.append((new_board_input,
                                np.flipud(new_action_probs).flatten(),
                                value))
    return extend_data


def data_augmentation(x_label, y_label):
    """
    数据扩充。
    Data augmentation.
    :param x_label: 神经网络的输入 x_label。 Input of the neural network.
    :param y_label: 神经网络的输出 x_label。 Output of the neural network.
    :return: 数据扩充后的 x_label, y_label.  X_label, y_label after data augmentation.
    """
    all_action_probs, values = y_label

    extend_xlabel = []
    extend_ylabel_action_probs = []
    extend_ylabel_value = []

    for board_input in x_label:
        # 将 board_input 4 维数据拆开分别进行数据扩充。
        # The board_input 4-dimensional data is disassembled and expanded separately.
        augmentation_board = np.array([get_data_augmentation(one_board_input) for one_board_input in board_input])
        board_augmentation = np.array(list(zip(*augmentation_board)))
        extend_xlabel.extend(np.array([one_augmentation for one_augmentation in board_augmentation]))

    for action_probs in all_action_probs:
        extend_action_probs = get_data_augmentation(action_probs.reshape(BOARD.board_size, BOARD.board_size),
                                                    operation=lambda a: a.flatten())
        extend_ylabel_action_probs.extend(extend_action_probs)

    for value in values:
        extend_value = get_data_augmentation(np.array(value))
        extend_ylabel_value.extend(extend_value)

    return extend_xlabel, (extend_ylabel_action_probs, extend_ylabel_value)


class PolicyValueNet_from_junxiaosong(Network):
    """
    [junxiaosong](https://github.com/junxiaosong/AlphaZero_Gomoku)
    使用 @junxiaosong 的神经网络。
    Network by @junxiaosong.
    """

    def __init__(self, is_training=False):
        self.l2_const = 1e-4

        is_new_model, self.model_dir, self.model_record_path = \
            console_select.select_model("Model/PolicyValueNet_from_junxiaosong", is_training)

        if is_new_model:
            self.create_net()
        else:
            self.model = keras.models.load_model(self.model_record_path)

    def __str__(self):
        return "PolicyValueNet_from_junxiaosong"

    def create_net(self):
        """
        创建策略价值网络。
        Create policy value net.
        """

        net = input_net = Input((4, BOARD.board_size, BOARD.board_size))
        net = layers.Conv2D(filters=32, kernel_size=(3, 3), padding="same", data_format="channels_first",
                            activation="relu", kernel_regularizer=regularizers.l2(self.l2_const))(net)
        net = layers.Conv2D(filters=64, kernel_size=(3, 3), padding="same", data_format="channels_first",
                            activation="relu", kernel_regularizer=regularizers.l2(self.l2_const))(net)
        net = layers.Conv2D(filters=128, kernel_size=(3, 3), padding="same", data_format="channels_first",
                            activation="relu", kernel_regularizer=regularizers.l2(self.l2_const))(net)

        policy_net = layers.Conv2D(filters=4, kernel_size=(1, 1), data_format="channels_first",
                                   activation="relu", kernel_regularizer=regularizers.l2(self.l2_const))(net)
        policy_net = layers.Flatten()(policy_net)
        policy_net = layers.Dense(BOARD.board_size * BOARD.board_size, activation="softmax",
                                  kernel_regularizer=regularizers.l2(self.l2_const))(policy_net)

        value_net = layers.Conv2D(filters=2, kernel_size=(1, 1), data_format="channels_first",
                                  activation="relu", kernel_regularizer=regularizers.l2(self.l2_const))(net)
        value_net = layers.Flatten()(value_net)
        value_net = layers.Dense(64, kernel_regularizer=regularizers.l2(self.l2_const))(value_net)
        value_net = layers.Dense(1, activation="tanh", kernel_regularizer=regularizers.l2(self.l2_const))(value_net)

        self.model = keras.Model(input_net, [policy_net, value_net])
        self.model.compile(optimizer=optimizers.Adam(),
                           loss=['categorical_crossentropy', 'mean_squared_error'])

    def train(self, x_label, y_label, learning_rate):
        """
        训练网络模型。
        Train the model.
        :param x_label: 输入神经网络的标签。 Input neural network labels.
        :param y_label: 待监督训练的输出标签。 Output labels for training to be supervised.
        :param learning_rate: 学习率。 Learning rate.
        """

        board_input = np.array(x_label)

        probs, values = y_label
        probs_output = np.array(probs)
        values_output = np.array(values)

        K.set_value(self.model.optimizer.lr, learning_rate)
        self.model.fit(board_input, [probs_output, values_output],
                       batch_size=len(x_label), verbose=0)

    def predict(self, board):
        """
        对当前局面预测下一步的概率。
        Probability of predicting the next step for the current board.
        :param board: 当前局面。 Current board.
        :return: [(action, probability), value]
        """

        board_input = board_to_xlabel(board)
        board_input = board_input.reshape((-1, 4, BOARD.board_size, BOARD.board_size))

        probs, value = self.model.predict_on_batch(board_input)
        probs = probs.reshape((BOARD.board_size, BOARD.board_size))

        action_probs = []
        for available_action in board.available_actions:
            action_probs.append((available_action, probs[available_action[0], available_action[1]]))

        return action_probs, value[0][0]

    def evaluate(self, x_label, y_label):
        """
        评估网络。
        Evaluate the network.
        :param x_label: 神经网络的输入 x_label。 Input of the neural network.
        :param y_label: 神经网络的输出 x_label。 Output of the neural network.
        :return: 网络的评估值。 Evaluation of the network.
        """

        board_input = np.array(x_label)

        probs, values = y_label
        probs_output = np.array(probs)
        values_output = np.array(values)

        return self.model.evaluate(board_input, [probs_output, values_output], batch_size=len(board_input), verbose=0)

    def get_entropy(self, x_label):
        """
        取得熵。
        Get the entropy.
        :param x_label: 神经网络的输入 x_label。 Input of the neural network.
        :return: 熵。 The entropy.
        """
        board_input = np.array(x_label)
        probs, _ = self.model.predict_on_batch(board_input)
        return -np.mean(np.sum(probs * np.log(probs + 1e-10), axis=1))
