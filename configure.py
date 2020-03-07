import configparser


class Configure:

    def __init__(self):
        self.conf = configparser.ConfigParser(allow_no_value=True)
        self.conf.read("game.conf")
        self.conf_dict = {}

    def get_conf(self):
        self.conf_dict["o"] = self.conf.getint("Fixed", "o")
        self.conf_dict["x"] = self.conf.getint("Fixed", "x")
        self.conf_dict["empty"] = self.conf.getint("Fixed", "empty")

        self.conf_dict["n_in_a_row"] = self.conf.getint("Changeable", "n_in_a_row")
        self.conf_dict["start_player"] = self.conf.getint("Changeable", "start_player")
        self.conf_dict["board_size"] = self.conf.getint("Changeable", "board_size")

        self.conf_dict["AI_search_times"] = self.conf.getint("AI", "search_times")
        self.conf_dict["AI_is_output_analysis"] = self.conf.getboolean("AI", "is_output_analysis")

    def set_board_size(self, size):
        self.conf.set("Changeable", "board_size", str(size))
        self.conf.write(open("game.conf", "w"))

    def set_n_in_a_row_game(self, n):
        self.conf.set("Changeable", "n_in_a_row", str(n))
        self.conf.write(open("game.conf", "w"))

    def set_AI_search_times(self, times):
        self.conf.set("AI", "search_times", str(times))
        self.conf.write(open("game.conf", "w"))

    def set_AI_is_output_analysis(self, is_output_analysis):
        self.conf.set("AI", "is_output_analysis", str(is_output_analysis))
        self.conf.write(open("game.conf", "w"))


if __name__ == '__main__':
    conf = Configure()
    conf.get_conf()

    size = conf.conf_dict["board_size"]
    n_in_a_row = conf.conf_dict["n_in_a_row"]
    AI_search_times = conf.conf_dict["AI_search_times"]
    AI_is_output_analysis = conf.conf_dict["AI_is_output_analysis"]

    while True:
        input1 = input("配置 1：请输入棋盘大小 size. (size >= 3)\n"
                       "Config 1: Please input the size of board. (size >= 3)\n"
                       "size ({}) = ".format(size))
        try:
            input_int = size if len(input1) == 0 else int(input1)
            if input_int < 3:
                print("size 应该大于等于 3，请重新输入。\n"
                      "size should be greater than or equal to 3. Please try again.\n")
                continue
            size = input_int
        except:
            print("输入有误，请重新输入。\n"
                  "The input is incorrect. Please try again.\n")
            continue
        break

    while True:
        input2 = input("配置 2：请输入几子连珠 n. (n >= 3)\n"
                       "Config 2: Please input how many pieces in a row. (n >= 3)\n"
                       "n ({}) = ".format(n_in_a_row))
        try:
            input_int2 = n_in_a_row if len(input2) == 0 else int(input2)
            if input_int2 < 3:
                print("n 应该大于等于 3，请重新输入。\n"
                      "n should be greater than or equal to 3. Please try again.\n")
                continue
            n_in_a_row = input_int2
        except:
            print("输入有误，请重新输入。\n"
                  "The input is incorrect. Please try again.\n")
            continue
        break

    while True:
        input3 = input("配置 3：请输入 AI 搜索次数 search times. (times >= 1)\n"
                       "Config 2: Please input the AI search times. (times >= 1)\n"
                       "AI search times ({}) = ".format(AI_search_times))
        try:
            input_int3 = AI_search_times if len(input3) == 0 else int(input3)
            if input_int3 < 1:
                print("times 应该大于等于 1，请重新输入。\n"
                      "times should be greater than or equal to 0. Please try again.\n")
                continue
            AI_search_times = input_int3
        except:
            print("输入有误，请重新输入。\n"
                  "The input is incorrect. Please try again.\n")
            continue
        break

    while True:
        input4 = input("配置 4：请输入是否输出 AI 分析数据，[Y/y]输出，[N/n]不输出。\n"
                       "Config 2: Please input the AI search times. [Y/y] output, [N/n] not output.\n"
                       "AI is output analysis ({}) = ".format(AI_is_output_analysis))
        if len(input4) == 0:
            pass
        elif input4 == "n" or input4 == "N":
            AI_is_output_analysis = False
        elif input4 == "y" or input4 == "Y":
            AI_is_output_analysis = True
        else:
            print("输入有误，请重新输入。\n"
                  "The input is incorrect. Please try again.\n")
            continue
        break

    conf.set_board_size(size)
    conf.set_n_in_a_row_game(n_in_a_row)
    conf.set_AI_search_times(AI_search_times)
    conf.set_AI_is_output_analysis(AI_is_output_analysis)

    print("设置成功！\n"
          "Success!")
