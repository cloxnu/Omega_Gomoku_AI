const board_steps = new Set();
let human_player = 0;

let socket = io();
socket.on('connect', function () {
    console.log('websocket connected');
    // socket.emit('action', {data: '(6, 7)'});
});

socket.on('disconnect', function () {
    console.log('websocket disconnected');
    socket.disconnect();
});

socket.on('board_init', function (board_size) {
    board_init(board_size);
});

socket.on('game_start', function () {
    human_player = 0;
    board_steps.clear();
    console.log('game start');
    document.getElementById("start-button").value = "停止游戏 Stop";
});

socket.on('game_stop', function () {
    human_player = 0;
    board_steps.clear();
    console.log('game stop');
    document.getElementById("start-button").value = "开始游戏 Start";
});

socket.on('board_step', function (json) {
    board_steps.add('' + json['action'][0] + ',' + json['action'][1]);
    draw_piece_on_board(json['player'], json['action'])
});

socket.on('turn_to', function (player) {
    if (player === 1) {
        document.getElementById("player1-div").style.background = "lightblue";
        document.getElementById("player2-div").style.background = "white";
        document.getElementById("player1-running").style.display = "block";
        document.getElementById("player2-running").style.display = "none";
    } else {
        document.getElementById("player2-div").style.background = "lightblue";
        document.getElementById("player1-div").style.background = "white";
        document.getElementById("player2-running").style.display = "block";
        document.getElementById("player1-running").style.display = "none";
    }
});

socket.on('player1_running', function (output) {
    document.getElementById("player1-running").innerHTML = "思考中 running... " + output;
});

socket.on('player2_running', function (output) {
    document.getElementById("player2-running").innerHTML = "思考中 running... " + output;
});

socket.on('take_human_action', function (player) {
    human_player = player;
    document.getElementById("player" + player + "-running").innerHTML =
        "请点击棋盘落子<br>Please click on the board";
});

function send_human_action(action) {
    human_player = 0;
    socket.emit('human_action', action);
}

socket.on('game_over', function (winner) {
    human_player = 0;
    document.getElementById("start-button").value = "开始游戏 Start";
    if (winner === 1) {
        alert("黑子获胜 Black wins!");
    } else if (winner === 2) {
        alert("白子获胜 White wins!");
    } else {
        alert("平局");
    }
});


function board_init(board_size) {
    console.log("board_init");
    const canvas = document.getElementById("board");
    const context = canvas.getContext("2d");

    context.clearRect(0, 0, canvas.width, canvas.height);
    context.shadowOffsetX = 0;
    context.shadowOffsetY = 0;
    context.shadowBlur = 0;
    const size = (board_size-1) * 40;
    for (let i = 20; i <= size+20; i += 40)
    {
        context.beginPath();
        context.moveTo(20, i);
        context.lineTo(size+20, i);
        context.closePath();
        context.strokeStyle = "#4c402f";
        context.stroke();

        context.beginPath();
        context.moveTo(i, 20);
        context.lineTo(i, size+20);
        context.closePath();
        context.strokeStyle = "#4c402f";
        context.stroke();
    }
}

function start_game() {
    socket.emit('start_game', 'start');
}


var current_transparent_piece = [];

function mouse_move_on_canvas(event) {
    if (human_player === 0)
        return;

    const x = event.layerX;
    const y = event.layerY;

    if (x < 5 || y < 5) {
        if (current_transparent_piece.length !== 0)
            clear_piece_on_transparent_board();
    } else if (((x - 5) % 40 > 30) || ((y - 5) % 40 > 30)) {
        if (current_transparent_piece.length !== 0)
            clear_piece_on_transparent_board();
    } else {
        const actionX = parseInt((x - 5) / 40);
        const actionY = parseInt((y - 5) / 40);
        if (current_transparent_piece.length !== 0) {
            if (current_transparent_piece !== [actionX, actionY])
                draw_piece_on_transparent_board(human_player, [actionX, actionY]);
        } else {
            draw_piece_on_transparent_board(human_player, [actionX, actionY]);
        }
    }
}

function mouse_click_on_canvas(event) {
    if (human_player === 0)
        return;

    const x = event.layerX;
    const y = event.layerY;

    if (x < 5 || y < 5) {

    } else if (((x - 5) % 40 > 30) || ((y - 5) % 40 > 30)) {

    } else {
        const actionX = parseInt((x - 5) / 40);
        const actionY = parseInt((y - 5) / 40);
        if (board_steps.has('' + actionX + ',' + actionY))
            return;
        send_human_action([actionX, actionY]);
    }
}

function mouse_out_on_canvas() {
    if (current_transparent_piece.length !== 0)
        clear_piece_on_transparent_board();
}

function draw_piece_on_board(player, action) {
    const canvas = document.getElementById("board");
    const context = canvas.getContext("2d");

    const x = action[0];
    const y = action[1];

    context.shadowOffsetX = 0;
    context.shadowOffsetY = 3;
    context.shadowBlur = 5;
    context.shadowColor = "#777777";

    context.beginPath();
    context.arc(x * 40 + 20, y * 40 + 20, 15, 0, Math.PI * 2);
    context.fillStyle = player === 1 ? "#202020" : "#f0f0f0";
    context.fill();
}

function clear_piece_on_transparent_board() {
    current_transparent_piece = [];
    const canvas = document.getElementById("transparent-board");
    canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
}

function draw_piece_on_transparent_board(player, action) {
    clear_piece_on_transparent_board();
    current_transparent_piece = action;

    if (board_steps.has('' + action[0] + ',' + action[1]))
        return;

    const canvas = document.getElementById("transparent-board");
    const context = canvas.getContext("2d");

    const x = action[0];
    const y = action[1];

    context.shadowOffsetX = 0;
    context.shadowOffsetY = 0;
    context.shadowBlur = 0;

    context.globalAlpha = 0.5;
    context.beginPath();
    context.arc(x * 40 + 20, y * 40 + 20, 15, 0, Math.PI * 2);
    context.fillStyle = player === 1 ? "#202020" : "#f0f0f0";
    context.fill();
}
