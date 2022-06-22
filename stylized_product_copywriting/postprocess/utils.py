
"""
Created on Fri Jun 18 13:41:22 2021

@author: xiaojie.guo
"""
#from pycorrector.macbert.macbert_corrector import MacBertCorrector
import os
import json
import pickle
import numpy as np
from multiprocessing import Pool
from collections import OrderedDict
import pandas as pd
import jieba

def classify(tokens, lda_model, dic):
     c_k=class_by_keyword(tokens)
     if c_k >= 0:
        return c_k
     else:    
        corpus = dic.doc2bow(tokens)
        row = lda_model.get_document_topics(corpus)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        orig_class = row[0][0]
        if orig_class in [11]:
                return 0
        if orig_class in [5,6,8]:
                return 3
        if orig_class in [2]:
                return 2 
        if orig_class in [0,1,3,9]:
                return 4                                                      
        if orig_class in [4]:
                return 1            
        if orig_class in [10,7]:
                return 5

def classify_1343(tokens, lda_model, dic):
     c_k=class_by_keyword_1314(tokens)
     if c_k >= 0:
        return c_k
     else:    
        corpus = dic.doc2bow(tokens)
        row = lda_model.get_document_topics(corpus)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        orig_class = row[0][0]
        if orig_class in [0,2,6,11]:
                return 0
        if orig_class in [1]:
                return 1
        if orig_class in [7,8]:
                return 2
        if orig_class in [5]:
                return 3
        if orig_class in [10]:
                return 5
        if orig_class in [12]:
                return 6
        if orig_class in [3,4,9]:
                return 8             

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

def load_csv(path):
    data=[]
    df = pd.read_csv(path)
    for row in df.iterrows():
      data.append(row[1]['product']+'|||'+row[1]['pred'])
    return data
      
def load_csv_sku(path):
    data=[]
    df = pd.read_csv(path)
    for row in df.iterrows():
      data.append(row[1]['product']+'|||'+row[1]['pred']+'|||'+str(row[1]['sku']))
    return data

def load_csv_sku_aspect(path):
    data=[]
    df = pd.read_csv(path)
    for row in df.iterrows():
      prod=row[1]['product'].split('|||')[1]
      aspect=row[1]['product'].split('|||')[0]
      try:
          data.append(aspect+'|||'+prod+'|||'+row[1]['pred']+'|||'+str(row[1]['sku']))
      except:
          print('failed generation!')
    return data    

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

def class_by_keyword(tokens):
    if len(set(['机身','外观','外壳']) & set(tokens))>0:
        a = 0
    elif len(set(['面容','解锁','指纹','人脸识别','面容ID']) & set(tokens))>0:
        a = 6          
    elif len(set(['屏','屏幕','英寸']) & set(tokens))>0:
        a = 1
    elif len(set(['网络','5G','双模']) & set(tokens))>0:
        a = 2
    elif len(set(['摄像头','三摄','四摄','广角','变焦','长焦','镜头','美颜','拍摄','镜头','后置','拍照','人像','单摄']) & set(tokens))>0:
        a = 3
    elif len(set(['处理器','存储','液冷','散热','内存','芯片']) & set(tokens))>0:
        a = 4
    elif len(set(['充电','续航','快充','电池']) & set(tokens))>0:
        a = 5          
    else:
        a = -1
    return a 


def class_by_keyword_1314(tokens):
    if len(set(['身材','比例','修身','宽松','版型']) & set(tokens))>0:
        a = 0
    elif len(set(['百搭','配搭','搭','穿搭']) & set(tokens))>0:
        a = 1
    elif len(set(['格纹', '千鸟格','色','颜色','条纹','图案','印花','撞色','字母','竖纹']) & set(tokens))>0:
        a = 2
    elif len(set(['面料','布料','纯棉','亲肤','材质','手感','透气性','羊毛','毛呢','鸭绒','保暖','羽绒','鹅绒','填充']) & set(tokens))>0:
        a = 3
    elif len(set(['口袋','插手','插袋','开袋','贴袋','插兜','物品']) & set(tokens))>0:
        a = 4
    elif len(set(['立领','圆领','衣领','领','翻领','领口','字领','颈部','高领','颈','尖领','连帽','帽']) & set(tokens))>0:
        a = 5  
    elif len(set(['裙摆','摆','百褶','荷叶','蛋糕','鱼尾','开叉','下摆']) & set(tokens))>0:
        a = 6   
    elif len(set(['袖口','袖']) & set(tokens))>0:
        a = 7                            
    elif len(set(['甜美','优雅','知性','复古','时尚','俏皮','少女','个性','时髦','性感','休闲','潮酷']) & set(tokens))>0:
        a = 8                            
    else:
        a = -1
    return a     



def stopwordslist():
    stopwords = [line.strip() for line in open('/home/xiaojie.guo/stylized_product_copywriting/topic_modeling/stop_words.txt', 'r', encoding='UTF-8').readlines()]
    stopwords.extend([])
    return stopwords

def seg_depart(sentence):
    sentence_depart = jieba.cut(sentence.strip())
    stopwords = stopwordslist()
    outstr = ''
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr     

def correct(sent):
    m = MacBertCorrector()
    correct_sent, err = m.macbert_correct(sent)
    return correct_sent
 