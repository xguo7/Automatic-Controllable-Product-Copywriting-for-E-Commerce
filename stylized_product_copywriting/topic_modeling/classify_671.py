import jieba
import numpy as np
# Plotting tools
#import pyLDAvis
#import pyLDAvis.gensim # don't skip this
import matplotlib.pyplot as plt

#Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import openpyxl
import re
import os

def check_multi(tokens):
    topic_words=[
    ['显卡','独立','独显'],
    ['体型','小巧','材质','机身','外形','外观','金属','体积'],
    ['存储','硬盘','内存','固态','储存'],
    ['风扇','散热','降温','热量'],
    ['指纹','解锁','隐私','安全','密码','指纹识别','加密'],
    ['触控','接口','模式','点触','转轴','旋转','翻转','协同'],
    ['电池','续航','电量','充电','持久','待机'],
    ['键盘','按键','手感','回弹','音效','声音','杜比','声音','发声'],
    ['屏幕','高清','刷新率','分辨率','屏','护眼','蓝光','显示屏','像素','摄像头']]
    count=0
    for topic in topic_words:
        for word in tokens:
            if word in topic:
                count+=1
                break      
    return count


def class_by_keyword(tokens):
    if len(set(['显卡','独立','独显']) & set(tokens))>0:
        a = 0   
    elif len(set(['体型','小巧','材质','机身','外形','外观','金属','体积']) & set(tokens))>0:
        a = 1
    elif len(set(['存储','硬盘','内存','固态','储存','处理器','芯片']) & set(tokens))>0:
        a = 2
    elif len(set(['风扇','散热','降温','热量']) & set(tokens))>0:
        a = 3
    elif len(set(['指纹','解锁','隐私','安全','密码','指纹识别','加密']) & set(tokens))>0:
        a = 4
    elif len(set(['触控','接口','模式','点触','转轴','旋转','翻转','协同']) & set(tokens))>0:
        a = 5                          
    elif len(set(['电池','续航','电量','充电','待机']) & set(tokens))>0:
        a = 6     
    elif len(set(['键盘','按键','手感','回弹','音效','声音','杜比','声音','发声']) & set(tokens))>0:
        a = 7       
    elif len(set(['屏幕','高清','刷新率','分辨率','屏','护眼','蓝光','显示屏','像素','摄像头']) & set(tokens))>0:
        a = 8                                     
    else:
        a = -1
    return a 



#read data
path='/home/xiaojie.guo/daren_data/671/'
with open(path+'daren671_clean.csv', 'r', encoding='utf-8') as f:
    orig_data=f.readlines()

workbook=openpyxl.load_workbook(path+'assigned_topic_671_13class.xlsx')
topic_data=workbook.worksheets[0]


len_=len(orig_data)
class_l=list(topic_data.rows)[1:]
new_origin=[]
print(len(class_l))
print(len_)
if len(class_l)==len_: #missed the last item
    print('class and product match!')
        
    new_class_l=[]
    score_l=[]
    count=0
    for i in range(0,len_):
        orig_class=class_l[i][1].value
        orig_tokens=class_l[i][4].value
        tokens=set(re.split(",|'",orig_tokens[1:-1]))
            
        if  check_multi(tokens) <2 and len(tokens)>3 and len(tokens)<30 :
            new_origin.append(orig_data[i])
            c_k=class_by_keyword(tokens)
            if c_k >= 0:
                count+=1
                new_class_l.append(c_k)
                score_l.append(1)
                #print(orig_tokens+"by keywords: " +str(c_k))

            else:
                #print('again!')
                score_l.append(class_l[i][2].value)
                if orig_class in [8,11]:
                        new_class_l.append(0)

                if orig_class in [1]:
                        new_class_l.append(1) 

                if orig_class in [2,12]:
                        new_class_l.append(2)  

                if orig_class in [0]:
                        new_class_l.append(3)                                                      

                if orig_class in [3]:
                        new_class_l.append(4)             

                if orig_class in [4,6]:
                        new_class_l.append(5)

                if orig_class in [5]:                   
                        new_class_l.append(6)

                if orig_class in [7]:
                        new_class_l.append(7) 

                if orig_class in [9,10]:
                        new_class_l.append(8) 
    final_class=[]
    #filter the low score (<0.5):
  

    os.makedirs(path+'assigned_write_671/')
    for i in range(len(new_origin)):   
        item = new_origin[i].replace("#",'')
        new_class = new_class_l[i]
        score = score_l[i]
        #print(item+str(new_class))
        if score>0.6:
            with open(path+'assigned_write_671/assigned_write'+str(new_class)+'.txt', 'a', encoding='utf-8') as f:
                f.write(item[:-1]+'|||'+str(new_class)+'|||'+str(score)+'\n')
                final_class.append(new_class)

    ##统计各个类别的文案数目
    from collections import Counter
    print(Counter(final_class)) 
    print(count)
                            
else:
    print('class and product do not match!')