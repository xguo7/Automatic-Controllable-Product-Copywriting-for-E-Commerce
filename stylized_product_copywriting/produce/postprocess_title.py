# this file is used to transform the final output file from copywriting part to generate the feature
import pandas as pd
import re
from sklearn.utils import shuffle
import random
from title_rules import refine_feature_1343, refine_feature_653

def get_brand(prod):
  prod=re.sub(u'\\（.*?）|\\【.*?】', "", prod)
  brand = prod.split(',')[0]
  if len(brand)>6:
    brand=brand[:2]
  return brand


sec_cid = '1343'
date='20211013'

filename1= '/home/xiaojie.guo/tmp/'+sec_cid+'_produce/generated_data/write_'+sec_cid+'_'+date+'_final.csv'
filename2= '/home/xiaojie.guo/tmp/'+sec_cid+'_produce/generated_write_title/write_title_'+sec_cid+'_'+date+'.csv'
filename3= '/home/xiaojie.guo/tmp/1343_produce/orig_data/data_1343_20211030.csv'
df1 = pd.read_csv(filename1)
df2 = pd.read_csv(filename2)
df2 = df2.sample(frac=1).reset_index(drop=True)


brand_dic={}
with open(filename3, 'r') as f:
  data=f.readlines()
for i in range(len(data)):
    brand = data[i].split('\t')[3].split('（')[0]
    sku = data[i].split('\t')[0]
    if sku not in brand_dic:
       brand_dic[sku]=brand

prod_dic={}
for i in range(len(df1)):
    prod = df1['product'][i]
    sku = df1['sku'][i]
    if sku not in prod_dic:
       prod_dic[sku]=prod


    

with open('/home/xiaojie.guo/tmp/'+sec_cid+'_produce/generation_'+sec_cid+'_'+date+'.txt', 'w', encoding =' utf-8') as f:
  for i in range(len(df2)):
    sku = df2['sku'][i]
    prod = prod_dic[sku]
    feature= df2['pred'][i]
    
    if "+" in feature:
      if sec_cid=='1343':
          write = df2['sku_title_write'][i].split('+')[0]
          brand = brand_dic[str(sku)]
          feature= refine_feature_1343(prod, feature, write) 
      elif sec_cid == '653':
          write = df2['write'][i]
          brand = get_brand(prod)
          feature= refine_feature_653(prod, feature, write)

      title = brand+' '+feature
      f.write(str(sku)+'\t'+title+'\t'+write+'\n')


