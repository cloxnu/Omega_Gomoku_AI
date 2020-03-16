import numpy as np
import random
import collections

from console_select import select_network

import Game.Board as BOARD
from Game.Game import start_until_game_over
from AI.Network.PolicyValueNet_from_junxiaosong import PolicyValueNet_from_junxiaosong, data_augmentation, data_augmentation_new
from Player.AI_MCTS import AI_MCTS
from Player.AI_MCTS_Net import AI_MCTS_Net


def train():
    network = select_network(is_training=True)
    if isinstance(network, PolicyValueNet_from_junxiaosong):
        train_with_net_junxiaosong(network)


def train_with_net_junxiaosong(network: PolicyValueNet_from_junxiaosong):
    """
    [junxiaosong](https://github.com/junxiaosong/AlphaZero_Gomoku)
    使用 @junxiaosong 的神经网络训练。
    Training with net by @junxiaosong.
    :param network: 选择的网络（带有模型）。 Selected network (with model).
    """
    batch_size = 512
    temp = 1
    learning_rate = 2e-3  # 学习率。 Learning rate.
    lr_multiplier = 1.0  # 学习率因子。 Learning rate factor.
    num_train_steps = 5
    kl = 0  # KL 散度。 KL divergence.
    kl_targ = 0.02

    # 每对局 check_point 次，保存模型并评估网络。 Check_point times per game, save model and evaluate network.
    check_point = 50

    all_play_data = collections.deque(maxlen=10000)
    all_play_data_count = 0
    player = AI_MCTS_Net(policy_value_function=network.predict,
                         is_training=True,
                         search_times=400,
                         is_output_analysis=False,
                         greedy_value=5)

    try:
        i = 1
        while True:
            # 自我对局。 Self play.
            print("自我对局中。。。 Self playing...")
            board_inputs, all_action_probs, values = player.self_play(temp=temp)

            print("进行的局数 Round: {}, 步数 Step: {}, ".format(i, len(values)), end="")

            # 数据扩充。 Data augmentation.
            play_data = \
                data_augmentation_new(x_label=board_inputs, y_label=(all_action_probs, values))

            # play_data = list(zip(board_inputs, all_action_probs, values))
            all_play_data.extend(play_data)
            all_play_data_count += len(play_data)

            print("棋盘总收集数据 Total board data collection: {}".format(all_play_data_count))

            # 收集数据数量达到 batch_size。 The amount of collected data reaches batch_size.
            if len(all_play_data) > batch_size:

                print("神经网络训练中。。。 Neural network training...")

                # 随机选出训练样本。 Randomly select training samples.
                will_train_play_data = random.sample(all_play_data, batch_size)

                # 取得要训练的标签。 Get labels to train.
                board_inputs, all_action_probs, values = [], [], []
                for board_input, all_action_prob, value in will_train_play_data:
                    board_inputs.append(board_input)
                    all_action_probs.append(all_action_prob)
                    values.append(value)

                # 训练前的预测值。 Predicted value before training.
                old_probs, old_value = network.model.predict_on_batch(np.array(board_inputs))

                # 获得损失。 Get loss.
                loss = network.evaluate(x_label=board_inputs, y_label=(all_action_probs, values))
                loss = loss[0]

                # 获得熵。 Get entropy.
                entropy = network.get_entropy(x_label=board_inputs)

                for train_step in range(num_train_steps):

                    # 更新网络。 Update the network.
                    network.train(x_label=board_inputs, y_label=(all_action_probs, values),
                                  learning_rate=learning_rate * lr_multiplier)

                    # 训练后的预测值。 Predicted value after training.
                    new_probs, new_value = network.model.predict_on_batch(np.array(board_inputs))

                    # 计算 KL 散度。 Calculate KL divergence.
                    kl = np.mean(np.sum(old_probs * (np.log(old_probs + 1e-10) - np.log(new_probs + 1e-10)), axis=1))
                    if kl > kl_targ * 4:  # KL 散度严重偏离。 KL divergence severely deviates.
                        break

                # 根据 KL 散度调整学习率。 Adjust learning rate based on KL divergence.
                if kl > kl_targ * 2 and lr_multiplier > 0.1:
                    lr_multiplier /= 1.5
                elif kl < kl_targ / 2 and lr_multiplier < 10:
                    lr_multiplier *= 1.5

                # explained_var_old = (1 - np.var(np.array(values) - old_value.flatten()) / np.var(np.array(values)))
                # explained_var_new = (1 - np.var(np.array(values) - new_value.flatten()) / np.var(np.array(values)))

                print("[ KL 散度 KL divergence: {:.5f}, 学习率因子 lr_multiplier: {:.3f}, "
                      "损失 loss: {}, 熵 entropy: {} ]".format(kl, lr_multiplier, loss, entropy))

            # 保存模型和评估网络。 Save models and evaluate networks.
            if i % check_point == 0:
                print("神经网络评估中。。。 Neural network evaluating...")
                pure_mcts = AI_MCTS(name="evaluate", is_output_analysis=False, greedy_value=5, search_times=1000)
                training_mcts = AI_MCTS_Net(name="training", policy_value_function=network.predict,
                                            search_times=400, is_output_analysis=False, greedy_value=5)
                win_times, lose_times, draw_times = 0, 0, 0
                for j in range(10):
                    if j % 2 == 0:
                        winner = start_until_game_over(training_mcts, pure_mcts)
                        if winner == BOARD.o:
                            win_times += 1
                        elif winner == BOARD.x:
                            lose_times += 1
                        else:
                            draw_times += 1
                    else:
                        winner = start_until_game_over(pure_mcts, training_mcts)
                        if winner == BOARD.x:
                            win_times += 1
                        elif winner == BOARD.o:
                            lose_times += 1
                        else:
                            draw_times += 1
                    print("对局 {0} 次，获胜 {1} 次，失败 {2} 次，平 {3} 次。 {0} games, {1} wins, {2} loses, {3} draws".
                          format(j + 1, win_times, lose_times, draw_times))
                print("保存模型中。。。 Model saving...")
                network.model.save(network.model_file)
                print("模型已保存至 The model saved to: \'{}\'".format(network.model_file))
            i += 1
    except KeyboardInterrupt:
        print("退出训练。 Exit training.")
        print("保存模型中。。。 Model saving...")
        network.model.save(network.model_file)
        print("模型已保存至 The model saved to: \'{}\'".format(network.model_file))


if __name__ == '__main__':
    train()
