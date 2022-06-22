import jieba
import numpy as np
# Plotting tools
#import pyLDAvis
#import pyLDAvis.gensim # don't skip this
import matplotlib.pyplot as plt
import os
#Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import openpyxl
import re

def check_multi(tokens):
    topic_words=[['防晒','紫外线','烈日','晒','高倍','UVB','UVA'],
    ['细纹','皱纹','抗皱','紧致','淡纹','提拉','轮廓'],
    ['清洁','黑头','粗大','控油','净化','污垢','净透','粉刺','洁净','祛痘','洁面'],
    ['美白', '祛斑','黑色素','色斑','肤色','提亮','焕白','亮白','淡斑'],
    ['补水','干燥','喝饱水','嘭','水润','干皮','水嫩','保湿','锁水','含水量','缺水'],
    ['修护','熬夜','脆弱','强韧','维稳','舒缓','敏感','受损','屏障'],
    ['质地','轻薄','刺激','味道','延展性','粘腻','流动性','轻盈']]
    count=0
    for topic in topic_words:
        for word in tokens:
            if word in topic:
                count+=1
                break      
    return count


def class_by_keyword(tokens):
    if len(set(['防晒','紫外线','烈日','晒','高倍','UVB','UVA']) & set(tokens))>0:
        a = 0   
    elif len(set(['细纹','皱纹','抗皱','紧致','淡纹','提拉','轮廓','唇纹','法令纹','抗老','初老']) & set(tokens))>0:
        a = 1
    elif len(set(['清洁','黑头','粗大','控油','净化','污垢','净透','粉刺','洁净','祛痘','洁面','卸妆']) & set(tokens))>0:
        a = 2
    elif len(set(['美白', '祛斑','黑色素','色斑','肤色','提亮','焕白','亮白','淡斑','透亮','白嫩','暗沉','亮度','色素','白皙']) & set(tokens))>0:
        a = 3
    elif len(set(['补水','干燥','喝饱水','嘭','水润','干皮','水嫩','保湿','锁水','含水量','缺水','水份','水分']) & set(tokens))>0:
        a = 4
    elif len(set(['修护','熬夜','脆弱','强韧','维稳','舒缓','敏感','受损','屏障','修复','平衡']) & set(tokens))>0:
        a = 5                          
    elif len(set(['质地','轻薄','刺激','味道','延展性','粘腻','流动性','轻盈','成分','植物','萃取','配方','蕴含']) & set(tokens))>0:
        a = 6     
    elif len(set(['包装','瓶身','压头','喷头','设计','携带','外观']) & set(tokens))>0:
        a = 7                                       
    else:
        a = -1
    return a 



#read data
path='/home/xiaojie.guo/daren_data/1381/'
with open(path+'daren1381_clean.csv', 'r', encoding='utf-8') as f:
    orig_data=f.readlines()

workbook1=openpyxl.load_workbook(path+'assigned_topic_1381_12class.xlsx')
topic_data1=workbook1.worksheets[0]


len_=len(orig_data)
class_l=list(topic_data1.rows)[1:]
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
                if orig_class in [6]:
                        new_class_l.append(0)

                if orig_class in [9]:
                        new_class_l.append(1) 

                if orig_class in [10]:
                        new_class_l.append(2)  

                if orig_class in [0]:
                        new_class_l.append(3)                                                      

                if orig_class in [1,7]:
                        new_class_l.append(4)             

                if orig_class in [2,3,11]:
                        new_class_l.append(5)

                if orig_class in [4,5,8]:
                        new_class_l.append(6)        

    final_class=[]
    #filter the low score (<0.5):
  
    os.makedirs(path+'assigned_write_1381/')
    for i in range(len(new_origin)):   
        item = new_origin[i].replace("#",'')
        new_class = new_class_l[i]
        score = score_l[i]
        #print(item+str(new_class))
        if score>0.65:
            with open(path+'assigned_write_1381/assigned_write'+str(new_class)+'.txt', 'a', encoding='utf-8') as f:
                f.write(item[:-1]+'|||'+str(new_class)+'|||'+str(score)+'\n')
                final_class.append(new_class)

    ##统计各个类别的文案数目
    from collections import Counter
    print(Counter(final_class)) 
    print(count)
                            
else:
    print('class and product do not match!')