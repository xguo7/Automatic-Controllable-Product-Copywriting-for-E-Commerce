#this file is used to detect and filter the generated write
#then the write of each aspect of the same product will be aggreagted together

import time
import re
from types import DynamicClassAttribute
from utils import *
from filter_rules import filter_part_1342, filter_part_653, filter_part_1343, filter_part_671, filter_part_1381, filter_part_794
import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--task", type=str, default="aggreagte",required=True)
parser.add_argument("--sec_id", type=str, default="671",required=True)
parser.add_argument("--data_path", type=str, default="clean_write.csv",required=True)
parser.add_argument("--save_path", type=str, default="aggregated_write.csv",required=True)
parser.add_argument("-n", type=int, default=1, help="process num to use")
parser.add_argument('--lda_model_name', default='model_lda', type=str, required=False, help='lda model path')
parser.add_argument('--lda_dct_path', default='/home/xiaojie.guo/daren_data/lda_dic', type=str, required=False, help='lda dct path')

args = parser.parse_args()

def if_match(number, product):
    prod = product.lower()
    for num in number:
      if num not in prod:
         return False
    return True


def filter_part():
    '''detect and filter the generated write for each aspect of each product
    require the input is .csv or txt with format of "sku|||product|||pred'''
    data=load_csv_sku_aspect(args.data_path)       
    print(str(len(data))+' data is loaded!')
    data_list = split_data(data, args.n)
    data_list = [(i,) for i in data_list]
    if args.sec_id == '653':
         res = multi_process_run(data_list, filter_part_653, args.n)
    if args.sec_id == '1343':
         res = multi_process_run(data_list, filter_part_1343, args.n)   
    if args.sec_id == '1342':
         res = multi_process_run(data_list, filter_part_1342, args.n)  
    if args.sec_id == '671':
         res = multi_process_run(data_list, filter_part_671, args.n)
    if args.sec_id == '1381':
         res = multi_process_run(data_list, filter_part_1381, args.n)
    if args.sec_id == '794':
         res = multi_process_run(data_list, filter_part_794, args.n)
    #print(len(res))
    save_data = []
    for part_res in res:
        save_data += part_res
        
    print('total qualified writes: '+str(len(save_data)))      
    with open(args.save_path, 'w', encoding='utf-8') as f:
        for item in save_data:
            f.write(item+'\n')   


 

def group_data(data):
    new_data = []
    current_prod = ''
    current_write = []
    current_sku = ''
    for item in data: 
        if item.split('|||')[2] == current_prod:
            current_write.append(item.split('|||')[3])
        else:
            if len(current_prod)>0:
                new_data.append([current_sku, current_prod, current_write])
            current_prod = item.split('|||')[2]
            current_sku = item.split('|||')[0]
            current_write = []
            current_write.append(item.split('|||')[3])
    new_data.append([current_sku, current_prod, current_write])      #put the last one into new data 
    return new_data


def remove_deplicate(sents):
    record = []
    new_sents=[]
    for i in range(len(sents)):
        sent_l=sents[i].split('，')
        new_sent_l=[]
        for sent in sent_l:
            if sent not in record:
                new_sent_l.append(sent)
                record.append(sent)
        new_sents.append('，'.join(new_sent_l))    
    return new_sents            


