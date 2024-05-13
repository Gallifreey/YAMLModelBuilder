import torch.nn as nn


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
            if ctx not in self.__data:
                raise RuntimeError(f"Unexpected model key found in {ctx}")
            self._parse_one_structure()

    def _parse_one_structure(self):
        pass

    def _parse_one_operator(self, name: str, params: list, at=-1):
        if '.' in name:
            self.__model.append(getattr(self.__torch_package, name.split('.')[-1])(params))
        else:
            self.__model.append(getattr(self.__package, name)(params))




