import random
import re

def refine_feature_1343(prod, feature):
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
    if pw in ['连衣','牛仔', '半身']:
       pw = pw+'裙'
    pw = pw.replace('群','裙')
    pw = pw.replace('袖','裙')   
    if '件套' in prod or '套装' in prod:
       if ('套' not in pw or '两件' not in pw or '三件' not in pw):
           pw=pw+'套装'

    core_word = ['裤','裙','连衣裙','衬衫']
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
  

def refine_feature_653(prod, feature, write):

    #检查中心词， 是否是5g
    pw= feature.split('+')[1]
    if pw == '5g手机' and '不支持5g' in prod:
       pw = '手机'
    #检查是否为老人机
    if '老人手机' in prod:
       pw = '老人手机'
    #检查是否为套装
    if '套装' in prod:
      pw = '手机套装'
  
    #检查修饰词
    subj = feature.split('+')[0]
    #纠正修饰词
    pattern_list = [['[三|双|单｜四]摄'], ['[曲｜全]面屏']]
    for pattern_l in pattern_list:
        subj_get = []
        prod_get = []
        for pattern in pattern_l:
                  subj_get.extend(re.findall(pattern, subj))
                  prod_get.extend(re.findall(pattern, prod))
        if len(subj_get)>0 and len(prod_get)>0:
                  subj = subj.replace(subj_get[0], prod_get[0]) 
    #处理含有参数的修饰词
    #number_pattern_list = [['\d+\.?\d*nm'], ['\d+\.?\d*万'], ['\d+\.?\d*英寸'], ['\d+\.?\d*[w|W|瓦]'],['\d+\.?\d*[h|H][Z|z]'],['\d+\.?\d*[m|M][a|A][h|H]', '\d+\.?\d*毫安']]
    num_pattern = re.findall('\d+', subj)
    if len(num_pattern)>0:
            subj = ''
    #num_list=['单','双','三','四']
    #for num in num_list:
    #   if num in subj:
    #       subj =''

    #删掉字母数字组合如果产品里面没有
    word = re.findall('^[A-Za-z][A-Za-z\d]{0,11}', subj)
    if len(word)> 0:
      if word[0] not in prod and 'oled' not in word[0]:
         subj = subj.replace(word[0],'')
    
    if pw == '老人手机':
      subj='智能方便'
  
    candidate_subj=['高清拍摄','持久续航','闪充','轻薄','闪充', '高性能','指纹解锁','轻薄']  
    if len(subj)>1:
      return subj+' '+pw
    else:  #处理卖点缺失问题
      if '电' in write:
          return '闪充'+' '+pw
      elif '续航' in write:
          return '持久续航'+' '+pw
      elif '高清' in write:
          return '高清拍摄'+' '+pw 
      elif '屏' in write:
          return '高清屏'+' '+pw 
      elif '像素' in write:
          return '高像素'+' '+pw     
      elif '徕卡' in write:
          return '感光徕卡'+' '+pw                 
      else:         
          index = random.randint(0,len(candidate_subj)-1)
          return candidate_subj[index]+' '+pw