from logging import error
import re
from gensim.models.ldamulticore import LdaMulticore
from gensim.test.utils import datapath
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
import time
import re
from types import DynamicClassAttribute
from utils import *
import argparse

def if_match(number, product):
    prod = product.lower()
    for num in number:
      if num not in prod:
         return False
    return True

def filter_part_671(data):
    clean_data=[]
   
    for item in data:
        write = item.split('|||')[2]
        aspect = item.split('|||')[0]#code_dic[item.split('|||')[0]]
        product = item.split('|||')[1]
        sku = item.split('|||')[3]
        #print(sku)
        #delete 【**】
        write = re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】[，|。|；|！]*", "", write)
        if len(write)>30:
            continue


        #check if match with input
        #check 5G
        if ('独立显卡' in write.lower() or  '独显' in write.lower()) and ('独立显卡' not in product.lower() or  '独显' not in product.lower()):
            continue
        #check无线充电
        for term in ['i3','i5','i7','i9']:
          if term in write.lower() and term not in product.lower():     
              continue


        if '核心' in write.lower():
            write.replace('核心','核')
        if 'whr' in write.lower():
            write.replace('whr','wh')            

        #check 摄影 屏幕频率 电池电量  充电瓦数 屏幕尺寸 像素 机身厚度
        pattern_list = [['[单｜双｜六｜八｜四]核','\d+\.?\d*核'], ['\d+\.?\d*nm'], ['\d+\.?\d*级压'], \
            ['\d+\.?\d*万'], ['\d+\.?\d*英寸'], ['\d+\.?\d*[w|W|瓦]'],['\d+\.?\d*[h|H][Z|z]'],['\d+\.?\d*[m|M][a|A][h|H]', '\d+\.?\d*毫安'],\
            ['\d+\.?\d*k'], ['\d+\.?\d*g[h|H][Z|z]'], ['\d+\.?\d*kg','\d+\.?\d*千克'],['\d+\.?\d*[W|w][H|h]'],['\d+\.?\d*毫米'],['[g|G|R|r][T|t][X|x]\d+\.?\d*']]
        for pattern_l in pattern_list:
            write_get = []
            prod_get = []
            for pattern in pattern_l:
                write_get.extend(re.findall(pattern, write))
                prod_get.extend(re.findall(pattern, product))
            if len(write_get)>0 and len(prod_get)>0:
                write = write.replace(write_get[0], prod_get[0])  


        #check number
        number = re.findall(r"\d+\.?\d*[a-z]*",write.lower())
        if len(number)>0 and not if_match(number, product):
            continue           

        clean_data.append(sku+"|||"+aspect+"|||"+product+"|||"+write)
    return clean_data


def filter_part_653(data):
    clean_data=[]   
    for item in data:
        
        write = item.split('|||')[2]
        aspect = item.split('|||')[0]#code_dic[item.split('|||')[0]]
        product = item.split('|||')[1]
        sku = item.split('|||')[3]
        

        #delete 【**】
        write = re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】[，|。|；|！]*", "", write)


        #check if match with input
        #check 5G
        if '5g' in write.lower() and '不支持5g' in product.lower():
            continue
        #check无线充电
        if '无线' in write.lower() and '不支持无线充电' in product.lower():     
            continue

        #check 摄影 屏幕频率 电池电量  充电瓦数 屏幕尺寸 像素 机身厚度
        pattern_list = [['[三|双|单｜四]摄'], ['\d+\.?\d*nm'], ['\d+\.?\d*万'], ['\d+\.?\d*英寸'], ['\d+\.?\d*[w|W|瓦]'],['\d+\.?\d*[h|H][Z|z]'],['\d+\.?\d*[m|M][a|A][h|H]', '\d+\.?\d*毫安']]
        for pattern_l in pattern_list:
            write_get = []
            prod_get = []
            for pattern in pattern_l:
                write_get.extend(re.findall(pattern, write))
                prod_get.extend(re.findall(pattern, product))
            if len(write_get)>0 and len(prod_get)>0:
                write = write.replace(write_get[0], prod_get[0])  


        #check number
        number = re.findall(r"\d+\.?\d*[a-z]*",write.lower())
        if len(number)>0 and not if_match(number, product):
            continue           

        clean_data.append(sku+"|||"+aspect+"|||"+product+"|||"+write)
    return clean_data    


