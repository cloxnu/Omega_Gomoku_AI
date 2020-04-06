from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from flask_socketio import SocketIO

bp = Blueprint("start", __name__, url_prefix="/start")
socket_io = SocketIO(async_mode="threading")

import Game.Board as BOARD
from Web import web_configure
from Web.web_game_thread import web_game_thread

# from gevent import monkey
# monkey.patch_all()

# import eventlet
# eventlet.monkey_patch()

game_thread = None
human_action = ()


@bp.route("/", methods=['POST', 'GET'])
def start():
    if web_configure.player == {}:
        return redirect(url_for('configure.configure'))
    context = {
        'board_size': BOARD.board_size,
        'player1_name': web_configure.player[0].name,
        'player2_name': web_configure.player[1].name,
        'player1_desc': str(web_configure.player[0]),
        'player2_desc': str(web_configure.player[1])
    }
    global game_thread
    if game_thread is not None:
        game_thread.stop()
        game_thread = None
    return render_template("start.html", **context)


@socket_io.on('connect')
def connect():
    print("websocket connected.")


@socket_io.on('start_game')
def start_game(command):
    if command == 'start':
        global game_thread
        if game_thread is None:
            send_board_init()
            send_game_start()
            game_thread = web_game_thread(player1=web_configure.player[0], player2=web_configure.player[1],
                                          send_board_step=send_board_step, turn_to=turn_to,
                                          send_player1_running=send_player1_running,
                                          send_player2_running=send_player2_running,
                                          wait_human_action=wait_human_action, game_over=game_over)
            game_thread.start()
        else:
            game_thread.stop()
            send_game_stop()
            game_thread = None
            print("stopped")


@socket_io.on('human_action')
def handle_action(action):
    global human_action
    human_action = action


def send_board_init():
    socket_io.emit('board_init', BOARD.board_size)


def send_game_start():
    socket_io.emit('game_start')


def send_game_stop():
    socket_io.emit('game_stop')


def send_board_step(current_player, action):
    i, j = action
    action = int(i), int(j)
    context = {
        'player': current_player,
        'action': action
    }
    socket_io.emit('board_step', context)


def turn_to(player):
    socket_io.emit('turn_to', 1 if player == BOARD.o else 2)


def send_player1_running(output):
    socket_io.emit('player1_running', output)


def send_player2_running(output):
    socket_io.emit('player2_running', output)


def wait_human_action(player, is_stop):
    socket_io.emit('take_human_action', player)
    global human_action
    while not is_stop():
        if human_action != ():
            action = human_action
            human_action = ()
            return action
    return None


def game_over(winner):
    if winner == BOARD.o:
        socket_io.emit('game_over', 1)
    elif winner == BOARD.x:
        socket_io.emit('game_over', 2)
    else:
        socket_io.emit('game_over', 0)
    global game_thread
    game_thread = None
