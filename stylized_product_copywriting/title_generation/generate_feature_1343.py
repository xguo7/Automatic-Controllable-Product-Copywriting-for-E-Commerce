# this file is used to transform the final output file from copywriting part to generate the feature
import pandas as pd
import re



filename1= '/home/xiaojie.guo/daren_data/title_1343/validation.csv'
filename2= '/home/xiaojie.guo/daren_data/title_1343/train.csv'
filename3= '/home/xiaojie.guo/daren_data/title_1343/gpt_pw/gpt-Sep_21_19_43_24/model_epoch12/result_write_gpt_test_df/samples_{"mode": "beam", "beam_width": 3, "no_repeat_ngram_size": 3}.csv'

df1 = pd.read_csv(filename1)
df2 = pd.read_csv(filename2)
df3 = pd.read_csv(filename3)

brand_dic={}

for i in range(len(df1)):
    brand = df1['brand'][i]
    sku = df1['sku'][i]
    if sku not in brand_dic:
       brand_dic[sku]=brand

for i in range(len(df2)):
    brand = df2['brand'][i]
    sku = str(df2['sku'][i])
    if sku not in brand_dic:
       brand_dic[sku]=brand

    
def refine_feature(prod, feature):
    #去掉没有生成完整的
    if '(' in feature:
      feature=feature.split('(')[1]
    if "+" not in feature or len(feature.split("+"))>2:
      return ''
    if '[UNK]' in feature:
      return ''
    
    
    #检查商品词
    pw= feature.split('+')[1]
    if '鞋' in pw:
      return ''
    if pw in ['连衣','牛仔', '半身']:
       pw = pw+'裙'
    pw = pw.replace('群','裙')
    pw = pw.replace('袖','裙')   
    core_word = ['裤','裙','连衣裙','衬衫']
    for w in core_word:
     if w in pw and w not in prod:
       return ''     

  
    #检查修饰词
    subj = feature.split('+')[0]
    if len(subj)>7:
      subj=''
    check = ['】','【','）','（']
    for c in check:
       if c in subj:
         subj = ''

    if len(subj)>0:
      return subj+' '+pw
    else: 
      return pw
  


with open('/home/xiaojie.guo/tmp/uniLM_write_title_1343.csv', 'w', encoding =' utf-8') as f:
  for i in range(len(df3)):
    sku = str(df3['sku'][i])
    feature= df3['pred'][i]
    write = df3['sku_title_write'][i].split('+')[0]
    prod = df3['sku_title_write'][i].split('+')[1]
    if sku in brand_dic and pd.isnull(feature) is False:
      brand = brand_dic[sku]
      feature= refine_feature(prod, feature) 
      if len(feature)>0:
        title = brand+' '+feature
        f.write(sku+'|||'+title+'|||'+write+'|||'+prod+'\n')

