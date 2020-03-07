[![Starkidstory](Image/starkidstory_title.png)](https://starkidstory.com)

![Header](Image/omega_title.png)

# Omega_Gomoku_AI

**Omega_Gomoku_AI** is a Gomoku game AI based on Monte Carlo Tree Search. It's written in Python. 

<p align="center">
<a href="https://starkidstory.com"><img src="Image/star_badge.png" height=20></a>
<img src="Image/omega_badge.png" height=20/>
<br/>
<a href="https://github.com/CLOXnu/ConvenientImagePicker/blob/master/README.zh-cn.md"><img src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-README-blue.svg?style=flat"/></a>
</p>

**Omega_Gomoku_AI** is not only used for Gomoku game, but you can also customize the size of the board and an n-in-a-row game. Tic-tac-toe, for example, is a 3-in-a-row game, and played on a board of size 3.

This repo provides a ~~visual game interface~~, easy-to-use training process, and easy-to-understand code. 

Enjoy yourself ~~~

## 📖 References & thanks

About the algorithm, **Omega_Gomoku_AI** refers to this article: [Monte Carlo Tree Search – beginners guide](https://int8.io/monte-carlo-tree-search-beginners-guide/), written by [int8](https://github.com/int8).

**Omega_Gomoku_AI** Inspired by [AlphaZero_Gomoku](https://github.com/junxiaosong/AlphaZero_Gomoku) and [tictactoe_mcts](https://github.com/zhuliquan/tictactoe_mcts).


## 🏠 Code structure

- [start.py](start.py) - Start the game, human vs AI, or human vs human, or AI vs AI.
- ~~train.py - The training script, which can be used to train with different networks and saved models.~~
- [configure.py](configure.py) - Configure the game, including board size, n-in-a-row, and AI search times.
- [game.conf](game.conf) - Configuration file.
- [Function.py](Function.py) - Some functions.
- [Game/](Game/)
  - [Game.py](Game/Game.py) - An abstract class named Game, implemented by Console board and Visual board.
  - [ConsoleBoard.py](Game/ConsoleBoard.py) - implements class Game.
- [Player/](Player/)
  - [Player.py](Player/Player.py) - An abstract class named Player, implemented by Human and AIs.
  - [Human.py](Player/Human.py) - Human player, implements class Game.
  - [AI/](Player/AI/) - AIs.
    - [MonteCarloTreeSearch.py](Player/AI/MonteCarloTreeSearch.py) - An abstract class MonteCarloTreeSearch, implements by all AIs using MCTS.
    - [MonteCarloTreeNode.py](Player/AI/MonteCarloTreeNode.py) - Base class for nodes in Monte Carlo Tree.
    - [AI_MCTS.py](Player/AI/AI_MCTS.py) - AI player with pure MCTS, implements class Game.
    
    

