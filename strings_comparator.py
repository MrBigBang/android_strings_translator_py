#!/usr/bin/env python
# -*- coding: utf-8 -*-

' strings_comparator.py '

__author__ = 'Hyman Lee'


############## main code ###############
import os
# from xml.dom import minidom
from translators import YouDaoTranslator
import const
from openpyxl import Workbook
from openpyxl import load_workbook
from excel_helper import ExcelHelper
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

translator = YouDaoTranslator()
wb = Workbook()


def get_strings_dict(tree, strings_dict):
    root = tree.getroot()
    for elem in tree.iter(tag = 'string'):
        strings_dict[elem.attrib['name']] = elem.text


def do_translate(strs2translated, source, target):
    for id in strs2translated:
        # print strs2translated[id]
        translated_str = translator.translate(strs2translated[id][const.SOURCE].encode('utf-8'), source, target)
        print translated_str
        strs2translated[id][const.TARGET] = translated_str


def translate_untranslated_string(from_dict, to_dict, source = 'zh_CHS', target = 'EN'):
    #格式：{'id':{'zh-CHS':'中国', 'EN':'China'}, ...}
    new_translated_strings = {}
    for from_key in from_dict:
        isTranslated = False
        for to_key in to_dict:
            if(from_key == to_key):
                isTranslated = True
                break
        if(not isTranslated):
            #没有翻译，调用google翻译api进行翻译，先存中文。
            new_translated_strings.setdefault(from_key, {})
            new_translated_strings[from_key][const.SOURCE] = from_dict[from_key]
    #一次请求
    do_translate(new_translated_strings, source, target)
    return new_translated_strings
    # print translated_rest

#该方法参考于：http://blog.csdn.net/shinobiii/article/details/8253976
# root_elem为传进来的Elment类，参数indent用于缩进，newline用于换行
def prettyxml(root_elem, indent, newline, level = 0):
    if root_elem:  # 判断element是否有子元素
        if root_elem.text == None or root_elem.text.isspace(): # 如果element的text没有内容
            root_elem.text = newline + indent * (level + 1)
        else:
            root_elem.text = newline + indent * (level + 1) + root_elem.text.strip() + newline + indent * (level + 1)
    #else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        #root_elem.text = newline + indent * (level + 1) + root_elem.text.strip() + newline + indent * level
    temp = list(root_elem) # 将root_elem转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyxml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作


def get_files(file_dir):
    # print os.path.abspath(os.curdir)
    cur_dir =  os.path.abspath('.')
    en_string_path = os.path.join(cur_dir, 'strings/values/strings.xml')
    zh_string_path = os.path.join(cur_dir, 'strings/values-zh-rCN/strings.xml')
    # print zh_string_path
    # print en_string_path
    ####先处理 string 标签
    zh_tree = ET.parse(zh_string_path)
    zh_strings_dict = {}
    get_strings_dict(zh_tree, zh_strings_dict)
    en_tree = ET.parse(en_string_path)
    en_strings_dict = {}
    get_strings_dict(en_tree, en_strings_dict)

    translated_rest = translate_untranslated_string(zh_strings_dict, en_strings_dict)
    root = en_tree.getroot()
    for name in translated_rest:
        #将新翻译的string追加到value-en/strings.xml中
        # root.append()
        # ET.SubElement(parent, tag)
        elem = ET.SubElement(root, 'string', {'name': name})
        elem.text = translated_rest[name][const.TARGET]
        # print elem
        # root.append(elem)
    tree = ET.ElementTree(root)
    prettyxml(tree.getroot(), '\t', os.linesep)
    # tree.write("test_en.xml", encoding="UTF-8")
    tree.write(en_string_path, encoding="utf-8", xml_declaration=True)

    #写入excel中，记录在线翻译的字符串
    eh = ExcelHelper(const.TRANSLATION_RECORD_PATH, const.TRANSLATION_RECORD_FILE)
    eh.record(translated_rest)



if __name__ == '__main__':
    get_files("")
