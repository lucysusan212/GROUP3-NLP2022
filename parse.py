from __future__ import annotations

import json
import pickle

import jsonpath
import os


def createFolder(folder_route: str) -> None:
    """
    判断该路径文件夹是否存在，如果不存在，则创建该文件夹
    :param folder_route: 文件夹路径，以/结尾
    :return:
    """
    if not os.path.exists(folder_route):
        os.makedirs(folder_route)


def json_str_list(data: dict | list, key: str) -> list:
    str_list = jsonpath.jsonpath(data, "$.." + key)
    return str_list if str_list else []


def in_ex_str(data: dict, include_key: list, exclude_key: list) -> list:
    s = []
    for in_key in include_key:
        s += json_str_list(data, in_key)
    for ex_key in exclude_key:
        ex = jsonpath.jsonpath(data, "$.." + ex_key)
        for in_key in include_key:
            s = list(set(s).difference(set(json_str_list(ex, in_key))))
    s = list(filter(None, s))
    return s


folder_route = ["../document_parses/pdf_json/", "../document_parses/pmc_json/"]
include_key = ['text', 'title']
exclude_key = ['cite_spans', 'ref_entries']
str_list = []

for folder in folder_route:
    file_list = os.listdir(folder)
    for file in file_list:
        with open(folder + file) as f:
            data = json.load(f)
            str_list += in_ex_str(data, include_key, exclude_key)

out_folder = "../parse/"
createFolder(out_folder)
parse_file = out_folder + 'parsedata.pkl'
with open(parse_file, 'wb') as pf:
    pickle.dump(str_list, pf)

# with open(parse_file, 'rb') as pf:
#     str_list = pickle.load(pf)
