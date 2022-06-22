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
    topic_words=[['抗菌','防霉','杀菌','细菌','抑菌','螨虫','净味','除菌','自洁','擦洗'],
    ['存储空间','容量大','全家人','多人','全家','宽敞','容量','分区','空间'],
    ['污渍','洗涤','烘干','烘'],
    ['变质', '保鲜','风冷','无霜','新鲜','储鲜','出冰','结霜'],
    ['画面','画质','屏幕','分辨率','超高','图像','色彩','高清'],
    ['人体','送风','气流','无风感','头痛','直吹','风感','零风感'],
    ['性能','处理器','芯片','搭载','强劲','高效','动力'],
    ['语音','人工智能','AI','声控','编程','控温'],
    ['机身','外形','外观','纤薄','大气','时尚','工艺','质感','铝板'],
    ['节能','电','噪音','环保','绿色','静音','能耗','浪费','低耗','省']]
    count=0
    for topic in topic_words:
        for word in tokens:
            if word in topic:
                count+=1
                break      
    return count


def class_by_keyword(tokens):
    if len(set(['抗菌','防霉','杀菌','细菌','抑菌','螨虫','净味','除菌','自洁','擦洗','异味']) & set(tokens))>0:
        a = 0   
    elif len(set(['存储空间','容量大','全家人','多人','宽敞','容量','分区','空间','大容量']) & set(tokens))>0:
        a = 1
    elif len(set(['污渍','洗涤','烘干','烘']) & set(tokens))>0:
        a = 2
    elif len(set(['变质','保鲜','风冷','无霜','新鲜','储鲜','出冰','结霜']) & set(tokens))>0:
        a = 3
    elif len(set(['画面','画质','屏幕','分辨率','超高','图像','色彩','高清','音效','屏']) & set(tokens))>0:
        a = 4
    elif len(set(['人体','送风','气流','无风感','头痛','直吹','风感','零风感']) & set(tokens))>0:
        a = 5                          
    elif len(set(['性能','处理器','芯片','强劲','高效','动力']) & set(tokens))>0:
        a = 6     
    elif len(set(['语音','人工智能','AI','声控','编程','控温']) & set(tokens))>0:
        a = 7   
    elif len(set(['机身','外形','外观','纤薄','大气','时尚','工艺','质感','铝板']) & set(tokens))>0:
        a = 8 
    elif len(set(['节能','电','噪音','环保','绿色','静音','能耗','浪费','低耗','省','电费']) & set(tokens))>0:
        a = 9                                                    
    else:
        a = -1
    return a 



#read data
path='/home/xiaojie.guo/daren_data/794/'
with open(path+'daren794_clean.csv', 'r', encoding='utf-8') as f:
    orig_data=f.readlines()

workbook1=openpyxl.load_workbook(path+'assigned_topic_794_16class.xlsx')
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
                if orig_class in [7,14]:
                        new_class_l.append(0)

                if orig_class in [0,15]:
                        new_class_l.append(1) 

                if orig_class in [3,8]:
                        new_class_l.append(2)  

                if orig_class in [2]:
                        new_class_l.append(3)                                                      

                if orig_class in [4]:
                        new_class_l.append(4)             

                if orig_class in [5]:
                        new_class_l.append(5)

                if orig_class in [1,10]:
                        new_class_l.append(6)    

                if orig_class in [6,9,13]:
                        new_class_l.append(7)  

                if orig_class in [11]:
                        new_class_l.append(8)  

                if orig_class in [12]:
                        new_class_l.append(9)                                                  
    final_class=[]
    #filter the low score (<0.5):
  
    os.makedirs(path+'assigned_write_794/')
    for i in range(len(new_origin)):   
        item = new_origin[i].replace("#",'')
        new_class = new_class_l[i]
        score = score_l[i]
        #print(item+str(new_class))
        if score>0.65:
            with open(path+'assigned_write_794/assigned_write'+str(new_class)+'.txt', 'a', encoding='utf-8') as f:
                f.write(item[:-1]+'|||'+str(new_class)+'|||'+str(score)+'\n')
                #f.write(item.split('|||')[-1]+'\n')
                final_class.append(new_class)

    ##统计各个类别的文案数目
    from collections import Counter
    print(Counter(final_class)) 
    print(count)
                            
else:
    print('class and product do not match!')