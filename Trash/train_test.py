import numpy as np

import Game.Board as BOARD
from Game.Game import start_until_game_over
from AI.Network.PolicyValueNet_from_junxiaosong import PolicyValueNet_from_junxiaosong
from Player.AI_MCTS import AI_MCTS
from Player.AI_MCTS_Net import AI_MCTS_Net


def train_test(network: PolicyValueNet_from_junxiaosong, train_epochs=0):
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

    f = open("self_play_data.txt", "r")
    try:
        # will_train_play_data = []
        # print("文件读入中。。。")

        # for j in range(100):

        print("训练即将开始，按 <Ctrl-C> 结束训练。\n"
              "The training is about to begin. Press <Ctrl-C> to end the training.\n"
              "-----------------------------------------------")
        for i in range(train_epochs):
            # 收集数据数量达到 batch_size。 The amount of collected data reaches batch_size.

            print("文件读入中。。。")

            state_str = f.readline()
            probs_str = f.readline()
            winner_str = f.readline()

            state_strs = state_str.split(",")
            state_strs = state_strs[:-1]
            state_inputs = np.array([np.float64(s) for s in state_strs])
            state_inputs = state_inputs.reshape((512, 4, 6, 6))

            probs_strs = probs_str.split(",")
            probs_strs = probs_strs[:-1]
            probs = np.array([np.float64(p) for p in probs_strs])
            probs = probs.reshape((512, 36))

            winner_strs = winner_str.split(",")
            winner_strs = winner_strs[:-1]
            winners = np.array([np.float64(w) for w in winner_strs])

            play_data = state_inputs, probs, winners

            print("神经网络训练中。。。 Neural network training...")

            # 取得要训练的标签。 Get labels to train.
            board_inputs, all_action_probs, values = play_data
            # for board_input, all_action_prob, value in play_data:
            #     board_inputs.append(board_input)
            #     all_action_probs.append(all_action_prob)
            #     values.append(value)

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
                  "损失 loss: {:.3f}, 熵 entropy: {:.3f} ]".format(kl, lr_multiplier, loss, entropy))

            # 保存模型和评估网络。 Save models and evaluate networks.
            if (i+1) % check_point == 0:
                print("神经网络评估中。。。 Neural network evaluating...")

                pure_mcts = AI_MCTS(name="evaluate", is_output_analysis=False, greedy_value=5.0, search_times=1000, is_output_running=False)
                training_mcts = AI_MCTS_Net(name="training", policy_value_function=network.predict,
                                            search_times=400, is_output_analysis=False, greedy_value=5.0, is_output_running=False)
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

                # 计算胜率。 Calculate the win rate.
                current_win_ratio = win_times / 10.0
                if current_win_ratio > win_ratio:
                    win_ratio = current_win_ratio
                    print("胜率新纪录！New record of win rate!")
                    print("保存最佳模型记录中。。。 Best model record saving...")
                    # 最佳模型记录格式 Best model record format: "best_1000_6.h5"
                    best_model_path = network.model_dir + "best_" + "{}_{}.h5".format(pure_mcts_search_times, win_times)
                    network.model.save(best_model_path)
                    print("最佳模型记录已保存至 The best model record saved to: \'{}\'".format(best_model_path))

                print("保存最新模型记录中。。。 Latest model record saving...")
                network.model.save(network.model_dir + "latest.h5")
                print("最新模型记录已保存至 The latest model record saved to: \'{}\'".format(network.model_dir + "latest.h5"))

    except KeyboardInterrupt:
        print("退出训练。 Exit training.")
        print("保存最新模型记录中。。。 Latest model record saving...")
        network.model.save(network.model_dir + "latest.h5")
        print("最新模型记录已保存至 The latest model record saved to: \'{}\'".format(network.model_dir + "latest.h5"))
        f.close()


if __name__ == '__main__':
    network = PolicyValueNet_from_junxiaosong(is_training=True, specified_model_name="train_test")
    train_test(network, train_epochs=100)
