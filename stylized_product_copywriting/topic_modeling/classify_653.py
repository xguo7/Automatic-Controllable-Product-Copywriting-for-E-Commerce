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

def check_multi(tokens):
    topic_words=[['拍摄', '镜头', '后置', '拍照','三摄','四摄','人像','单摄','散热', '液冷'],
    ['运行', '麒麟', '处理器', '骁龙', '高通', '大容量'],
    ['电池', '续航',  '持久', '快充', '电量', '充电','闪充'],
    ['解锁', '指纹','隐私'],
    ['屏',  '视野', '英寸', '屏幕','全面','显示屏','显示'],
    ['5G', '双模','双卡'],
    ['材料','防水','进水','外观','机身']]
    count=0
    for topic in topic_words:
        for word in tokens:
            if word in topic:
                count+=1
                break       
    return count


def class_by_keyword(tokens):
    if len(set(['机身','外观','外壳']) & set(tokens))>0:
        a = 0
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
    elif len(set(['面容','解锁','指纹','人脸识别','面容ID']) & set(tokens))>0:
        a = 6                          
    else:
        a = -1
    return a 



#read data
path='/home/xiaojie.guo/daren_data/'
with open(path+'daren653_clean_sku.csv', 'r', encoding='utf-8') as f:
    orig_data=f.readlines()

workbook=openpyxl.load_workbook(path+'assigned_topic.xlsx')
topic_data=workbook.worksheets[0][1:]



len_=len(orig_data)
class_l=list(topic_data.rows)
new_origin=[]

if len(class_l)==len_:
    print('class and product match!')
        
    new_class_l=[]
    score_l=[]
    count=0
    for i in range(1,len_):
        orig_class=class_l[i][1].value
        orig_tokens=class_l[i][4].value
        tokens=set(re.split(",|'",orig_tokens[1:-1]))
            
        if check_multi(orig_tokens) <2 and len(orig_tokens)>5:
            new_origin.append(orig_data[i])
            score_l.append(class_l[i][2].value)
            c_k=class_by_keyword(tokens)
            if c_k >= 0:
                count+=1
                new_class_l.append(c_k)
                #print(orig_tokens+"by keywords: " +str(c_k))

            else:
                #print('again!')
                if orig_class in [11]:
                        new_class_l.append(0)

                if orig_class in [5,6,8]:
                        new_class_l.append(3) 

                if orig_class in [2]:
                        new_class_l.append(2)  

                if orig_class in [0,1,3,9]:
                        new_class_l.append(4)                                                      

                if orig_class in [4]:
                        new_class_l.append(1)             

                if orig_class in [10,7]:
                        new_class_l.append(5)
        

    final_class=[]
    #filter the low score (<0.5):
  

    for i in range(len(new_origin)):   
        item = new_origin[i]
        new_class = new_class_l[i]
        score = score_l[i]
        #print(item+str(new_class))
        if score>0.5:
            with open(path+'assigned_write_sku/assigned_write'+str(new_class)+'.txt', 'a', encoding='utf-8') as f:
                f.write(item[:-1]+'|||'+str(new_class)+'|||'+str(score)+'\n')
                final_class.append(new_class)

    ##统计各个类别的文案数目
    from collections import Counter
    print(Counter(final_class)) 
    print(count)
                            
else:
    print('class and product do not match!')
