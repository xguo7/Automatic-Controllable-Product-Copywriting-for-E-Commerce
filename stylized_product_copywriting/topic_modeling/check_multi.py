import jieba
import re




def check_multi(write):
    topic_words=[['拍摄', '镜头', '后置', '拍照','三摄','四摄','人像','单摄'],
    ['运行', '麒麟', '处理器', '骁龙', '高通'],
    ['电池', '续航', '大容量',  '持久', '快充', '电量', '充电','闪充'],
    ['解锁', '指纹','隐私'],
    ['屏', '机身', '视野', '英寸', '画面','屏幕','全面','显示屏','显示','材料','防水','进水','外观'],
    ['5G', '双模','双卡'],
    ['散热', '液冷']]
    count=0
    write=list(jieba.cut(write, HMM=True))
    for topic in topic_words:
        for word in write:
            if word in topic:
                count+=1
                break       
    return count

                        
'''
topic_count={}
for i in range(10):
   topic_count[i]=0

with open('split_write.txt', 'r', encoding='utf-8') as f:
    data=f.readlines()

new_data=0
for item in data:
    #write=re.split('。|；|！',item)[1:-1]
    write=re.split('。|；|！',item)
    for sent in write:
        new_data+=1
        num_topic=check_multi(sent)
        topic_count[num_topic]+=1
        if num_topic==0:
            with open('num_topic_0.txt', 'a', encoding='utf-8') as f:
                      f.write(sent+'\n')
        if num_topic==2:
            with open('num_topic_2.txt', 'a', encoding='utf-8') as f:
                      f.write(sent+'\n')     
        if num_topic==3:
            with open('num_topic_3.txt', 'a', encoding='utf-8') as f:
                      f.write(sent+'\n')                        

 

print(new_data)    
print(topic_count)'''
