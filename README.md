[![Starkidstory](Image/starkidstory_title.png)](https://starkidstory.com)

![Header](Image/omega_title.png)

# Omega_Gomoku_AI

**Omega_Gomoku_AI** is a Gomoku game AI based on Monte Carlo Tree Search. It's written in Python. 

<p align="center">
<a href="https://starkidstory.com"><img src="Image/star_badge.png" height=20></a>
<img src="Image/omega_badge.png" height=20/>
</p>

**Omega_Gomoku_AI** is not only used for Gomoku game, but you can also customize the size of the board and an n-in-a-row game. Tic-tac-toe, for example, is a 3-in-a-row game, and played on a board of size 3.

This repo provides a ~~visual game interface~~, easy-to-use training process, and easy-to-understand code. 

Enjoy yourself ~~~

## 📖 References & thanks

About the algorithm, **Omega_Gomoku_AI** refers to this article: [Monte Carlo Tree Search – beginners guide](https://int8.io/monte-carlo-tree-search-beginners-guide/), witten by [[int8]](https://github.com/int8).

**Omega_Gomoku_AI** Inspired by [AlphaZero_Gomoku](https://github.com/junxiaosong/AlphaZero_Gomoku) and [tictactoe_mcts](https://github.com/zhuliquan/tictactoe_mcts).


## 🏠 Code structure

- [start.py](start.py) - [Detail](#start.py)
- ~~train.py~~
- [configure.py](configure.py)
- [game.conf](game.conf)
- [Function.py](Function.py)
- [Game/](Game/)
  - [Game.py](Game/Game.py)
  - [ConsoleBoard.py](Game/ConsoleBoard.py)
- [Player/](Player/)
  - [Player.py](Player/Player.py)
  - [Human.py](Player/Human.py)
  - [AI/](Player/AI/)
    - [MonteCarloTreeSearch.py](Player/AI/MonteCarloTreeSearch.py)
    - [MonteCarloTreeNode.py](Player/AI/MonteCarloTreeNode.py)
    - [AI_MCTS.py](Player/AI/AI_MCTS.py)
    
    
### start.py
    
    

