# this file is used to transform the final output file from copywriting part to generate the feature
import pandas as pd
import re
from sklearn.utils import shuffle
import random

sec_cid='1342'
date='20211202'
prod_write_filename= '/mnt/10.252.199.12/home/xiaojie.guo/tmp/'+sec_cid+'_produce/generated_data/write_'+sec_cid+'_'+date+'_final.csv'
title_filename= '/home/xiaojie.guo/Data/unilm_'+sec_cid+'/title_with_pretrain/bert_save_v4/model.32.bin.test'
brand_filename= '/mnt/10.252.199.12/home/xiaojie.guo/tmp/'+sec_cid+'_produce/orig_data/data_'+sec_cid+'_'+date+'.csv'


    
def refine_feature_1342(prod, feature):
    #去掉没有生成完整的
    if '(' in feature:
      feature=feature.split('(')[1]
    if "+" not in feature or len(feature.split("+"))>2:
      return ''
    if '[UNK]' in feature:
      return ''
    sensitive_words = ['时尚', '百搭','鞋','】','【','）','（']
    for word in sensitive_words:
      if word in feature:
         return ''
    
    #检查商品词
    pw= feature.split('+')[1] 
    if '件套' in prod or '套装' in prod:
       if ('套' not in pw or '两件' not in pw or '三件' not in pw):
           pw=pw+'套装'

    core_word = ['裤','裙','衬衫']
    for w in core_word:
     if w in pw and w not in prod:
       return ''    
  
    #检查修饰词
    subj = feature.split('+')[0]
    if len(subj)>7:
      return ''
    if subj == pw or subj in pw:
      return ''

    if len(subj)>1:
      return subj+' '+pw
    else: 
      return ''
  

def refine_feature_671(prod, feature):
    #去掉没有生成完整的
    if '(' in feature:
      feature=feature.split('(')[1]
    if "+" not in feature or len(feature.split("+"))>2:
      return ''
    if '[UNK]' in feature:
      return ''
    sensitive_words = ['】','【','）','（']
    for word in sensitive_words:
      if word in feature:
         return ''
    
    #检查商品词
    pw= feature.split('+')[1] 
    if '套装' in prod:
           pw='电脑套装'

    #检查修饰词
    subj = feature.split('+')[0]
    if len(subj)>7:
       return ''
    if subj == pw or subj in pw:
       return ''
    num_pattern = re.findall('\d+', subj)
    if len(num_pattern)>0:
        subj = ''
    pattern_list = [['[单｜双｜六｜八｜四]核','\d+\.?\d*核']]
    for pattern_l in pattern_list:
        subj_get = []
        prod_get = []
        for pattern in pattern_l:
                  subj_get.extend(re.findall(pattern, subj))
                  prod_get.extend(re.findall(pattern, prod))
        if len(subj_get)>0 and len(prod_get)>0:
                  subj = subj.replace(subj_get[0], prod_get[0]) 

    if len(subj)>1:
      return subj+' '+pw
    else: 
      return ''


def refine_feature_1381(prod, feature):
    #去掉没有生成完整的
    if '(' in feature:
      feature=feature.split('(')[1]
    if "+" not in feature or len(feature.split("+"))>2:
      return ''
    if '[UNK]' in feature:
      return ''
    sensitive_words = ['】','【','）','（']
    for word in sensitive_words:
      if word in feature:
         return ''
    
    #检查商品词
    pw= feature.split('+')[1] 
    if '套装' in prod:
           pw=' 护肤套装'

    #检查修饰词
    subj = feature.split('+')[0]
    if len(subj)>7:
       return ''
    if subj == pw or subj in pw:
       return ''
    num_pattern = re.findall('\d+', subj)
    if len(num_pattern)>0:
        subj = ''

    if len(subj)>1:
      return subj+' '+pw
    else: 
      return ''

def refine_feature_794(prod, feature):
    #去掉没有生成完整的
    if '(' in feature:
      feature=feature.split('(')[1]
    if "+" not in feature or len(feature.split("+"))>2:
      return ''
    if '[UNK]' in feature:
      return ''
    sensitive_words = ['】','【','）','（']
    for word in sensitive_words:
      if word in feature:
         return ''
         
    pw= feature.split('+')[1] 
    if '套装' in prod:
           pw=' 家电套装'
    #检查修饰词
    subj = feature.split('+')[0]
    if len(subj)>7:
       return ''
    if subj == pw or subj in pw:
       return ''
    num_pattern = re.findall('\d+', subj)
    if len(num_pattern)>0:
        subj = ''

    if len(subj)>1:
      return subj+' '+pw
    else: 
      return ''

brand_dic={}
with open(brand_filename, 'r') as f:
  data=f.readlines()
for i in range(len(data)):
    #print(data[i].split('\t'))
    brand = data[i].split('\t')[3].split('（')[0]
    if brand=='完   美':
        brand='完美'
    sku = data[i].split('\t')[0]
    if sku not in brand_dic:
       brand_dic[sku]=brand


with open(title_filename) as f:
        data_title = f.readlines()

data_df = pd.read_csv(prod_write_filename)

assert len(data_df)==len(data_title)


result=[]
for i in range(len(data_df)):
    sku = data_df['sku'][i]
    write = data_df['write'][i]
    prod = data_df['product'][i]
    feature= data_title[i].strip().replace(' ','')   
    brand = brand_dic[str(sku)]
    if "+" in feature:
        if sec_cid == '1342':
             feature= refine_feature_1342(prod, feature) 
        elif sec_cid== '671':
             feature= refine_feature_671(prod, feature) 
        elif sec_cid== '1381':
             feature= refine_feature_1381(prod, feature)     
        elif sec_cid== '794':
             feature= refine_feature_794(prod, feature)                       
        if len(feature)>0 and len(feature.split(' '))==2:
          title = brand+' '+feature
          result.append(str(sku)+'\t'+title+'\t'+write+'\n')

with open('/mnt/10.252.199.12/home/xiaojie.guo/tmp/'+sec_cid+'_produce/generation_'+sec_cid+'_'+date+'.txt', 'w', encoding =' utf-8') as f:          
    random.shuffle(result)
    for item in result:
          f.write(item)


