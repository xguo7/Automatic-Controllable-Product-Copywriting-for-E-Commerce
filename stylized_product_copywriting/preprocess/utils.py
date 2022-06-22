#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 13:41:22 2021

@author: xiaojie.guo
"""

import os
import json
import pickle
import numpy as np
from multiprocessing import Pool
from collections import OrderedDict


def load_json(path):
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)


def dump_json(path, data, indent=4):
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=indent)


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def dump_pickle(path, data):
    with open(path, "wb") as f:
        pickle.dump(data, f)


def load_txt(path):
    data = []
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            line = line.strip()
            data.append(line)
    return data


def dump_txt(path, data):
    with open(path, "w", encoding="utf8") as f:
        for line in data:
            f.write(line + "\n")


def make_dir_path(dir_path):
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


def make_path(f):
    'f should be a file path instead of dir'
    d = os.path.dirname(f)
    make_dir_path(d)


def multi_process_run(arg_list, fun, n_process=4):
    pool = Pool(processes=n_process)
    jobs = [pool.apply_async(fun, args=n) for n in arg_list]

    pool.close()
    pool.join()

    try:    # the fun doesn't have a non-None return value
        return [job.get() for job in jobs]
    except:
        return []


def split_data(data, n):
    l = len(data)
    sl = int(l / n)
    if sl*n != l:
        sl += 1
    data_list = []

    for i in range(0, l, sl):
        data_list.append(data[i:i+sl])
    return data_list

import re

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

def contain_zh(word):
    '''
    判断传入字符串是否包含中文
    :param word: 待判断字符串
    :return: True:包含中文  False:不包含中文
    '''
    global zh_pattern
    match = zh_pattern.search(word)

    return match