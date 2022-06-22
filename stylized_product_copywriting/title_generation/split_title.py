import openpyxl
import random
import re
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl.worksheet.datavalidation import DataValidation
import numpy as np
import csv
import re




def build_data(data, path):
        with open(path,'w',encoding = 'utf-8') as f:
            csv_write = csv.writer(f, delimiter='\t')
            csv_head = ["article_id","sku", "write_product","title"]
            csv_write.writerow(csv_head)
            id=0
            for item in data:
               item=item.split('|||')
               sku_id = item[0]
               write_product = item[1].replace(' ','')
               title=item[2][:-1]
               write_product =  re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】[，|。|；|！]*", "", write_product)
               if len(write_product)==0:
                   print(id)
               item_list=[id, sku_id, write_product, title]
               csv_write.writerow(item_list)
               id+=1


path = '/home/xiaojie.guo/daren_data/794/'

'''
#prepare data for each topic
for i in range(7):
        with open(path+'assigned_write/assigned_write'+str(i)+'.txt', encoding='utf-8') as f:
            data=f.readlines()
            random.shuffle(data)   
            l = len(data)
            build_data(data[:int(0.1*l)],path+'topic'+str(i)+'.csv')
'''
#prepare train, validation, test for all the data

with open(path+'daren794_clean_title.csv', encoding='utf-8') as f:
            data=f.readlines()
            random.shuffle(data)   

l = len(data)
print(l)
build_data(data[:int(0.9*l)],path+'train_title.csv')
build_data(data[int(0.9*l):int(0.95*l)],path+'eval_title.csv')
build_data(data[int(0.95*l):],path+'test_title.csv')
#build_data(all_data,path+'processed_daren1342_sku.csv')



print('finish spliting!')