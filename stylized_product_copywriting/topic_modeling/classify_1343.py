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
    topic_words=[['身材','宽松','比例','修身','版型'],
    ['百搭','搭','穿搭','搭配'],
    ['面料','布料','纯棉','亲肤','材质','手感','透气性','羊毛','毛呢','鸭绒','保暖','羽绒','鹅绒','填充'],
    ['格纹', '千鸟格','色','颜色','条纹','图案','印花','撞色','字母','竖纹'],
    ['立领','圆领','衣领','领','翻领','领口','字领','颈部','高领','颈','尖领','连帽','帽'],
    ['口袋','插手','插袋','开袋','贴袋','插兜','物品']]
    count=0
    for topic in topic_words:
        for word in tokens:
            if word in topic:
                count+=1
                break      
    return count


def class_by_keyword(tokens):
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



#read data
path='/home/xiaojie.guo/daren_data/'
with open(path+'daren1343_clean.csv', 'r', encoding='utf-8') as f:
    orig_data=f.readlines()[1:-1]

workbook1=openpyxl.load_workbook(path+'assigned_topic_1343_part1.xlsx')
workbook2=openpyxl.load_workbook(path+'assigned_topic_1343_part2.xlsx')
topic_data1=workbook1.worksheets[0]
topic_data2=workbook2.worksheets[0]


len_=len(orig_data)
class_l=list(topic_data1.rows)[1:]+list(topic_data2.rows)[1:]
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
                if orig_class in [0,2,6,11]:
                        new_class_l.append(0)

                if orig_class in [1]:
                        new_class_l.append(1) 

                if orig_class in [7,8]:
                        new_class_l.append(2)  

                if orig_class in [5]:
                        new_class_l.append(3)                                                      

                if orig_class in [10]:
                        new_class_l.append(5)             

                if orig_class in [12]:
                        new_class_l.append(6)

                if orig_class in [3,4,9]:
                        new_class_l.append(8)        

    final_class=[]
    #filter the low score (<0.5):
  

    for i in range(len(new_origin)):   
        item = new_origin[i].replace("#",'')
        new_class = new_class_l[i]
        score = score_l[i]
        #print(item+str(new_class))
        if score>0.6:
            with open(path+'assigned_write_1343/assigned_write'+str(new_class)+'.txt', 'a', encoding='utf-8') as f:
                f.write(item[:-1]+'|||'+str(new_class)+'|||'+str(score)+'\n')
                final_class.append(new_class)

    ##统计各个类别的文案数目
    from collections import Counter
    print(Counter(final_class)) 
    print(count)
                            
else:
    print('class and product do not match!')