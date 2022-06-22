#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 13:22:12 2021

@author: xiaojie.guo
"""

import time
import re
from types import DynamicClassAttribute
from args_parser import args
from utils import *
import jieba
from pattern import check_topic, check_split

#delimiters = ["！", "。", "；"]
regexPattern = '|'.join(map(re.escape, args.delimiters))


def remove_useless(d):
        return d[0:4] + [d[6]]+d[7].split('|') +[d[24].split('|||')[0]]+d[20:21]+d[17:18] + d[-2:]

def unify_pattern(d):
    new_d=[]
    for item in d:
       items=item.split('\t') 
       if check_topic(items[-1]) is True:
           items[-1]='。'.join(items[-1].split('。')[1:])
           new_d.append('\t'.join(items))
       elif check_split(items[-1]) is True:
           new_d.append(item)
    return new_d


def split_(d):
    res = []
    for i in d:
        d_list = i.split('\t')
        d_list = remove_useless(d_list)
        cw = d_list[-1]
        cw = re.split(regexPattern, cw)
        if (cw[-1] == ''):
            cw = cw[:-1]
        d_list[-1] = cw
        res.append(d_list)
    return res


def split():
    '''
    split copywriting with "！", "。" and "；"
    '''
    data = load_txt(args.data_path)
    data=unify_pattern(data)
    print(len(data))

    if args.debug > -1:
        data = data[:args.debug]
    data_list = split_data(data, args.n)
    data_list = [(i,) for i in data_list]
    res = multi_process_run(data_list, split_, args.n)
    save_data = []
    for part_res in res:
        save_data += part_res
    
    print(len(save_data))
    c=0
    with open(args.save_path, "w", encoding="utf8") as f:
        for line in save_data:
            for item in line[-1]:
                #print(line)
                #print(item)
                c+=1
                f.write("\t".join(line[:-1]+[item])+'\n')
    print('total item: '+str(c))
                
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
        if '官网' in element or '其它' in element or '（' in element  or '(' in element:
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
        elements=item.split('\t')
        sku = elements[0]    
        #print(sku)
        write = elements[-1].replace('#','')
        #print(write)
        if len(write)!=0:
            #clean_write=' '.join(jieba.cut(write, HMM=True))
            prod_desc=','.join(elements[1:-5])      #title, memory, color 
            prod_desc= prod_desc.replace(' ', ',')
            attr=extract_attr(elements[-4]+elements[-3]+elements[-5])               
            #clean_prod=' '.join(jieba.cut(prod_desc+attribute, HMM=True))  
            clean_prod = prod_desc+attr
            
            clean_data.append(sku+'|||'+clean_prod+'|||'+write) #
    
    return clean_data


                
def clean():
    '''
    clean the data for the final use
    the input data should be the splitted data files
    '''
    
    data=load_txt(args.data_path)       
   
    data_list = split_data(data, args.n)
    data_list = [(i,) for i in data_list]
    res = multi_process_run(data_list, clean_, args.n)
    save_data = []
    for part_res in res:
        save_data += part_res
    save_data=list(set(save_data))    
    print('total daren writes: '+str(len(save_data)))      
    with open(args.save_path, 'w', encoding='utf-8') as f:
        for item in save_data:
            f.write(item+'\n')   
    
def clean_with_title_(data):
    clean_data=[]
    for item in data:
        elements=item.split('\t')
        sku = elements[0]    
        #print(sku)
        write = elements[-1].replace('#','')
        title = elements[-2]
        #print(write)
        if len(write)!=0 and len(title.split(' '))==3:
            #clean_write=' '.join(jieba.cut(write, HMM=True))
            prod_desc=','.join(elements[1:-5])      #title, memory, color 
            prod_desc= prod_desc.replace(' ', ',')
            attr=extract_attr(elements[-4]+elements[-3]+elements[-5])                
            #clean_prod=' '.join(jieba.cut(prod_desc+attribute, HMM=True))  
            clean_prod = prod_desc+attr
            title = '+'.join(title.split(' ')[1:])
            write_prod = write+'。+'+clean_prod
            clean_data.append(sku+'|||'+write_prod+'|||'+title) #
    
    return clean_data

    
                
def clean_with_title():
    '''
    clean the data for the final use
    the input data should be the splitted data files
    '''
    
    data=load_txt(args.data_path)       
   
    data_list = split_data(data, args.n)
    data_list = [(i,) for i in data_list]
    res = multi_process_run(data_list, clean_with_title_, args.n)
    save_data = []
    for part_res in res:
        save_data += part_res
    save_data=list(set(save_data))    
    print('total daren writes: '+str(len(save_data)))      
    with open(args.save_path, 'w', encoding='utf-8') as f:
        for item in save_data:
            f.write(item+'\n')   
def main():
    if args.task == "split":
        split()
    elif args.task == "clean":
        clean()
    elif args.task == "get_attr":
        get_atributes()   
    elif args.task == "clean_with_title":
        clean_with_title()             
    else:
        raise NotImplementedError()


if __name__ == "__main__":
    a = time.time()
    main()
    a = time.time() - a 
    print("Finished: " + str(a) + "s") 


 
  