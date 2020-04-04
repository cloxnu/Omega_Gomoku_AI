import pathlib

from configure import Configure


class web_select:

    def __init__(self):
        self.all_model_path = []
        self.all_model_name = []
        self.all_record_path = []
        self.all_record_name = []
        self.selected_model_path = ""
        self.selected_record_path = ""

    def load_models(self, dir: str):
        conf = Configure()
        conf.get_conf()
        board_conf_str = "{0}_{1}".format(conf.conf_dict["board_size"], conf.conf_dict["n_in_a_row"])
        model_path = pathlib.Path(dir) / board_conf_str
        model_path.mkdir(parents=True, exist_ok=True)
        self.all_model_path = sorted(item for item in model_path.glob('*/') if item.is_dir())
        self.all_model_name = [path.name for path in self.all_model_path]

    def set_model_path(self, model_index: int):
        self.selected_model_path = str(self.all_model_path[model_index]) + "/"

    def get_all_record_name(self, model_index: int):
        """
        根据用户选择的模型检测模型记录。
        Check model records based on the model selected by the user.
        :param model_index: 模型序号。 The index of model.
        :return: [<str>] 所有模型记录。 All the model record.
        """
        model_path = self.all_model_path[model_index]
        self.all_record_path = sorted(item for item in model_path.glob('*.h5'))
        self.all_record_name = [path.name[:-3] for path in self.all_record_path]
        return self.all_record_name

    def set_record_path(self, record_index: int):
        self.selected_record_path = str(self.all_record_path[record_index])
