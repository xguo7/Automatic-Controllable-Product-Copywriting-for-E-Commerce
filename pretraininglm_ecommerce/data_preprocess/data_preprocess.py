import os
import pandas as pd
import numpy as np
from collections import defaultdict
import random


## 读取并合并下载后的数据
## data_dir, 文件夹路径
## folder_name, 当前选择的数据的文件夹名称
## n = -1， 读取文件夹内全部文件，可以设置n为比较小的数值做测试
def get_df(data_dir, folder_name, n = 2):
    file_list = [os.path.join(data_dir,  folder_name ,x) for x in os.listdir(os.path.join(data_dir,  folder_name)) if 'part' in x]
    if n > 0:
        file_list = file_list[:n]
    df_all = []
    for filename in file_list:
        try:
            df = pd.read_csv(filename, sep = '\t',encoding='utf8', header = None)
            df_all.append(df)
            print(len(df))
        except:
            pass
    df_info = pd.concat(df_all, axis = 0)
    with open(os.path.join(data_dir,  folder_name, 'head.txt'), 'r') as f:
        x = f.read()
    header = [ a for a in x.split('\n') if len(a) > 0]
    df_info.columns = header
    return df_info
## df_ocr_info.tsv生成过程，可在pretrain数据目录下找到该文件
def preprocess_ocr(df_ocr):
    ocr_info_list = []
    df_tmp = df_ocr[~df_ocr['ocr'].isna()]
    for i in range(len(df_tmp)):
    # for i in range(20):
        if i%50000 == 1:
            print(i)
            if len(ocr_info_list) > 0:
                df_ocr_info = pd.DataFrame(ocr_info_list)
                df_ocr_info.columns = ['sku','ocr_merge']
                df_ocr_info.to_csv('df_ocr_info.tsv', sep = '\t', index = None)
        sku = df_tmp.iloc[i]['sku']
        x = df_tmp.iloc[i]['ocr']
        ocr_list = [a.strip() for a in x[2:-2].split('),(') if len(a.strip()) > 0]

        ocr_info = '|||'.join([''.join([aa.strip("'") for aa in ocr_list[i][2:-2].replace(')','').replace('(','').split(", ") if len(aa.strip("'")) > 0]) for i in range(len(ocr_list))])
        ocr_info = ocr_info.replace('None','')
        if len(ocr_info) > 0:
    #         print(sku)
    #         print(ocr_info)
            ocr_info_list.append([sku, ocr_info])
    df_ocr_info = pd.DataFrame(ocr_info_list)
    df_ocr_info.columns = ['sku','ocr_merge']
    df_ocr_info.to_csv('df_ocr_info.tsv', sep = '\t', index = None)
    return 

## 从原始数据中获取文案和商品数据
def get_item_ad(df_info, type = 'train'):
    print(len(df_info))
    if type == 'train':
        split_tag = 0
    else:
        split_tag = 2
    df_info = df_info[df_info['split_tag'] == split_tag]
    print(len(df_info))
    print(len(set(df_info['sku'])))
    df_item = df_info[['sku','sku_title', 'attr2_value_name','item_second_cate_name']]
    print(len(df_item))
    df_item = df_item.drop_duplicates()
    print(len(df_item))
    df_item['attr_merge'] = df_item['attr2_value_name'].apply(lambda x: '|'.join(set([a.strip() for a in x[2:-2].split('),(') if len(a.strip()) > 0])))
    df_wenan = df_info[['id','sku','sku_title','recommend_reason']]
    print(len(df_wenan))
    return df_wenan, df_item

## 从OCR数据中获取文案和商品数据
def get_item_ocr(df_ocr, df_ocr_info):
    sku_ids = set(df_ocr_info['sku'])
    print(len(sku_ids))
    df_item = df_ocr[df_ocr['sku'].isin(sku_ids)][['sku','sku_title', 'attr2_value_name','item_second_cate_name']]
    print(len(df_item))
    df_item = df_item.drop_duplicates()
    print(len(df_item))
    df_item['attr_merge'] = df_item['attr2_value_name'].apply(lambda x: '|'.join(set([a.strip() for a in x[2:-2].split('),(') if len(a.strip()) > 0])))
    
    sku_list = list(df_ocr_info['sku'])
    ocr_list = list(df_ocr_info['ocr_merge'])
    result_all = []
    count = 0
    for i in range(len(sku_list)):
        sku = sku_list[i]
        for ocr in ocr_list[i].split('|||'):
            result_all.append([count, sku, ocr])
            count += 1
    df_wenan = pd.DataFrame(result_all, columns = ['id', 'sku','recommend_reason'])
    df_wenan = df_wenan.sample(frac=1).reset_index(drop=True)
    print(len(df_wenan))
    df_wenan = df_wenan.merge(df_item[['sku','sku_title']], how = 'left', on = 'sku')
    df_wenan = df_wenan[['id','sku','sku_title','recommend_reason']]
    print(len(df_wenan), len(df_item))
    return df_wenan, df_item

