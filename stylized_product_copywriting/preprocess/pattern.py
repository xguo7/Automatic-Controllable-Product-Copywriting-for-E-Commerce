from os import WIFCONTINUED
import re

def check_len(topic):
    items=topic.split('，')
    c=0
    for s in items:
        if len(s)>9:
            c+=1
    if c==0:
        return True
    else: 
        return False

def check_topic(write):
        topic=write.split('。')[0]
        if len(re.split('，|、', topic))<4 and check_len(topic) is True:
            return True
        else:
            return False

def check_split(write):
    if len(re.split('；|。|！' ,write))>1:
        return True
    else:
        return False



'''
with open('653.csv', encoding='utf-8') as f:
    data=f.readlines()

#统计小标题  
topic_write=[]  
whole_write=[]
split_write=[]
for  item in data:
    write=item.split('\t')[2]
    if check_topic(write) is True:
        topic_write.append(write)
    elif len(re.split('；|。|！' ,write))>1:
        split_write.append(write)
    else:
        whole_write.append(write)

#print(len(topic_write))
#with open('topic_write.txt','w', encoding='utf-8') as f:
#   for topic in topic_write:
#     f.write(topic+'\n')

print(len(split_write))
with open('split_write.txt','w', encoding='utf-8') as f:
   for item in split_write:
     f.write(item+'\n')

print(len(whole_write))
with open('whole_write.txt','w', encoding='utf-8') as f:
   for item in whole_write:
     f.write(item+'\n')    

'''