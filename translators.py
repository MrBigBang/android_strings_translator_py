#!/usr/bin/env python
# -*- coding: utf-8 -*-

' translators.py '

__author__ = 'Hyman Lee'


############## main code ###############

import random
import requests
import json
from urllib import urlencode
import hashlib

class GoogleTranslator(object):
    """todo: google翻译"""
    def __init__(self):
        super(GoogleTranslator, self).__init__()

    def translate(self, text, source, target):
        pass


class YouDaoTranslator(object):
    """有道翻译"""
    __salt = 0
    __app_secret = '应用密钥'
    __app_id = '应用ID'

    def __init__(self):
        super(YouDaoTranslator, self).__init__()

    def translate(self, text, source, target):
        sign = self.__get_sign(text)
        params = {'q': text, 'from': source, 'to': target, 'appKey': self.__app_id, 'salt': self.__salt, 'sign': sign}
        params = urlencode(params)
        # print params
        r = requests.get('http://openapi.youdao.com/api?' + params)
        if r.status_code == 200:
            #判断errorCode是否为0
            # response = json.dumps(r.text, sort_keys=True, indent=4, separators=(',', ': '))
            # print response
            # r.json()
            json_res = json.loads(r.text)
            # print json_res[u'errorCode']
            if json_res[u'errorCode'] == u'0':
                # 进行解析，获取翻译数据
                translation_list = json_res[u'translation']
                # print translation_list
                if len(translation_list) > 0:
                    return translation_list[0]
                web_translation_list = json_res[u'web']
                if len(web_translation_list) > 0:
                    return web_translation_list[0][u'value'][0]

    def __get_sign(self, q):
        self.__salt = random.randint(0, 99)
        # print "salt %d" % self.__salt
        #appKey+q+salt+密钥 得到str，然后MD5 得到sign
        str = '%s%s%d%s' % (self.__app_id, q, self. __salt, self.__app_secret)
        # print str
        m = hashlib.md5()
        m.update(str)
        sign =  m.hexdigest().upper()
        # print sign
        return sign





if __name__ == '__main__':
    t = YouDaoTranslator()
    print t.translate('测试', 'zh_CHS', 'EN')
