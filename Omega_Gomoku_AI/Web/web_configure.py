from flask import Blueprint, redirect, render_template, request, jsonify, url_for

bp = Blueprint("configure", __name__, url_prefix="/configure")

from Web.web_select import web_select

model_select = [web_select(), web_select()]

from Player.Human import Human
from Player.AI_MCTS import AI_MCTS
from Player.AI_MCTS_Net import AI_MCTS_Net
from AI.Network.PolicyValueNet_from_junxiaosong import PolicyValueNet_from_junxiaosong

player = {}


@bp.route("/", methods=['POST', 'GET'])
def configure():
    if request.method == 'POST':
        player_conf = ({}, {})
        for i in range(2):
            for j in range(7):
                player_conf[i][j] = request.form.get('select{}-{}'.format(i + 1, j), -1)
        ready_to_start(player_conf)
        return redirect(url_for("start.start"))
    return render_template("configure.html")


def ready_to_start(player_conf: (dict, dict)):
    for player_index, conf in enumerate(player_conf):
        name = conf[1]
        if conf[0] == "1":  # Human
            player[player_index] = Human(name=name)
        elif conf[0] == "2":  # AI with pure MCTS
            search_times = 2000 if conf[2] == -1 else int(conf[2])
            greedy_value = 0.5 if conf[3] == -1 else float(conf[3])
            player[player_index] = AI_MCTS(name=name, search_times=search_times, greedy_value=greedy_value,
                                           is_output_analysis=False, is_output_running=False)
        elif conf[0] == "3":  # AI with neural network
            search_times = 2000 if conf[2] == -1 else int(conf[2])
            greedy_value = 0.5 if conf[3] == -1 else float(conf[3])
            model_select[player_index].set_record_path(record_index=int(conf[6]) - 1)
            if conf[4] == "1":  # network
                policy_value_net = PolicyValueNet_from_junxiaosong(
                    is_new_model=False, is_in_thread=True,
                    model_dir=model_select[player_index].selected_model_path,
                    model_record_path=model_select[player_index].selected_record_path)
            else:
                policy_value_net = PolicyValueNet_from_junxiaosong(
                    is_new_model=False, is_in_thread=True,
                    model_dir=model_select[player_index].selected_model_path,
                    model_record_path=model_select[player_index].selected_record_path)
            player[player_index] = AI_MCTS_Net(name=name, policy_value_function=policy_value_net.predict,
                                               board_to_xlabel=policy_value_net.board_to_xlabel,
                                               search_times=search_times, greedy_value=greedy_value,
                                               is_output_analysis=False, is_output_running=False)


@bp.route("/models", methods=['POST'])
def get_models():
    value = request.get_json()['network']
    curr_player = request.get_json()['player']
    if value == 1:
        model_select[curr_player].load_models(dir="Model/PolicyValueNet_from_junxiaosong")
        res = model_select[curr_player].all_model_name
        return jsonify(res)


@bp.route("/records", methods=['POST'])
def get_records():
    value = request.get_json()['model']
    curr_player = request.get_json()['player']
    model_select[curr_player].set_model_path(model_index=value)
    res = model_select[curr_player].get_all_record_name(model_index=value)
    return jsonify(res)
