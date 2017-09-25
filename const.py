#!/usr/bin/env python
# -*- coding: utf-8 -*-

' const.py '

__author__ = 'Hyman Lee'


############## main code ###############

class _const:
    """常量数据类"""
    class ConstError(TypeError):
        """修改常量抛出此错误"""
        pass

    __PROPERTY_PATH = './translator.properties'

    def __init__(self):
        # 读取配置文件加载常量，常量名即为配置文件中的名字
        self.__load_config()

    def __load_config(self):
        with open(self.__PROPERTY_PATH, 'r') as f:
            for line in f.readlines():
                line = line.strip('\n').strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    key = strs[0].strip()
                    val = strs[1].strip()
                    self.__dict__[key] = val

    # def getsource(self):
    #     return self.__dict__['SOURCE']

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can not rebind const instance attribute (%s)" % name
        self.__dict__[name] = value


    def __delattr__(self, name):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can not unbind const instance attribute (%s)" % name
        raise AttributeError, "const instance has no attribute (%s)" % name


import sys
sys.modules[__name__] = _const()





