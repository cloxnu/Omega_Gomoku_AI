import numpy as np
import random
import collections
import datetime
import os

from console_select import select_yes_or_no

import Game.Board as BOARD
from Game.Game import start_until_game_over
from AI.Network.PolicyValueNet_from_junxiaosong import PolicyValueNet_from_junxiaosong, data_augmentation, data_augmentation_new
from Player.AI_MCTS import AI_MCTS
from Player.AI_MCTS_Net import AI_MCTS_Net


def train_with_net_junxiaosong(network: PolicyValueNet_from_junxiaosong, allow_user_input=True, round_times=0):
    """
    [junxiaosong](https://github.com/junxiaosong/AlphaZero_Gomoku)
    使用 @junxiaosong 的神经网络训练。
    Training with net by @junxiaosong.
    :param network: 选择的网络（带有模型）。 Selected network (with model).
    :param allow_user_input: 允许用户输入。 Allow the input from console.
    :param round_times: 自我对局次数。(0 表示无限)。 self-play times. (0 means infinite).
    """
    batch_size = 512
    temp = 1
    learning_rate = 2e-3  # 学习率。 Learning rate.
    lr_multiplier = 1.0  # 学习率因子。 Learning rate factor.
    num_train_steps = 5
    kl = 0  # KL 散度。 KL divergence.
    kl_targ = 0.02

    # 神经网络评估对战纯蒙特卡洛树 AI 的搜索次数。
    # The search times of the pure Monte Carlo tree AI.
    pure_mcts_search_times = 1000

    # 网络评估胜率。 Network evaluation win rate.
    win_ratio = 0

    # 每对局 check_point 次，保存模型并评估网络。 Check_point times per game, save model and evaluate network.
    check_point = 50

    all_play_data = collections.deque(maxlen=10000)
    all_play_data_count = 0
    player = AI_MCTS_Net(policy_value_function=network.predict,
                         is_training=True,
                         search_times=400,
                         greedy_value=5.0,
                         is_output_analysis=False,
                         is_output_running=False)

    is_output_log = select_yes_or_no("请选择是否输出此次训练日志文件。[Y/y] 输出，[N/n] 不输出。\n"
                                     "Please choose whether to output the training log file. "
                                     "[Y/y] output，[N/n] not output.\n"
                                     "(y): ", default=True) if allow_user_input else True

    log_file = open(network.model_dir + "out.log", mode="a", encoding="utf-8")
    if is_output_log:
        log_file.write("\n\n-------------------------------------------")
        print("训练日志文件将会保存至 The training log file will be saved to: {}".format(network.model_dir + "out.log"))

    try:
        i = 1
        print("\n训练开始时间 Training start time: {0},\n"
              "训练模型路径 Training model path: {1}\n".
              format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), network.model_dir))
        if is_output_log:
            log_file.write("\n训练开始时间 Training start time: {0},\n"
                           "训练模型路径 Training model path: {1}\n\n".
                           format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), network.model_dir))

        print("训练即将开始，按 <Ctrl-C> 结束训练。\n"
              "The training is about to begin. Press <Ctrl-C> to end the training.\n"
              "-----------------------------------------------")
        while True:
            # 自我对局。 Self play.
            print("自我对局中。。。 Self playing...")
            board_inputs, all_action_probs, values = player.self_play(temp=temp)

            print("进行的局数 Round: {}, 步数 Step: {}, ".format(i, len(values)), end="")
            if is_output_log:
                log_file.write("进行的局数 Round: {}, 步数 Step: {}, ".format(i, len(values)))

            # 数据扩充。 Data augmentation.
            play_data = \
                data_augmentation_new(x_label=board_inputs, y_label=(all_action_probs, values))

            # play_data = list(zip(board_inputs, new_action_probs, values))
            all_play_data.extend(play_data)
            all_play_data_count += len(play_data)

            print("棋盘总收集数据 Total board data collection: {}".format(all_play_data_count))
            if is_output_log:
                log_file.write("棋盘总收集数据 Total board data collection: {}\n".format(all_play_data_count))

            # 收集数据数量达到 batch_size。 The amount of collected data reaches batch_size.
            if len(all_play_data) > batch_size:

                print("神经网络训练中。。。 Neural network training...")
                if is_output_log:
                    log_file.write("神经网络训练中。。。 Neural network training...\n")

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

                print("[ KL 散度 KL divergence: {:.5f}, 学习率因子 lr_multiplier: {:.3f}, "
                      "损失 loss: {:.3f}, 熵 entropy: {:.3f} ]".format(kl, lr_multiplier, loss, entropy))
                if is_output_log:
                    log_file.write("[ KL 散度 KL divergence: {:.5f}, 学习率因子 lr_multiplier: {:.3f}, "
                                   "损失 loss: {:.3f}, 熵 entropy: {:.3f} ]\n".format(kl, lr_multiplier, loss, entropy))

            # 保存模型和评估网络。 Save models and evaluate networks.
            if i % check_point == 0:
                print("神经网络评估中。。。 Neural network evaluating...")
                if is_output_log:
                    log_file.write("神经网络评估中。。。 Neural network evaluating...\n")

                pure_mcts = AI_MCTS(name="evaluate", greedy_value=5.0, search_times=pure_mcts_search_times,
                                    is_output_analysis=False, is_output_running=False)
                training_mcts = AI_MCTS_Net(name="training", policy_value_function=network.predict,
                                            search_times=400, greedy_value=5.0,
                                            is_output_analysis=False, is_output_running=False)
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
                    if is_output_log:
                        log_file.write("对局 {0} 次，获胜 {1} 次，失败 {2} 次，平 {3} 次。 "
                                       "{0} games, {1} wins, {2} loses, {3} draws\n".
                                       format(j + 1, win_times, lose_times, draw_times))

                # 计算胜率。 Calculate the win rate.
                current_win_ratio = win_times / 10.0
                if current_win_ratio > win_ratio:
                    win_ratio = current_win_ratio
                    print("胜率新纪录！New record of win rate!")
                    print("保存最佳模型记录中。。。 Best model record saving...")
                    if is_output_log:
                        log_file.write("胜率新纪录！New record of win rate!\n")

                    # 保存最佳模型。 Save old model.
                    # 最佳模型记录格式 Best model record format: "best_1000_6.h5"
                    best_model_path = network.model_dir + "best_" + "{}_{}.h5".format(pure_mcts_search_times, win_times)
                    network.model.save(best_model_path)
                    print("最佳模型记录已保存至 The best model record saved to: \'{}\'".format(best_model_path))

                    # 删除以前的最佳模型。 Remove old model.
                    for old_win_times in range(win_times):
                        old_model = network.model_dir + "best_{}_{}.h5".format(pure_mcts_search_times, old_win_times)
                        if os.path.exists(old_model):
                            os.remove(old_model)

                    if is_output_log:
                        log_file.write("最佳模型记录已保存至 The best model record saved to: \'{}\'\n".format(best_model_path))

                if current_win_ratio == 1.0 and pure_mcts_search_times < 5000:
                    pure_mcts_search_times += 1000
                    win_ratio = 0
                    print("恭喜全部获胜，评估难度增加，纯 MCTS AI 选手搜索次数上升为 {}".format(pure_mcts_search_times))

                print("保存最新模型记录中。。。 Latest model record saving...")
                network.model.save(network.model_dir + "latest.h5")
                print("最新模型记录已保存至 The latest model record saved to: \'{}\'".format(network.model_dir + "latest.h5"))
                if is_output_log:
                    log_file.write("最新模型记录已保存至 The latest model record saved to: \'{}\'\n".format(network.model_dir + "latest.h5"))
            if i == round_times:
                raise KeyboardInterrupt
            i += 1
    except KeyboardInterrupt:
        print("退出训练。 Exit training.")
        print("保存最新模型记录中。。。 Latest model record saving...")
        network.model.save(network.model_dir + "latest.h5")
        print("最新模型记录已保存至 The latest model record saved to: \'{}\'".format(network.model_dir + "latest.h5"))
        if is_output_log:
            log_file.write("退出训练。 Exit training.\n"
                           "最新模型记录已保存至 The latest model record saved to: \'{}\'".format(network.model_dir + "latest.h5"))
        log_file.close()
