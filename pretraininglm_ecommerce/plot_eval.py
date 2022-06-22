import os
import matplotlib.pyplot as plt
data_dir = '/export/Data/zhangxueying17/Pretrain_Text_Generation/unilm_v2/bert_save/'
data_dir = '/export/Data/zhangxueying17/Pretrain_Text_Generation/unilm_v3/bert_save/'
uni_list = []
for file in [os.path.join(data_dir, x) for x in os.listdir(data_dir) if 'eval_uni' in x]:
    with open(file, 'r') as f:
        xx = f.read()
        loss = float(xx.split('\t')[0])
        uni_list.append(loss)
bi_list = []
for file in [os.path.join(data_dir, x) for x in os.listdir(data_dir) if 'eval_bi' in x]:
    with open(file, 'r') as f:
        xx = f.read()
        loss = float(xx.split('\t')[0])
        bi_list.append(loss)
nsp_list = []
for file in [os.path.join(data_dir, x) for x in os.listdir(data_dir) if 'eval_bi' in x]:
    with open(file, 'r') as f:
        xx = f.read()
        loss = float(xx.split('\t')[1])
        nsp_list.append(loss)
s2s_list = []
for file in [os.path.join(data_dir, x) for x in os.listdir(data_dir) if 'eval_s2s' in x]:
    with open(file, 'r') as f:
        xx = f.read()
        loss = float(xx.split('\t')[0])
        s2s_list.append(loss)
min_len = min(min(len(s2s_list), len(bi_list)), len(uni_list))
biall_list = [bi_list[i] + nsp_list[i] for i in range(min_len)]
lost_list = [biall_list[i] + s2s_list[i] + uni_list[i] for i in range(min_len)]
data_all = {}
data_all['uni'] = uni_list
data_all['bi'] = bi_list
data_all['nsp'] = nsp_list
data_all['s2s'] = s2s_list
data_all['biall'] = biall_list
data_all['all'] = lost_list

plot_keys = ['uni','bi','nsp','s2s','biall','all']
plot_keys = ['uni','bi','s2s','nsp']
for key in plot_keys:
    plt.plot([i+1 for i in range(len(data_all[key]))], data_all[key])
plt.legend(plot_keys)
plt.xlabel('epoch')
plt.ylabel('loss')
plt.savefig('eval_unilmv3.png')