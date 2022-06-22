import pandas as pd
import os

sec_cid = '1342'
orig_file='data_'+sec_cid+'_20211202_clean.csv'
orig_path='/mnt/10.252.199.12/home/xiaojie.guo/tmp/'+sec_cid+'_produce/orig_data/'+orig_file
#orig_path='/mnt/10.252.199.12/home/xiaojie.guo/daren_data/'+sec_cid+'/test.csv'

with open (orig_path,'r') as f:
    data_sku_prod = f.readlines()
    data_sku_prod = data_sku_prod[1:]

if sec_cid =='653':
    with open('/home/xiaojie.guo/Data/unilm_'+sec_cid+'/model.15.bin.test2') as f:
        data_write = f.readlines()
    num_aspect=7
    assert len(data_sku_prod)*num_aspect == len(data_write)
    list =['机身外观','屏幕音效','网络5g','拍照摄影','性能存储', '电池充电', '解锁识别']

elif sec_cid == '1343':
    with open('/home/xiaojie.guo/Data/unilm_'+sec_cid+'/model.14.bin.test2') as f:
        data_write = f.readlines()
    num_aspect=9
    assert len(data_sku_prod)*num_aspect == len(data_write)
    list =["面料材质", "细节（袖口)", "搭配方式", "风格气质", "细节（口袋)", "款式版型", "图案花纹", "细节（领口)", "细节（衣摆)"]

elif sec_cid == '1342':
    with open('/home/xiaojie.guo/Data/unilm_'+sec_cid+'/with_pretrain/bert_save_v4/model.100.bin.test2') as f:
        data_write = f.readlines() 
    num_aspect=8
    assert len(data_sku_prod)*num_aspect == len(data_write)
    list =["面料材质", "细节（袖口)", "搭配方式", "风格气质", "细节（口袋)", "款式版型", "图案花纹", "细节（领口)"]

elif sec_cid == '671':
    with open('/home/xiaojie.guo/Data/unilm_'+sec_cid+'/with_pretrain/bert_save_v4/model.100.bin.test2') as f:
        data_write = f.readlines()
    num_aspect=9
    assert len(data_sku_prod)*num_aspect == len(data_write)
    list =["性能存储", "显卡处理", "机身外观", "触控协同",  "屏幕摄像", "键盘音效", "解锁安全", "散热风扇", "续航充电"]

elif sec_cid == '1381':
    with open('/home/xiaojie.guo/Data/unilm_'+sec_cid+'/with_pretrain/bert_save_v4/model.100.bin.test2') as f:
        data_write = f.readlines()
    num_aspect=8
    assert len(data_sku_prod)*num_aspect == len(data_write)
    list =["防晒隔离", "抗皱紧致", "清洁控油", "美白淡斑",  "补水保湿", "修护舒缓", "成分质地", "包装设计"]    

elif sec_cid == '794':
    with open('/home/xiaojie.guo/Data/unilm_'+sec_cid+'/with_pretrain/bert_save_v4/model.100.bin.test2') as f:
        data_write = f.readlines()
    num_aspect=10
    assert len(data_sku_prod)*num_aspect == len(data_write)
    list =['除菌自洁', '容量多档', '去污烘干', '保鲜除霜', '画质音效', '制冷送风', '性能高效', '智能控制', '外观材质', '节能静音']   

result =[]
for i in range(len(data_write)):
    item = data_write[i].strip().replace(' ','')
    aspect = list[i%num_aspect]
    pred=item
    product=aspect+'|||'+data_sku_prod[int(i/num_aspect)].split('|||')[1].strip()
    sku=data_sku_prod[int(i/num_aspect)].split('|||')[0].strip() #for produce
    #product=aspect+'|||'+data_sku_prod[int(i/num_aspect)].split('\t')[0].strip()
    #sku=data_sku_prod[int(i/num_aspect)].split('\t')[-1].strip() #for develop
    result.append([pred, product, sku])
df=pd.DataFrame(result, columns=['pred','product','sku'])

if not os.path.exists('/mnt/10.252.199.12/home/xiaojie.guo/tmp/'+sec_cid+'_produce/generated_data/'):
   os.makedirs('/mnt/10.252.199.12/home/xiaojie.guo/tmp/'+sec_cid+'_produce/generated_data/')
   
df.to_csv('/mnt/10.252.199.12/home/xiaojie.guo/tmp/'+sec_cid+'_produce/generated_data/write_'+orig_file[5:-10]+'.csv')