def filter_part_1343(data):
    clean_data=[] 
    for item in data:
        write = item.split('|||')[2]
        aspect = item.split('|||')[0]#code_dic[item.split('|||')[0]]
        product = item.split('|||')[1]
        sku = item.split('|||')[3]

        #delete 【**】
        write = re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】[，|。|；|！]*", "", write)
        if len(write)>30:
            continue

        #check if the product support the aspect
        #check 袖口
        if aspect == '细节（袖口)':
            continue
        #check 口袋
        if aspect == '细节（口袋)' and '袋' not in product.lower() and '兜' not in product.lower():     
            continue
        #check 领口
        if aspect == '细节（领口)' and ('裙' in product.lower() or '裤' in product.lower()):        
            continue        
        
        #check if content match
        #check 图案印花
        if "a字" in write and ("A字" not in product or 'A版' not in product):
            continue
        #check 材质
        if "棉" in write and "棉" not in product:
            continue
        #check 图案花纹
        if "翻领" in write and "翻领" not in product:
            continue
        
        #print(aspect)
        write_l=[]
        prod_l=[]
        pattern = ['撞色', '条纹', '字母','印花','拼接' ,'格纹','千鸟格']
        for word in pattern:
            if word in write:
                write_l.append(word)
            if word in product:
                prod_l.append(word)
        if len(write_l)>1 and len(prod_l)>0:
            for i in range(len(write_l)):
                  if write_l[i] not in prod_l:
                     write.replace(write_l[i],'')
        if len(write_l)==1 and len(prod_l)>0 and write_l[0] not in prod_l:
                     write.replace(write_l[0],prod_l[0])
        if len(write_l)==1 and len(prod_l)==0:
                     continue                            
        
        clean_data.append(sku+"|||"+aspect+"|||"+product+"|||"+write)
    return clean_data 


def filter_part_1342(data):
    clean_data=[]

    for item in data:
        write = item.split('|||')[2]
        aspect = item.split('|||')[0]#code_dic[item.split('|||')[0]]
        product = item.split('|||')[1]
        sku = item.split('|||')[3]
        print(sku)
        #delete 【**】
        write = re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】[，|。|；|！]*", "", write)
        if len(write)>30:
            continue
        
        #check if the product support the aspect
        #check 袖口
        if aspect == '细节（袖口)':
            continue
        #check 口袋
        if aspect == '细节（口袋)' and '袋' not in product.lower() and '兜' not in product.lower():     
            continue
        #check 衣摆
        if aspect == '细节（衣摆)' and ('短袖' in product.lower() or '长袖' in product.lower() or '长袖' in product.lower() \
            or 't恤' in product.lower() or '裤' in product.lower()):        
            continue 
        #check 领口
        if aspect == '细节（领口)' and ('群' in product.lower() or '裤' in product.lower()):        
            continue        
        
        #check if content match
        #check 图案印花
        if "a字" in write and "a字" not in product:
            continue
        #check 材质
        if "棉" in write and "棉" not in product:
            continue
        #check 图案花纹
        if "翻领" in write and "翻领" not in product:
            continue
        if "纯色" in write and ('字母' in product or '印花' in product or '撞色' in product):
            continue
        if "连帽" in write and "连帽" not in product:
            continue
        if "抽绳" in write and "抽绳" not in product:
            continue   
        if "连帽" in write and "连帽" not in product:
            continue   
        if "绣花" in write and "绣花" not in product:
            continue              
        if "刺绣" in write and "刺绣" not in product:
            continue      
        
        write_l=[]
        prod_l=[]
        pattern = ['撞色', '条纹', '字母','印花','拼接' ,'格纹','千鸟格','logo','LOGO']
        for word in pattern:
            if word in write:
                write_l.append(word)
            if word in product:
                prod_l.append(word)
        if len(write_l)>1 and len(prod_l)>0:
            for i in range(len(write_l)):
                  if write_l[i] not in prod_l:
                     write.replace(write_l[i],'')
        if len(write_l)==1 and len(prod_l)>0 and write_l[0] not in prod_l:
                     write.replace(write_l[0],prod_l[0])
        if len(write_l)>=1 and len(prod_l)==0:
                     continue        

        #check 摄影 屏幕频率 电池电量  充电瓦数 屏幕尺寸 像素 机身厚度
        pattern_list = [['[黑|白|蓝|红|黄|纯|亮|绿|粉|灰|紫]色']]
        for pattern_l in pattern_list:
            write_get = []
            prod_get = []
            for pattern in pattern_l:
                write_get.extend(re.findall(pattern, write))
                prod_get.extend(re.findall(pattern, product))
            if len(write_get)>0 and len(prod_get)>0:
                write = write.replace(write_get[0], prod_get[0])  
            if len(write_get)>=1 and len(prod_get)==0:
                continue

        clean_data.append(sku+"|||"+aspect+"|||"+product+"|||"+write)
    return clean_data


