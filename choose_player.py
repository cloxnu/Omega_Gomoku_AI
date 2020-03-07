
def choose(prompt):
    """
    选择玩家。
    Choose player.
    :return: <bool>
    """
    is_choose = True

    while True:
        input_str = input(prompt)
        try:
            input_int = int(input_str)
            if input_int == 1:
                is_choose = True
            elif input_int == 2:
                is_choose = False
            else:
                print("输入有误，请重新输入。\n"
                      "The input is incorrect. Please try again.\n")
                continue
        except:
            print("输入有误，请重新输入。\n"
                  "The input is incorrect. Please try again.\n")
            continue
        break

    input_name = input("它的名字是。 It's name is.\n"
                       ": ")
    return is_choose, input_name
