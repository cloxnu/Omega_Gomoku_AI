import sys

from console_select import select_network

from Train.train_with_net_junxiaosong import train_with_net_junxiaosong
from AI.Network.PolicyValueNet_from_junxiaosong import PolicyValueNet_from_junxiaosong


def train(specified_network=0, specified_model_name="", round_times=0, allow_user_input=True):
    network = select_network(is_training=True,
                             specified_network=specified_network, specified_model_name=specified_model_name)
    if isinstance(network, PolicyValueNet_from_junxiaosong):
        train_with_net_junxiaosong(network, allow_user_input, round_times)


if __name__ == '__main__':
    try:
        specified_network = int(sys.argv[1])
        specified_model_name = sys.argv[2]
        round_times = int(sys.argv[3])
    except:
        train()
    else:
        train(specified_network, specified_model_name, round_times, allow_user_input=False)