def filter_part_1381(data):
    clean_data=[]

    for item in data:
        write = item.split('|||')[2]
        aspect = item.split('|||')[0]#code_dic[item.split('|||')[0]]
        product = item.split('|||')[1]
        sku = item.split('|||')[3]
        
        if '[UNK]' in write:
            continue
        if "这款" in write:
            write = '这款'+write.split('这款')[1]
        #delete 【**】
        write = re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】[，|。|；|！]*", "", write)
        if len(write)>30:
            continue

        #check if the product support the aspect
        #check 袖口
        if aspect == '防晒隔离':
            if '防晒' in write and '防晒' not in product:
               continue
        if aspect == '清洁控油':
            if '防晒' in product:
                continue
        if aspect == '补水保湿':
            if '防晒' in product:
                continue
        if aspect != '包装设计' and '设计' in write:
                continue
        if aspect == '抗皱紧致':
            if '洁面' in product:
                continue
        if aspect == '修护舒缓':
            if '洁面' in product:
                continue        
        #check if content match
        #check 图案印花
        if ("泡沫" in write or '洗面奶' in write) and "洁面" not in product:
            continue
             
        
        clean_data.append(sku+"|||"+aspect+"|||"+product+"|||"+write)
    return clean_data    


def filter_part_794(data):
    clean_data=[]
    error_c=0
    for item in data:
      try:
        write = item.split('|||')[2]
        aspect = item.split('|||')[0]#code_dic[item.split('|||')[0]]
        product = item.split('|||')[1]
        sku = item.split('|||')[3]
        #print(aspect)
        #delete 【**】
        write = re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】[，|。|；|！]*", "", write)
        if len(write)>30:
            continue
        
        #check if aspect match with product
        if aspect == '除菌自洁' or aspect == '容量多档':
            if '冰箱' not in product and '洗衣机' not in product and '冰柜' not in product:
               continue
        if aspect == '去污烘干':
            if '洗衣机' not in product:
               continue  
        if aspect == '保鲜除霜':
            if '冰箱' not in product and '冰柜' not in product:
               continue            
        if aspect == '画质音效':
            if '电视机' not in product:
               continue  
        if aspect == '制冷送风':
            if '冰箱' not in product and '冰柜' not in product and '空调' not in product:
               continue       
        

        #check if match with input
        if '℃' in write.lower() and '℃' not in product.lower():
            p = re.findall('\d+\.?\d*℃', write)
            write = write.replace(p, '') 
          

        #check 摄影 屏幕频率 电池电量  充电瓦数 屏幕尺寸 像素 机身厚度
        pattern_list = [['\d+\.?\d*公斤'], ['\d+\.?\d*℃'], ['\d+\.?\d*升','\d+\.?\d*L','\d+\.?\d*l'],['\d+\.?\d*毫米']]
        for pattern_l in pattern_list:
            write_get = []
            prod_get = []
            for pattern in pattern_l:
                write_get.extend(re.findall(pattern, write))
                prod_get.extend(re.findall(pattern, product))
            if len(write_get)>0 and len(prod_get)>0:
                write = write.replace(write_get[0], prod_get[0])  
        
        
        #check number
        number = re.findall(r"\d+\.?\d*[a-z]*",write.lower())
        if len(number)>0 and not if_match(number, product):
            continue           
        
        clean_data.append(str(sku)+"|||"+aspect+"|||"+product+"|||"+write)
        #print(sku+"|||"+aspect+"|||"+product+"|||"+write)
      except: error_c+=1
    print('error:'+str(error_c))
    print(len(clean_data))
    return clean_data