def aggregate_(data):
    np.random.seed(0)
    p= np.array([0.9, 0.06, 0.04]) #the probability of each connector
    connector_l = ['。','，','；'] # the list of possible connector
    new_data = []
       
    for i in range(len(data)):       
        prod = data[i][1]
        write = data[i][2]
        sku = data[i][0]
        #choose a connecter:
        connector = np.random.choice(connector_l, p = p.ravel())
        #find the first sentence
        if args.sec_id == '653':
              first_patterns = ["\w+出品\w+，", "^这款手机", "^这款产品", "^手机","该手机"]
        elif args.sec_id == '1343':      
              first_patterns = ["^这款\w+[采｜选]用"]
        elif args.sec_id == '1342':
              first_patterns = ["^这款\w+"]
        elif args.sec_id == '671':
              first_patterns = ["\w+出品\w+，", "^这款", "^笔记本","^该", "^此款"]
        elif args.sec_id == '1381':
              first_patterns = ["^这款", "^该", "^此款","^这个"]        
        elif args.sec_id == '794':
              first_patterns = ["^这款", "^该"]   
        first_sent = []
        inner_sent = []
        others = []
        
        for sent in write:
            key = 0
            #check if first sentence
            for pattern in first_patterns:
                #print(re.findall(p, sent))
                if len(re.findall(pattern, sent))>0:
                    key =1 #indicate this sentence has been dealt with
                    
                    if len(first_sent) == 0:
                        first_sent.append(sent)                      
                    else:
                        sent = re.sub(pattern, "", sent)
                        others.append(sent) 
                    #break
            #check if the inner sent
            if key == 0: 
                if "此外" in sent or "还有" in sent or "同时" in sent or "另外" in sent or \
                    '还' in sent or '可以' in sent:
                    inner_sent.append(sent)
                else:
                    others.append(sent)
        #结合几个句子
        all_sent = first_sent+others+inner_sent
        #print(all_sent)
        if len(all_sent) < 3 :
                    all_sent=remove_deplicate(all_sent)
                    new_write = connector.join(all_sent)+'。'
                    if len(new_write)>55:
                        new_data.append(sku+'|||'+new_write+'|||'+prod)     
        else:        
            if len(all_sent) == 3 :
                     option2 = [(0,1,2)]
            elif len(all_sent) == 4:
                     option2 = [(0,1,3), (1,2,3)]
            elif len(all_sent) == 5:
                     option2 = [(0,2,4), (1,3,4)]
            elif len(all_sent) == 6:
                     option2 = [(0,3,5), (1,2,4)]
            elif len(all_sent) == 7:
                     option2 = [(0,1,5), (1,2,4), (2,5,4)]
            elif len(all_sent) == 8:
                     option2 = [(0,2,6), (1,4,7), (1,3,5)]

            for option in option2:
                selected_sent = [all_sent[option[0]],all_sent[option[1]],all_sent[option[2]]]
                new_write = connector.join([selected_sent[0],selected_sent[1],selected_sent[2]])+'。'
                if len(new_write)>100:
                    new_write = connector.join([selected_sent[0],selected_sent[1]])+'。'
                if len(new_write)>55:    
                    new_data.append(sku+'|||'+new_write+'|||'+prod)                                                                  

    return new_data   


def aggregate(): 
    '''put the write of the different aspect from the same input into one sentence
    require the input document is .csv with format of "sku|||aspect|||product|||pred"
    '''

    data = load_txt(args.data_path)
    data = group_data(data)  #group the write for the same product into one data
    data_list = split_data(data, args.n)
    data_list = [(i,) for i in data_list]
    res = multi_process_run(data_list, aggregate_, args.n)
    save_data = []
    for part_res in res:
        save_data += part_res
        
    print('total qualified writes: '+str(len(save_data)))      

    result = pd.DataFrame(columns = ('product', 'write', 'sku'))
    for i in range(len(save_data)):
        item= save_data[i].split('|||')
        sku = item[0]
        product = item[2]
        write = item[1]
        sku_title_write = write + '+' + product
        result=result.append(pd.DataFrame({'sku':[sku],'product':[product], 'write':[write], 'sku_title_write':[sku_title_write]}))
    result.to_csv(args.save_path, sep= ',', index = False)  

    




 


def main():
    if args.task == "filter_part":
        filter_part()
    elif args.task == "aggregate":
        aggregate()       
    else:
        raise NotImplementedError()


if __name__ == "__main__":
    a = time.time()
    main()
    a = time.time() - a 
    print("Finished: " + str(a) + "s") 