import pathlib

from configure import Configure
import AI.Network.PolicyValueNet_from_junxiaosong as PolicyValueNet_from_junxiaosong


def select(prompt, allowed_input):
    """
    要求用户从控制台选择条目。
    Ask the user to select an entry from the console.
    :param prompt: 提示语。 prompt.
    :param allowed_input: 允许输入的值，要求是 int 类型。 Allowed values, int type required.
    :return: <int> 选择的值。 Selected value.
    """
    choose_value = 1

    while True:
        input_str = input(prompt)
        try:
            input_int = int(input_str)
            if input_int in allowed_input:
                choose_value = input_int
            else:
                print("输入有误，请重新输入。\n"
                      "The input is incorrect. Please try again.\n")
                continue
        except:
            print("输入有误，请重新输入。\n"
                  "The input is incorrect. Please try again.\n")
            continue
        break
    return choose_value


def select_player(prompt, allowed_input):
    """
    选择玩家。
    Choose player.
    :param prompt: 提示语。 prompt.
    :return: (<int>, <str>) 选择的值和玩家的名字。 Selected values and player names.
    """

    choose_value = select(prompt, allowed_input)

    input_name = input("它的名字是。 It's name is.\n"
                       ": ")
    return choose_value, input_name


def set_AI_conf(search_times=2000, greedy_value=5.0):
    """
    设定 AI 玩家的配置。
    Set AI player configuration.
    :param search_times: AI 搜索次数的默认值。 Default value for AI searches.
    :param greedy_value: 贪婪值的默认值。 Default value for greedy value.
    :return: search_times, greedy_value
    """

    while True:
        input_str = input("AI 配置 1：请输入 AI 搜索次数 search times. (times >= 1)\n"
                          "AI Config 1: Please input the AI search times. (times >= 1)\n"
                          "AI search times ({}) = ".format(search_times))
        try:
            input_int = search_times if len(input_str) == 0 else int(input_str)
            if input_int < 1:
                print("times 应该大于等于 1，请重新输入。\n"
                      "times should be greater than or equal to 0. Please try again.\n")
                continue
            search_times = input_int
        except:
            print("输入有误，请重新输入。\n"
                  "The input is incorrect. Please try again.\n")
            continue
        break

    while True:
        input_str = input("AI 配置 2：请输入蒙特卡洛树搜索的贪婪值 greedy value. (c > 0)\n"
                          "AI Config 2: Please enter greedy value for Monte Carlo tree search. (c > 0)\n"
                          "c ({}) = ".format(greedy_value))
        try:
            input_float = greedy_value if len(input_str) == 0 else float(input_str)
            if input_float <= 0:
                print("c 应该大于 0，请重新输入。\n"
                      "c should be greater than 0. Please try again.\n")
                continue
            greedy_value = input_float
        except:
            print("输入有误，请重新输入。\n"
                  "The input is incorrect. Please try again.\n")
            continue
        break

    return search_times, greedy_value


def select_network(is_training=False):
    """
    选择想要使用的神经网络。
    Select the network you want to use.
    :param is_training: 是否训练。 Whether to train.
    :return: <Network> 网络。 network.
    """
    network_selected = select("请选择想要使用的神经网络。按 <Ctrl-C> 退出。\n"
                              "1: 由 [junxiaosong] 提供的神经网络\n"
                              "Please select the neural network you want to use. Press <Ctrl-C> to exit.\n"
                              "1: Neural network provided by [junxiaosong]\n"
                              ": ", allowed_input=[1])
    if network_selected == 1:
        return PolicyValueNet_from_junxiaosong.PolicyValueNet_from_junxiaosong(is_training)


def select_model(dir: str, is_training=False):
    """
    选择想要使用或训练的网络模型。
    Select the network model you want to use or train.
    :param dir: 网络模型目录。 Network model directory.
    :param is_training: 是否训练。 Whether to train.
    :return: (<bool>, <str>, <str>) 是否是新的网络模型，和网络模型路径，网络模型记录路径。
    Whether it is a new network model, and the network model path, and the network model record path.
    """
    conf = Configure()
    conf.get_conf()
    board_conf_str = "{0}_{1}".format(conf.conf_dict["board_size"], conf.conf_dict["n_in_a_row"])
    model_path = pathlib.Path(dir)
    model_path = model_path / board_conf_str
    model_path.mkdir(parents=True, exist_ok=True)
    all_model_path = sorted(item for item in model_path.glob('*/') if item.is_dir())
    all_model_name = [path.name for path in all_model_path]

    if is_training:
        print("请选择想要训练的网络模型。按 <Ctrl-C> 退出。\n"
              "Please select the network model you want to train. Press <Ctrl-C> to exit.")
        print("0: 创建新的网络模型。 Create a new network model.")
    else:
        print("请选择想要使用的网络模型。按 <Ctrl-C> 退出。\n"
              "Please select the network model you want to use. Press <Ctrl-C> to exit.")
    for i, one_model_name in enumerate(all_model_name):
        print("{0}: {1}".format(i + 1, one_model_name))

    model_selected = select(": ", allowed_input=range(0 if is_training else 1, len(all_model_path) + 1))
    if model_selected == 0:
        while True:
            new_name = input("请输入新的模型名称。按 <Ctrl-C> 退出。\n"
                             "Please enter a new model name. Press <Ctrl-C> to exit.\n"
                             ": ")
            if len(new_name) == 0:
                print("模型名称为空，请重新输入。\n"
                      "Model name is empty, please try again.\n")
                continue
            if new_name in all_model_name:
                print("该模型名称已存在，请重新输入。\n"
                      "The model name already exists, please try again.\n")
                continue
            model_path = model_path / new_name
            model_path.mkdir(parents=True, exist_ok=True)
            return True, str(model_path) + "/", None
    else:
        model_path = all_model_path[model_selected - 1]
        model_record_path = sorted(item for item in model_path.glob('*.h5'))
        model_record_name = [path.name[:-3] for path in model_record_path]
        if is_training:
            print("请选择想要训练的模型记录。按 <Ctrl-C> 退出。\n"
                  "Please select the model record you want to train. Press <Ctrl-C> to exit.")
        else:
            print("请选择想要使用的模型记录。按 <Ctrl-C> 退出。\n"
                  "Please select the model record you want to use. Press <Ctrl-C> to exit.")
        for i, one_model_record_name in enumerate(model_record_name):
            print("{0}: {1}".format(i + 1, one_model_record_name))
        model_record_selected = select(": ", allowed_input=range(1, len(model_record_path) + 1))
        return False, str(model_path) + "/", str(model_record_path[model_record_selected - 1])
