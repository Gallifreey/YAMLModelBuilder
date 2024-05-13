from os import PathLike

import yaml


class YAMLReader(object):

    def __init__(self, path: PathLike):
        self.__data: dict = {}
        self.__path: PathLike = path
        self.start()

    def start(self):
        with open(self.__path, 'r') as f:
            self.__data = yaml.load(f)
            f.close()

    def get_yaml_data(self):
        return self.__data
