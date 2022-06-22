from random import randint, shuffle, choice
from random import random as rand
import math
import torch

from biunilm.loader_utils import get_random_word, batch_list_to_batch_tensors, Pipeline

# Input file format :
# 1. One sentence per line. These should ideally be actual sentences,
#    not entire paragraphs or arbitrary spans of text. (Because we use
#    the sentence boundaries for the "next sentence prediction" task).
# 2. Blank lines between documents. Document boundaries are needed
#    so that the "next sentence prediction" task doesn't span between documents.




class Bi_Uni_Dataset(torch.utils.data.Dataset):
    """ Load sentence pair (sequential or random order) from corpus """

    def __init__(self, file_src_bi, file_tgt_bi, file_tgt_uni, file_src_s2s, file_tgt_s2s, 
                batch_size, tokenizer, max_len, file_nsp = None,  
                short_sampling_prob=0.1, sent_reverse_order=False, bi_uni_pipeline=[]):
        super().__init__()
        self.tokenizer = tokenizer  # tokenize function
        self.max_len = max_len  # maximum length of tokens
        self.short_sampling_prob = short_sampling_prob
        self.bi_uni_pipeline = bi_uni_pipeline
        self.batch_size = batch_size
        self.sent_reverse_order = sent_reverse_order

        # read the file into memory
        self.ex_list = []
        self.ex_list_bi = []
        self.ex_list_uni = []
        self.ex_list_s2s = []

        with open(file_src_s2s, "r", encoding='utf-8') as f_src, open(file_tgt_s2s, "r", encoding='utf-8') as f_tgt:
            for src, tgt in zip(f_src, f_tgt):
                src_tk = tokenizer.tokenize(src.strip())
                tgt_tk = tokenizer.tokenize(tgt.strip())
                assert len(src_tk) > 0
                assert len(tgt_tk) > 0
                self.ex_list_s2s.append((src_tk, tgt_tk))

        if file_nsp is None:
            with open(file_src_bi, "r", encoding='utf-8') as f_src, open(file_tgt_bi, "r", encoding='utf-8') as f_tgt:
                for src, tgt in zip(f_src, f_tgt):
                    src_tk = tokenizer.tokenize(src.strip())
                    tgt_tk = tokenizer.tokenize(tgt.strip())
                    assert len(src_tk) > 0
                    assert len(tgt_tk) > 0
                    self.ex_list_bi.append((src_tk, tgt_tk, -1))
        else:
            with open(file_src_bi, "r", encoding='utf-8') as f_src, open(file_tgt_bi, "r", encoding='utf-8') as f_tgt, open(file_nsp, "r", encoding='utf-8') as f_nsp:
                for src, tgt, nsp in zip(f_src, f_tgt, f_nsp):
                    src_tk = tokenizer.tokenize(src.strip())
                    tgt_tk = tokenizer.tokenize(tgt.strip())
                    is_next = int(nsp.strip())
                    assert len(src_tk) > 0
                    assert len(tgt_tk) > 0
                    assert is_next in [0,1]
                    self.ex_list_bi.append((src_tk, tgt_tk, is_next))

        with open(file_tgt_uni, "r", encoding='utf-8') as f_tgt:
            for tgt in f_tgt:
                tgt_tk = tokenizer.tokenize(tgt.strip())
                assert len(tgt_tk) > 0
                self.ex_list_uni.append(tgt_tk)

        self.total_len = 3 * min(len(self.ex_list_bi),len(self.ex_list_s2s),len(self.ex_list_uni))



        print('Load {0} documents'.format(self.total_len))

    def __len__(self):
        return self.total_len

    def __getitem__(self, idx):
        if idx % 3 == 0:
            instance = self.ex_list_bi[idx//3]
            proc = self.bi_uni_pipeline[0]
            instance = proc(instance)
        if idx % 3 == 1:
            instance = self.ex_list_uni[idx//3]
            proc = self.bi_uni_pipeline[1]
            instance = proc(instance)
        if idx % 3 == 2:
            instance = self.ex_list_s2s[idx//3]
            proc = self.bi_uni_pipeline[2]
            instance = proc(instance)
        return instance

    def __iter__(self):  # iterator to load data
        for __ in range(math.ceil(self.total_len/ float(self.batch_size))):
            batch = []
            for __ in range(self.batch_size):
                idx = randint(0, self.total_len-1)
                batch.append(self.__getitem__(idx))
            # To Tensor
            yield batch_list_to_batch_tensors(batch)


