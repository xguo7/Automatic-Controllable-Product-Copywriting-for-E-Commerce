#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 13:22:12 2021

@author: xiaojie.guo
"""

import time
import re
from types import DynamicClassAttribute
from multiprocessing import Pool
import pandas as pd

#delimiters = ["！", "。", "；"]
#regexPattern = '|'.join(map(re.escape, args.delimiters))

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

def multi_process_run(arg_list, fun, n_process=4):
    pool = Pool(processes=n_process)
    jobs = [pool.apply_async(fun, args=n) for n in arg_list]

    pool.close()
    pool.join()

    try:    # the fun doesn't have a non-None return value
        return [job.get() for job in jobs]
    except:
        return []


def split_data(data, n):
    l = len(data)
    sl = int(l / n)
    if sl*n != l:
        sl += 1
    data_list = []

    for i in range(0, l, sl):
        data_list.append(data[i:i+sl])
    return data_list

    
def contain_zh(word):
    '''
    判断传入字符串是否包含中文
    :param word: 待判断字符串
    :return: True:包含中文  False:不包含中文
    '''
    global zh_pattern
    match = zh_pattern.search(word)

    return match

def remove_useless(d):
    '''
    '商品sku编号','商品标题','商品描述','商品品牌名','cid1名称','cid2名称','cid3名称','广告词','尺寸','长','宽','高','计算体积',
   '颜色','重量（毫克）','属性组名','属性名', '属性值名','属性备注','属性名','属性值名','属性备注','修饰词', '产品词','商详页OCR'   
    '''
    if args.sec_cid in ['1343','1342']:
       return d[0:2] + [d[6]]+d[7].split('|')+d[20:21]+[d[24].split('|||')[0]]
    else:
       return d[0:3] + [d[6]]+d[7].split('|')+d[17:18]+d[20:21]+[d[24].split('|||')[0]]

                
def get_atributes():
   '''
   get the attributes name for topic selecting
   '''
   dic={}
   data = load_txt(args.data_path)
   for item in data:
       elements=item.split('\t')
       attr_name=elements[18].split('|||')+elements[19].split('|||')+elements[22].split('|||')
       clean_attr=list(set(attr_name))
       for word in clean_attr:
           if word in dic:
               dic[word]+=1
           else:
               dic[word]=0                    
   with open(args.save_path, "w", encoding="utf8") as f:
        for key in dic:
            f.write(key+': '+str(dic[key])+'\n')
   

def extract_attr(attr):
    attr=set(attr.split('|||'))
    new_attr=[]
    for element in attr:
        if '联通' in element or '电信' in element or '移动' in element or 'WCDMA' in element or 'GSM' in element or '年' in element or '其他' in element or 'MP4' in element or '个' in element or '月' in element or '色' in element:
           continue
        elif '官网' in element or '其它' in element or '（' in element  or '(' in element:
           continue 
        elif not contain_zh(element):
           continue 
        elif len(element)<2:
           continue
        new_attr.append(element)
    return ','.join(new_attr)

def clean_(data):
    clean_data=[]
    for item in data:
        try:
            elements = remove_useless(item.split('\t'))
            sku = elements[0]    
            prod_desc=elements[1]+elements[2]+elements[3]      #title, memory, color 
            prod_desc= prod_desc.replace(' ', ',')  
            if args.sec_cid in ['1343','1342']:
               attr=extract_attr(elements[4]+'|||'+elements[5])  
            else:         
               attr=extract_attr(elements[4]+elements[5]+'|||'+elements[6])  
            prod = prod_desc+attr.replace('/',',')
            clean_prod = re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】[，|。|；|！]*", "", prod)
            clean_prod=clean_prod.replace('\n','')
            clean_data.append(sku+'|||'+clean_prod) #
        except:
            print('error!')
    
    return clean_data
                
def main():
    '''
    clean the data for the final use
    the input data should be the splitted data files
    '''
    with open(args.data_path,'r') as f:
       data=f.readlines()

    data_list = split_data(data, args.n)
    data_list = [(i,) for i in data_list]
    res = multi_process_run(data_list, clean_, args.n)
    save_data = []
    for part_res in res:
        save_data += part_res
        
          
    save_data=list(set(save_data))
    print('total daren writes: '+str(len(save_data)))
    with open(args.save_path, 'w', encoding='utf-8') as f:
        f.write('sku'+'\t'+'product'+'\n')
        for item in save_data:
            f.write(item+'\n') 

    
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("sec_cid", type=str, help="second cid")
parser.add_argument("data_path", type=str, help="data path")
parser.add_argument("save_path", type=str, help="save path")
parser.add_argument("-n", type=int, default=8, help="process num to use")
parser.add_argument("--debug", type=int, default=-1, help="load little data")
parser.add_argument("--delimiters", type=list, default=["！", "。", "；"], help="load little data")

args = parser.parse_args()

if __name__ == "__main__":
    a = time.time()
    main()
    a = time.time() - a 
    print("Finished: " + str(a) + "s") 


 
  