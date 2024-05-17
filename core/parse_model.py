import torch.nn as nn

from utils.util import get_object_by_id


class ModelParser(object):
    """
    模型解释器
    """

    def __init__(self, context: list[str], data: dict, package_path: str):
        self.__context = context
        self.__data = data
        self.__model = nn.ModuleList()
        self.__package = __import__(package_path)
        self.__torch_package = __import__(name='torch.nn', fromlist=['nn'])

    def build(self):
        for ctx in self.__context:
            if ctx not in self.__data.keys():
                continue
            self._parse_one_structure(ctx)

    def _parse_one_structure(self, key: str):
        for model in self.__data[key]:
            self._parse_one_operator(model[1], [model[0], model[-1]])

    def _parse_one_operator(self, name: str, params: list):
        if '.' in name:
            self.__model.append(getattr(self.__torch_package, name.split('.')[-1])(*params[1]))
        else:
            obj = getattr(self.__package, name)(*params[1])
            # 特殊处理残差结构
            if isinstance(params[0], list) and len(params[0]) > 1:
                # 需要允许自定义Concat存在`fromModules`属性
                if not hasattr(obj, 'fromModules'):
                    raise RuntimeError(f'Attribute fromModules is not exist in your model {name} ')
                obj.fromModules = params[0]
            self.__model.append(obj)

    def get_model(self):
        return self.__model

    def forward(self, x):
        history_ids = []
        for index, m in enumerate(self.__model):
            if hasattr(m, 'fromModules'):
                # 说明是残差
                x = m([get_object_by_id(history_ids[i]) for i in m.fromModules])
            else:
                x = m(x)
            history_ids.append(id(x))
        return x
