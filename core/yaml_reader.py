from os import PathLike
from typing import Union

import yaml
from yaml import FullLoader


class YAMLReader(object):

    def __init__(self, path: Union[str, PathLike[str]]):
        self.__data: dict = {}
        self.__path: PathLike = path
        self.start()

    def start(self):
        with open(self.__path, 'r') as f:
            self.__data = yaml.load(f, Loader=FullLoader)
            f.close()

    def get_yaml_data(self):
        return self.__data
