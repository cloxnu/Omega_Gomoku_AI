[![Starkidstory](Image/starkidstory_title.png)](https://starkidstory.com)

![Header](Image/omega_title.png)

# Omega_Gomoku_AI

**Omega_Gomoku_AI** 是一个基于蒙特卡洛树搜索 (MCTS) 算法的五子棋 AI 游戏，用 Python 铸造。

<p align="center">
<a href="https://starkidstory.com"><img src="Image/star_badge.png" height=20></a>
<img src="Image/omega_badge.png" height=20/>
<br/>
<a href="https://github.com/CLOXnu/ConvenientImagePicker/blob/master/README.zh-cn.md"><img src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-README-blue.svg?style=flat"/></a>
</p>

**Omega_Gomoku_AI** 不仅用于五子棋游戏，你还可以自定义棋盘大小，以及几子连珠这样的游戏规则。例如井字棋，就是个 3\*3 大小的棋盘，三子连珠。

此仓库提供~~可视化游戏界面~~，易用的训练过程，以及易于理解的代码。

玩得愉快～～

## 📖 参考文献和感谢

关于算法，**Omega_Gomoku_AI** 参考于这篇文章：[Monte Carlo Tree Search – beginners guide](https://int8.io/monte-carlo-tree-search-beginners-guide/)，作者是 [int8](https://github.com/int8)。

**Omega_Gomoku_AI** 受启发于 [AlphaZero_Gomoku](https://github.com/junxiaosong/AlphaZero_Gomoku) 和 [tictactoe_mcts](https://github.com/zhuliquan/tictactoe_mcts).


## 🏠 代码结构

- [start.py](start.py) - 开始游戏，人类 vs AI，AI vs AI， 人类 vs 人类 均可调。
- ~~train.py - 训练脚本，可用不同网络和保存的模型进行训练。~~
- [configure.py](configure.py) - 配置游戏，包括棋盘尺寸，几子连珠，或者蒙特卡洛树的搜索次数。
- [game.conf](game.conf) - 配置文件。
- [Function.py](Function.py) - 一些功能函数。
- [Game/](Game/)
  - [Game.py](Game/Game.py) - 抽象类 Game, 被控制台棋盘 (Console board) 和可视化棋盘 (Visual board) 实现。
  - [ConsoleBoard.py](Game/ConsoleBoard.py) - 控制台棋盘，实现类 Game.
- [Player/](Player/)
  - [Player.py](Player/Player.py) - 抽象类 Player, 被人类玩家 (Human) 和 AI 玩家实现。
  - [Human.py](Player/Human.py) - 人类玩家，实现类 Player.
  - [AI/](Player/AI/) - AIs.
    - [MonteCarloTreeSearch.py](Player/AI/MonteCarloTreeSearch.py) - 抽象类 MonteCarloTreeSearch，被所有使用蒙特卡洛树搜索的 AI 实现。
    - [MonteCarloTreeNode.py](Player/AI/MonteCarloTreeNode.py) - 蒙特卡洛树节点的基类。
    - [AI_MCTS.py](Player/AI/AI_MCTS.py) - 纯蒙特卡洛树搜索的 AI 玩家，实现类 Player, MonteCarloTreeSearch.
    
    
## 用法

你可以自己尝试 **Omega_Gomoku_AI**，方法如下：

### 使用 Docker

如果你安装了 Docker，那么执行如下命令：

```shell
$ docker pull clox/omega_gomoku_ai:1.0
```

然后，执行：

```shell
$ docker run -it clox/omega_gomoku_ai:1.0
```

完成后，尽情玩耍。

### 使用 PC/Mac/Linux

Make sure you have a Python environment installed on your computer, and after cloning this repo, then run the following command:

```shell
$ pip install -r requirement.txt
```

必要时，命令 'pip' 可改为 'pip3'。

使用 Mac/Linux，只需运行：

```shell
$ bash game.sh
```

或者，分开运行：

```shell
$ python configure.py
```

来配置游戏，运行：

```shell
$ python start.py
```

来开始游戏。

无论何种方式都相当简单。


## 开始。。。

默认地，游戏会在 8\*8 的棋盘上进行五子连珠游戏，并且纯蒙特卡洛树的 AI 玩家会进行每回合 2,000 次的搜索。

![AI thinking](Image/AI_thinking.png)

![AI_moves](Image/AI_moves.png)

有时，纯蒙特卡洛树的 AI 玩家会执行一些诡异的落子，这是因为每回合 2,000 次的搜索对于五子连珠游戏太少了。所以你可以将棋盘大小设为 3\*3，或是 4\*4，设为三子连珠或是四子连珠，就像井字棋。

当然，把 2,000 次每回合的搜索次数改得更多也是个好主意，不过这样会牺牲时间。

~~带有神经网络的蒙特卡洛树搜索的 AI 玩家会解决这个问题。~~


## 未完待续。。。


