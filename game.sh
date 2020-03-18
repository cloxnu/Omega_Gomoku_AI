if [[ $1 = "-t" ]]
then
  python test.py
  exit 0
fi

echo ""
echo "欢迎使用 Omega_Gomoku_AI"
echo "Welcome to use Omega_Gomoku_AI"

while true
do
  echo ""
  echo "下一步操作，请输入对应的数字执行操作。按 <Ctrl-D> 结束"
  echo "Next step, please enter the corresponding number to perform the operation. Press <Ctrl-D> to end."
  echo "---------------------------"
  echo "0: 退出 Exit"
  echo "1: 配置游戏 Configure the game"
  echo "2: 运行游戏 Run"
  echo "3: 神经网络训练 Neural network training"
  echo "---------------------------"

  read -p ": " input
  case $input in
  0)
    break
    ;;
  1)
    python configure.py
    continue
    ;;
  2)
    python start.py
    continue
    ;;
  3)
    python train.py
    continue
    ;;
  *)
    echo "输入有误，请重新输入。"
    echo "The input is incorrect, please try again."
    continue
    ;;
  esac
done