## 从文案和商品数据中构建训练数据， 包括子任务：bi-商品属性一致性，s2s-商品文案， uni-文案
def get_df_unilm(df_wenan, df_item, max_len, n = 15, seed = 1234, 
                 wenan_min = 20, wenan_max = 90,  wenan_cut = 90,
                 attr_min = 10, attr_max = 80, attr_cut = 80,
                 title_min = 5, title_max = 80, title_cut = 80, drop_dup_ad = True):
    print(len(df_wenan), len(df_item))
    df_tmp = df_item[['sku','sku_title','attr_merge','item_second_cate_name']]
    if drop_dup_ad:
        df_w_tmp = df_wenan.drop_duplicates('recommend_reason')
    else:
        df_w_tmp = df_wenan
    print(len(df_w_tmp), len(df_tmp))
    ## 过滤长度不达标文案
    df_w_tmp = df_w_tmp[df_w_tmp['recommend_reason'].apply(lambda x: len(str(x)) > wenan_min and len(str(x)) < wenan_max)]
    ## 过滤长度不达标属性
    df_tmp = df_tmp[df_tmp['attr_merge'].apply(lambda x: len(str(x)) > attr_min and len(str(x)) < attr_max)]
    ## 过滤长度不达标标题
    df_tmp = df_tmp[df_tmp['sku_title'].apply(lambda x: len(str(x)) > title_min and len(str(x)) < title_max)]
    df_w_tmp = df_w_tmp[df_w_tmp['sku_title'].apply(lambda x: len(str(x)) > title_min and len(str(x)) < title_max)]
    ## 对于过长标题及文案截断
    df_w_tmp['sku_title'] = df_w_tmp['sku_title'].apply(lambda x: x[:title_cut])
    df_w_tmp['recommend_reason'] = df_w_tmp['recommend_reason'].apply(lambda x: x[:wenan_cut])
    
    df_tmp['sku_title'] = df_tmp['sku_title'].apply(lambda x: x[:title_cut])
    df_tmp['attr_merge'] = df_tmp['attr_merge'].apply(lambda x: x[:attr_cut])
    print(len(df_w_tmp), len(df_tmp))
    
    ## 构建字典sku--id, sku对应多条文案数据中，每条数据有唯一的id,方便后面构建负例
    sku_id_dic = defaultdict(list)
    id_list = list(df_w_tmp['id'])
    sku_list = list(df_w_tmp['sku'])
    for i in range(len(df_w_tmp)):
        sku_id_dic[sku_list[i]].append(id_list[i])
    print(len(sku_id_dic))
    
    ## 随机选取一半的sku用作bi-商品属性一致性任务，另外一半用作s2s-商品文案任务
    df_tmp = df_tmp.sample(frac=1, random_state = seed).reset_index(drop=True)
    sku_all = list(df_tmp['sku'])
    sku_bi = sku_all[:len(sku_all)//2]
    sku_s2s =  sku_all[len(sku_all)//2:]
    ## 通过设置适当的n，构建max_len数量目标的数据集，
    ## 一个sku对应多条文案且数量不确定，目前方法可选取大致范围内数量合适的数据
    while n > 2:
        s2s_id = []
        for sku in sku_s2s:
            s2s_id += sku_id_dic[sku][:n]
        print(n, len(s2s_id))  
#         if len(s2s_id) > len(df_tmp):
        if len(s2s_id) > max_len * 3:
            n -= 1
        else:
            break
    print(len(s2s_id))
    ## 保证uni-文案任务中使用的文案和s2s任务不重合
    uni_id = list(set(df_w_tmp['id']).difference(set(s2s_id)))
    print(len(uni_id))
    ## 最终平衡各任务数据量，使三个任务数据量一致
    max_len = min(len(uni_id), len(s2s_id),len(sku_bi)*2, max_len)
    uni_id = uni_id[:max_len]
    s2s_id = s2s_id[:max_len]
    sku_bi = sku_bi[:max_len//2]
    print(len(uni_id),len(s2s_id),len(sku_bi))
    
    ## bi-商品属性一致性任务, 正负例构建
    cat_dic = defaultdict(list)
    sku_cat_dic = {}
    sku_title_dic = {}
    sku_attr_dic = {}
    sku_list, cat_list = list(df_tmp['sku']), list(df_tmp['item_second_cate_name'])
    title_list, attr_list = list(df_tmp['sku_title']), list(df_tmp['attr_merge'])
    for i in range(len(sku_list)):
        cat_dic[cat_list[i]].append(sku_list[i])
        sku_cat_dic[sku_list[i]] = cat_list[i]
        sku_title_dic[sku_list[i]] = title_list[i]
        sku_attr_dic[sku_list[i]] = attr_list[i]
        
    result_pos = []
    random.shuffle(sku_bi)
    for i in range(len(sku_bi)):
        sku = sku_bi[i]
        attr = sku_attr_dic[sku]
        if i%2 == 0:
            attr_list = attr.split('|')
            random.shuffle(attr_list)
            attr = '|'.join(attr_list)
        result_pos.append([sku_title_dic[sku], attr, 0])
    result_neg = []
    random.shuffle(sku_bi)
    for i in range(len(sku_bi)):
        sku = sku_bi[i]
        if i%2 == 0:
            pool = cat_dic[sku_cat_dic[sku]]
        else:
            pool = sku_list
        sku_pair = random.choice(pool)
        result_neg.append([sku_title_dic[sku], sku_attr_dic[sku_pair], 1])
    
    result_all = result_pos + result_neg
    df_bi = pd.DataFrame(result_all)
    df_bi.columns = ['title', 'attr','nsp']
    df_bi = df_bi.sample(frac=1, random_state = 4321).reset_index(drop=True)

    df_s2s = df_w_tmp[df_w_tmp['id'].isin(set(s2s_id))][['id','sku','recommend_reason']]
    print(len(df_s2s))
    df_s2s = df_s2s.merge(df_tmp[['sku','sku_title','attr_merge']], how = 'left', on = 'sku')
    print(len(df_s2s))
    df_s2s['input'] = df_s2s['sku_title'] + df_s2s['attr_merge']
    df_uni = df_w_tmp[df_w_tmp['id'].isin(set(uni_id))][['id','sku','recommend_reason']]
    print(len(df_bi), len(df_s2s),len(df_uni))
    return df_bi, df_s2s, df_uni

def sentence_reorder(x):
    item_list = x.strip('。').split('。')
    random.shuffle(item_list)
    return '。'.join(item_list) + '。'


## 从文案和商品数据中构建训练数据， 包括子任务：bi-商品属性一致性，s2s-商品文案， uni-文案， s2s-打乱句子顺序, bi-商品文案一致性
## 未注释部分参见 get_df_unilm
def get_df_unilm_add2task(df_wenan, df_item, max_len, n = 15, seed = 1234, 
                 wenan_min = 20, wenan_max = 90,  wenan_cut = 90,
                 attr_min = 10, attr_max = 80, attr_cut = 80,
                 title_min = 5, title_max = 80, title_cut = 80, drop_dup_ad = True):
    print(len(df_wenan), len(df_item))
    df_tmp = df_item[['sku','sku_title','attr_merge','item_second_cate_name']]
    if drop_dup_ad:
        df_w_tmp = df_wenan.drop_duplicates('recommend_reason')
    else:
        df_w_tmp = df_wenan
    print(len(df_w_tmp), len(df_tmp))
    df_w_tmp = df_w_tmp[df_w_tmp['recommend_reason'].apply(lambda x: len(str(x)) > wenan_min and len(str(x)) < wenan_max)]
    df_tmp = df_tmp[df_tmp['attr_merge'].apply(lambda x: len(str(x)) > attr_min and len(str(x)) < attr_max)]
    df_tmp = df_tmp[df_tmp['sku_title'].apply(lambda x: len(str(x)) > title_min and len(str(x)) < title_max)]
    df_w_tmp = df_w_tmp[df_w_tmp['sku_title'].apply(lambda x: len(str(x)) > title_min and len(str(x)) < title_max)]
    df_w_tmp['sku_title'] = df_w_tmp['sku_title'].apply(lambda x: x[:title_cut])
    df_w_tmp['recommend_reason'] = df_w_tmp['recommend_reason'].apply(lambda x: x[:wenan_cut])
    
    df_tmp['sku_title'] = df_tmp['sku_title'].apply(lambda x: x[:title_cut])
    df_tmp['attr_merge'] = df_tmp['attr_merge'].apply(lambda x: x[:attr_cut])
    print(len(df_w_tmp), len(df_tmp))
    
    sku_id_dic = defaultdict(list)
    id_list = list(df_w_tmp['id'])
    sku_list = list(df_w_tmp['sku'])
    for i in range(len(df_w_tmp)):
        sku_id_dic[sku_list[i]].append(id_list[i])
    print(len(sku_id_dic))
    
    
    df_tmp = df_tmp.sample(frac=1, random_state = seed).reset_index(drop=True)
    sku_all = list(df_tmp['sku'])
    sku_bi = sku_all[:len(sku_all)//2]
    sku_s2s =  sku_all[len(sku_all)//2:]
#     n = 50
    while n > 2:
        s2s_id = []
        for sku in sku_s2s:
            s2s_id += sku_id_dic[sku][:n]
        print(n, len(s2s_id))  
#         if len(s2s_id) > len(df_tmp):
        if len(s2s_id) > max_len * 3:
            n -= 1
        else:
            break
    print(len(s2s_id))
    uni_id = list(set(df_w_tmp['id']).difference(set(s2s_id)))
    print(len(uni_id))
    max_len = min(len(uni_id), len(s2s_id),len(sku_bi)*2, max_len)
    uni_id = uni_id[:max_len]
    s2s_id = s2s_id[:max_len]
    sku_bi = sku_bi[:max_len//2]

    ## 从s2s_id中选择各一半用作两个任务: s2s-商品文案，s2s-打乱句子顺序
    s2s_id_wenan = s2s_id[:max_len//2]
    s2s_id_order = s2s_id[max_len//2:]

    print(len(uni_id),len(s2s_id),len(sku_bi), len(s2s_id_wenan), len(s2s_id_order))
    
    cat_dic = defaultdict(list)
    sku_cat_dic = {}
    sku_title_dic = {}
    sku_attr_dic = {}
    sku_list, cat_list = list(df_tmp['sku']), list(df_tmp['item_second_cate_name'])
    title_list, attr_list = list(df_tmp['sku_title']), list(df_tmp['attr_merge'])
    for i in range(len(sku_list)):
        cat_dic[cat_list[i]].append(sku_list[i])
        sku_cat_dic[sku_list[i]] = cat_list[i]
        sku_title_dic[sku_list[i]] = title_list[i]
        sku_attr_dic[sku_list[i]] = attr_list[i]
        
    
    ## get data for task: product / attribute relevance
    result_all = []
    for i in range(len(sku_bi)):
        sku = sku_bi[i]
        random_thres = random.random()
        if random_thres > 0.5:
            attr = sku_attr_dic[sku]
            if random_thres > 0.75:
                attr_list = attr.split('|')
                random.shuffle(attr_list)
                attr = '|'.join(attr_list)
            result_all.append([sku_title_dic[sku], attr, 0])
        else:
            if random_thres < 0.25:
                pool = cat_dic[sku_cat_dic[sku]]
            else:
                pool = sku_list
            sku_pair = random.choice(pool)
            result_all.append([sku_title_dic[sku], sku_attr_dic[sku_pair], 1])
    
    df_bi_att = pd.DataFrame(result_all)
    df_bi_att.columns = ['title', 'attr','nsp']
    df_bi_att = df_bi_att.sample(frac=1, random_state = 4321).reset_index(drop=True)

    ## get data for task s2s
    df_s2s = df_w_tmp[df_w_tmp['id'].isin(set(s2s_id_wenan))][['id','sku','recommend_reason']]
    print(len(df_s2s))
    df_s2s = df_s2s.merge(df_tmp[['sku','sku_title','attr_merge']], how = 'left', on = 'sku')
    print(len(df_s2s))
    df_s2s['input'] = df_s2s['sku_title'] + df_s2s['attr_merge']

    ## get data for task uni-bidirection
    df_uni = df_w_tmp[df_w_tmp['id'].isin(set(uni_id))][['id','sku','recommend_reason']]

    ## get data for task sentence reorder
    df_s2s_order = df_w_tmp[df_w_tmp['id'].isin(set(s2s_id_order))][['id','sku','recommend_reason']]
    df_s2s_order['input'] = df_s2s_order['recommend_reason'].apply(lambda x: sentence_reorder(x))
    print(len(df_s2s_order))
    
    ## merge df_s2s
    df_s2s = merge_df(df_s2s[['id','sku','input','recommend_reason']], df_s2s_order[['id','sku','input','recommend_reason']])


    ## bi-商品文案一致性任务, 正负例构建
    df_w_tmp_uniq = df_w_tmp[['sku','recommend_reason']].sample(frac=1, random_state = seed).reset_index(drop=True).drop_duplicates('sku')
    sku_wenan_dic = {}
    sku_w_list, wenan_w_list = list(df_w_tmp_uniq['sku']), list(df_w_tmp_uniq['recommend_reason'])
    for i in range(len(sku_w_list)):
        sku_wenan_dic[str(sku_w_list[i])] = wenan_w_list[i]

    sku_wenan_dic = {int(key):value for key, value in sku_wenan_dic.items()}
    sku_wenan_relevance = list(set(sku_s2s).difference(set(df_s2s['sku'])).intersection(sku_wenan_dic.keys()))[:max_len//2]
    print(len(sku_wenan_relevance))
    cat_wenan_dic = {key: list(set(value).intersection(sku_wenan_dic.keys())) for key,value in cat_dic.items()}
    
    sku_wenan_list = list(sku_wenan_dic.keys())
    
    result_all = []
    for i in range(len(sku_wenan_relevance)):
        sku = int(sku_wenan_relevance[i])
        attr = sku_attr_dic[sku]
        random_thres = random.random()
        if random_thres > 0.5:
            result_all.append([sku_title_dic[sku], attr, sku_wenan_dic[sku], 0])
        else:
            if random_thres < 0.25:
                pool = cat_wenan_dic[sku_cat_dic[sku]]
            else:
                pool = sku_wenan_list
            if len(pool) == 0:
                pool = sku_wenan_list
            sku_pair = random.choice(pool)
            result_all.append([sku_title_dic[sku], attr, sku_wenan_dic[sku_pair], 1])
    
    df_bi_wenan = pd.DataFrame(result_all)
    df_bi_wenan.columns = ['title', 'attr','wenan', 'nsp']
    df_bi_wenan['seq1'] = df_bi_wenan['title'] + df_bi_wenan['attr']
    df_bi_wenan['seq2'] = df_bi_wenan['wenan']
    df_bi_wenan = df_bi_wenan.sample(frac=1, random_state = 4321).reset_index(drop=True)

    ## merge df_bi
    df_bi = df_bi_att[['title', 'attr','nsp']]
    df_bi.columns = ['seq1','seq2','nsp']
    df_bi = merge_df(df_bi, df_bi_wenan[['seq1','seq2','nsp']])

    print(len(df_bi), len(df_s2s),len(df_uni))
    return df_bi, df_s2s, df_uni


## 合并两个dataframe，并使用random_seed做shuffle
def merge_df(df1, df2, seed = 1234):
    df = pd.concat([df1,df2], axis = 0)
    df = df.sample(frac=1, random_state = seed).reset_index(drop=True)
    return df

## 获取第一版本的unilm预训练模型的训练数据，包括子任务：bi-商品属性一致性，s2s-商品文案， uni-文案
def get_unilm_v2(data_dir, 
                 output_dir = '/export/Data/zhangxueying17/smart_shopping/pretrain/unilm_v2/'):
    df_info = get_df(data_dir, 'pretrain_all_select', -1)
    df_ocr = get_df(data_dir, 'pretrain_ocr', -1)
    df_ocr_info = pd.read_csv('df_ocr_info.tsv', sep = '\t')

    df_wenan, df_item = get_item_ad(df_info, type = 'train')
    df_wenan_o, df_item_o = get_item_ocr(df_ocr, df_ocr_info)

    df_bi_a, df_s2s_a, df_uni_a = get_df_unilm(df_wenan, df_item, 1700000)
    df_bi_o, df_s2s_o, df_uni_o = get_df_unilm(df_wenan_o, df_item_o, 1700000, 15,   
                                            wenan_max = 1000, attr_max = 1000, title_max = 1000)

    df_bi = merge_df(df_bi_a, df_bi_o)
    df_s2s = merge_df(df_s2s_a, df_s2s_o)
    df_uni = merge_df(df_uni_a, df_uni_o)

    print(len(df_s2s),len(df_bi),len(df_uni))
    
    df_bi.to_csv(os.path.join(output_dir, 'bi.tsv'), sep = '\t', index = None)
    df_uni.to_csv(os.path.join(output_dir, 'uni.tsv'), sep = '\t', index = None)
    df_s2s.to_csv(os.path.join(output_dir, 's2s.tsv'), sep = '\t', index = None)

## 获取第二版本的unilm预训练模型的训练数据，较第一版增加了两个子任务，s2s-打乱句子顺序, bi-商品文案一致性
def get_unilm_v3(data_dir,
                 output_dir = '/export/Data/zhangxueying17/smart_shopping/pretrain/unilm_v3/'):

    df_info = get_df(data_dir, 'pretrain_all_select', -1)
    df_ocr = get_df(data_dir, 'pretrain_ocr', -1)
    df_ocr_info = pd.read_csv(os.path.join(data_dir,'df_ocr_info.tsv'), sep = '\t')

    df_wenan, df_item = get_item_ad(df_info, type = 'train')
    df_wenan_o, df_item_o = get_item_ocr(df_ocr, df_ocr_info)

    df_bi_a, df_s2s_a, df_uni_a = get_df_unilm_add2task(df_wenan, df_item, 1700000)
    df_bi_o, df_s2s_o, df_uni_o = get_df_unilm(df_wenan_o, df_item_o, 1700000, 15,  
                                            wenan_max = 1000, attr_max = 1000, title_max = 1000)
    df_bi_o.columns = ['seq1','seq2','nsp']
    df_s2s_o = df_s2s_o[['id','sku','input','recommend_reason']]

    df_bi = merge_df(df_bi_a, df_bi_o)
    df_s2s = merge_df(df_s2s_a, df_s2s_o)
    df_uni = merge_df(df_uni_a, df_uni_o)

    print(len(df_s2s),len(df_bi),len(df_uni))
    
    df_bi.to_csv(os.path.join(output_dir, 'bi.tsv'), sep = '\t', index = None)
    df_uni.to_csv(os.path.join(output_dir, 'uni.tsv'), sep = '\t', index = None)
    df_s2s.to_csv(os.path.join(output_dir, 's2s.tsv'), sep = '\t', index = None)





## 获取第一版本的unilm预训练模型的eval数据
def get_unilm_v2_eval(data_dir,
                      output_dir = '/export/Data/zhangxueying17/smart_shopping/pretrain/unilm_v2_eval/'):

    df_info = get_df(data_dir, 'pretrain_all_select', -1)
    df_wenan, df_item = get_item_ad(df_info, type = 'eval')
    df_bi, df_s2s, df_uni = get_df_unilm(df_wenan, df_item, 50000)

    print(len(df_s2s),len(df_bi),len(df_uni))

    df_bi.to_csv(os.path.join(output_dir, 'bi.tsv'), sep = '\t', index = None)
    df_uni.to_csv(os.path.join(output_dir, 'uni.tsv'), sep = '\t', index = None)
    df_s2s.to_csv(os.path.join(output_dir, 's2s.tsv'), sep = '\t', index = None)

## 获取第二版本的unilm预训练模型的eval数据
def get_unilm_v3_eval(data_dir,
                      output_dir = '/export/Data/zhangxueying17/smart_shopping/pretrain/unilm_v3_eval/'):

    df_info = get_df(data_dir, 'pretrain_all_select', -1)

    df_wenan, df_item = get_item_ad(df_info, type = 'eval')

    df_bi, df_s2s, df_uni = get_df_unilm_add2task(df_wenan, df_item, 50000)

    print(len(df_s2s),len(df_bi),len(df_uni))

    df_bi.to_csv(os.path.join(output_dir, 'bi.tsv'), sep = '\t', index = None)
    df_uni.to_csv(os.path.join(output_dir, 'uni.tsv'), sep = '\t', index = None)
    df_s2s.to_csv(os.path.join(output_dir, 's2s.tsv'), sep = '\t', index = None)


def test():
    x = '套装合计8册，精选海豚绘本花园语言启蒙类绘本。幼儿园3-6岁必备。从五大领域中的语言领域出发，着重语言启蒙能力的提升。引导孩子能说、敢说、会说，培养前阅读和前书写技能。'
    print(sentence_reorder(x))

def main():
    ## please change data_dir and output_dir
    data_dir = '/export/Data/zhangxueying17/smart_shopping/pretrain/'
    # get_unilm_v2(data_dir)
    # get_unilm_v2_eval(data_dir)
    # get_unilm_v3(data_dir)
    get_unilm_v3_eval(data_dir)

if __name__ == "__main__":
    main()