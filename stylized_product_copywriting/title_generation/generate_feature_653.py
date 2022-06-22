# this file is used to transform the final output file from copywriting part to generate the feature
import pandas as pd
import re
from sklearn.utils import shuffle



filename1= '/home/xiaojie.guo/tmp/unilm_final_653_sku_new.csv'
filename2= '/home/xiaojie.guo/tmp/unilm_write_title_653_sku.csv'
df1 = pd.read_csv(filename1)
df2 = pd.read_csv(filename2)
df2 = df2.sample(frac=1).reset_index(drop=True)

prod_dic={}
for i in range(len(df1)):
    prod = df1['product'][i]
    sku = df1['sku'][i]
    if sku not in prod_dic:
       prod_dic[sku]=prod

def get_brand(prod):
  prod=re.sub(u'\\（.*?）|\\【.*?】', "", prod)
  brand = prod.split(',')[0]
  if len(brand)>6:
    brand=brand[:2]
  return brand
    
def refine_feature(prod, feature):
    #检查中心词， 是否是5g
    pw= feature.split('+')[1]
    if pw == '5g手机' and '不支持5g' in prod:
       pw = '手机'
  
    #检查修饰词
    subj = feature.split('+')[0]
    pattern_list = [['[三|双|单｜四]摄'], ['[曲｜全]面屏'], ['\d+\.?\d*nm'], ['\d+\.?\d*万'], ['\d+\.?\d*英寸'], ['\d+\.?\d*[w|W|瓦]'],['\d+\.?\d*[h|H][Z|z]'],['\d+\.?\d*[m|M][a|A][h|H]', '\d+\.?\d*毫安']]
    for pattern_l in pattern_list:
        subj_get = []
        prod_get = []
        for pattern in pattern_l:
                  subj_get.extend(re.findall(pattern, subj))
                  prod_get.extend(re.findall(pattern, prod))
        if len(subj_get)>0 and len(prod_get)>0:
                  subj = subj.replace(subj_get[0], prod_get[0]) 
    #删掉字母数字组合如果产品里面没有
    word = re.findall('^[A-Za-z][A-Za-z\d]{0,11}', subj)
    if len(word)> 0:
      if word[0] not in prod and 'oled' not in word[0]:
         subj = subj.replace(word[0],'')
  
    if len(subj)>1:
      return subj+' '+pw
    else: 
      return pw
  



with open('/home/xiaojie.guo/tmp/generation_653_sku.txt', 'w', encoding =' utf-8') as f:
  for i in range(len(df2)):
    sku = df2['sku'][i]
    prod = prod_dic[sku]
    feature= df2['pred'][i]
    write = df2['write'][i]
    brand = get_brand(prod)
    feature= refine_feature(prod, feature) 
    title = brand+' '+feature
    f.write(str(sku)+'\t'+title+'\t'+write+'\n')


