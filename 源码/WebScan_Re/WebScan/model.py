# coding:utf-8
import importlib,json,os


from output import printf


class models:
    def __init__(self):
        self.models = []

    def get_models(self):
        '''
            递归模块信息
        '''
        file_dir = "./plugins"
        models = []
        dir_list = os.listdir(file_dir)
        for cur_file in dir_list:
            # 获取文件的绝对路径
            path = os.path.join(file_dir, cur_file)
            if os.path.isdir(path):
                if self.check_model(cur_file):
                    models.append(self.get_info(cur_file))
        return models

    def check_model(self, model):  # 检查模块完整性（只是简单的检查，对内容的检查有待添加）
        file_dir = "./plugins"
        path = os.path.join(file_dir, model)
        if not os.path.exists(path + "/" + model + ".py"):
            printf("[-][" + model + "]Module error! Lack of running core files!", "red")
            return False
        if not os.path.exists(path + "/Repair.py"):
            printf("[-][" + model + "]Module error! Lack of repair scripts!", "red")
            return False
        if not os.path.exists(path + "/info.json"):
            printf("[-][" + model + "]Module error! Lack of module information file!", "red")
            return False
        return True

    def get_info(self, model):
        file = "./plugins/" + model + "/info.json"
        with open(file, mode="r") as file_obj:
            contents = file_obj.read().rstrip()
        re = json.loads(contents)
        re["model"] = model
        return re

    def run_model(self, model, urls, thread, islog,session):
        params = importlib.import_module('plugins.' + model + '.' + model)  # 绝对导入
        params.run(urls, thread, islog,session)
