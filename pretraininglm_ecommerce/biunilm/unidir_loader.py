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


def truncate_tokens(tokens, max_len, always_truncate_tail=False):
    num_truncated = [0, 0]
    while True:
        if len(tokens) <= max_len:
            break
        trunc_tokens = tokens
        # whether always truncate source sequences
        if (not always_truncate_tail) and (rand() < 0.5):
            del trunc_tokens[0]
            num_truncated[0] += 1
        else:
            trunc_tokens.pop()
            num_truncated[1] += 1
    return num_truncated


class UniDirDataset(torch.utils.data.Dataset):
    """ Load sentence pair (sequential or random order) from corpus """

    def __init__(self, file_tgt, batch_size, tokenizer, max_len, file_oracle=None, short_sampling_prob=0.1, sent_reverse_order=False, uni_pipeline=[]):
        super().__init__()
        self.tokenizer = tokenizer  # tokenize function
        self.max_len = max_len  # maximum length of tokens
        self.short_sampling_prob = short_sampling_prob
        self.uni_pipeline = uni_pipeline
        self.batch_size = batch_size
        self.sent_reverse_order = sent_reverse_order

        # read the file into memory
        self.ex_list = []
        if file_oracle is None:
            with open(file_tgt, "r", encoding='utf-8') as f_tgt:
                for tgt in f_tgt:
                    tgt_tk = tokenizer.tokenize(tgt.strip())
                    assert len(tgt_tk) > 0
                    self.ex_list.append(tgt_tk)
        # else:
        #     with open(file_src, "r", encoding='utf-8') as f_src, \
        #             open(file_tgt, "r", encoding='utf-8') as f_tgt, \
        #             open(file_oracle, "r", encoding='utf-8') as f_orc:
        #         for src, tgt, orc in zip(f_src, f_tgt, f_orc):
        #             src_tk = tokenizer.tokenize(src.strip())
        #             tgt_tk = tokenizer.tokenize(tgt.strip())
        #             s_st, labl = orc.split('\t')
        #             s_st = [int(x) for x in s_st.split()]
        #             labl = [int(x) for x in labl.split()]
        #             self.ex_list.append((src_tk, tgt_tk, s_st, labl))
        print('Load {0} documents'.format(len(self.ex_list)))

    def __len__(self):
        return len(self.ex_list)

    def __getitem__(self, idx):
        instance = self.ex_list[idx]
        proc = choice(self.uni_pipeline)
        instance = proc(instance)
        return instance

    def __iter__(self):  # iterator to load data
        for __ in range(math.ceil(len(self.ex_list) / float(self.batch_size))):
            batch = []
            for __ in range(self.batch_size):
                idx = randint(0, len(self.ex_list)-1)
                batch.append(self.__getitem__(idx))
            # To Tensor
            yield batch_list_to_batch_tensors(batch)


class Preprocess4UniDirection(Pipeline):
    """ Pre-processing steps for pretraining transformer """

    def __init__(self, max_pred, mask_prob, vocab_words, indexer, max_len=512, skipgram_prb=0, skipgram_size=0, block_mask=False, mask_whole_word=False, new_segment_ids=False, truncate_config={}, mask_source_words=False, mode="l2r", has_oracle=False, num_qkv=0, s2s_special_token=False, s2s_add_segment=False, s2s_share_segment=False, pos_shift=False):
        super().__init__()
        self.max_len = max_len
        self.max_pred = max_pred  # max tokens of prediction
        self.mask_prob = mask_prob  # masking probability
        self.vocab_words = vocab_words  # vocabulary (sub)words
        self.indexer = indexer  # function from token to token index
        self.max_len = max_len
        self._tril_matrix = torch.tril(torch.ones(
            (max_len, max_len), dtype=torch.long))     ## lower triangle matrix as l2r input mask

        self._tril_matrix_upper = torch.transpose(torch.tril(torch.ones(
            (max_len, max_len), dtype=torch.long)), 0, 1)  ## upper triangle matrix as r2l input mask
            
        self.skipgram_prb = skipgram_prb
        self.skipgram_size = skipgram_size
        self.mask_whole_word = mask_whole_word
        self.new_segment_ids = new_segment_ids
        self.always_truncate_tail = truncate_config.get(
            'always_truncate_tail', False)
        # self.max_len_a = truncate_config.get('max_len_a', None)
        # self.max_len_b = truncate_config.get('max_len_b', None)
        # self.trunc_seg = truncate_config.get('trunc_seg', None)
        self.task_idx = 3   # relax projection layer for different tasks
        self.mask_source_words = mask_source_words
        assert mode in ("l2r","r2l")
        self.mode = mode
        self.has_oracle = has_oracle
        self.num_qkv = num_qkv
        self.s2s_special_token = s2s_special_token
        # self.s2s_add_segment = s2s_add_segment
        # self.s2s_share_segment = s2s_share_segment
        self.pos_shift = pos_shift

    def __call__(self, instance):
        tokens_b = instance

        # if self.pos_shift and self.mode == 'l2r':
        #     tokens_b = ['[CLS]'] + tokens_b

        # -2  for special tokens [CLS], [SEP],
        num_truncated_a, _ = truncate_tokens(tokens_b, self.max_len - 2,always_truncate_tail=self.always_truncate_tail)

        # Add Special Tokens
        if self.s2s_special_token:
            if self.mode == 'l2r':
                tokens = ['[L2R_CLS]'] + tokens_b + ['[L2R_SEP]']
            else:
                tokens = ['[R2L_CLS]'] + tokens_b + ['[R2L_SEP]']
        else:
            tokens = ['[CLS]'] + tokens_b + ['[SEP]']

        if self.new_segment_ids:
            if self.mode == "l2r":
                segment_ids = [2] * (len(tokens))
            else:
                segment_ids = [3] * (len(tokens))
        else:
            segment_ids = [0]*(len(tokens))

        if self.pos_shift:
            n_pred = min(self.max_pred, len(tokens_b)+1)
            masked_pos = [i for i in range(len(tokens_b)+1)] ## predict end token in shift mode
            masked_weights = [1]*n_pred
            masked_ids = self.indexer(tokens_b+['[SEP]'])
        else:
            # For masked Language Models
            # the number of prediction is sometimes less than max_pred when sequence is short
            effective_length = len(tokens_b)
            # if self.mask_source_words:
            #     effective_length += len(tokens_a)
            n_pred = min(self.max_pred, max(
                1, int(round(effective_length*self.mask_prob))))
            # candidate positions of masked tokens
            cand_pos = []
            special_pos = set()
            for i, tk in enumerate(tokens):
                # only mask tokens_b (target sequence)
                # we will mask [SEP] as an ending symbol ? 预训练是否mask[SEP]
                if (tk != '[CLS]'):
                    cand_pos.append(i)
                # elif self.mask_source_words and (i < len(tokens_a)+2) and (tk != '[CLS]') and (not tk.startswith('[SEP')):
                #     cand_pos.append(i)
                else:
                    special_pos.add(i)
            shuffle(cand_pos)

            masked_pos = set()
            max_cand_pos = max(cand_pos)
            for pos in cand_pos:
                if len(masked_pos) >= n_pred:
                    break
                if pos in masked_pos:
                    continue

                def _expand_whole_word(st, end):
                    new_st, new_end = st, end
                    while (new_st >= 0) and tokens[new_st].startswith('##'):
                        new_st -= 1
                    while (new_end < len(tokens)) and tokens[new_end].startswith('##'):
                        new_end += 1
                    return new_st, new_end

                if (self.skipgram_prb > 0) and (self.skipgram_size >= 2) and (rand() < self.skipgram_prb):
                    # ngram
                    cur_skipgram_size = randint(2, self.skipgram_size)
                    if self.mask_whole_word:
                        st_pos, end_pos = _expand_whole_word(
                            pos, pos + cur_skipgram_size)
                    else:
                        st_pos, end_pos = pos, pos + cur_skipgram_size
                else:
                    # directly mask
                    if self.mask_whole_word:
                        st_pos, end_pos = _expand_whole_word(pos, pos + 1)
                    else:
                        st_pos, end_pos = pos, pos + 1

                for mp in range(st_pos, end_pos):
                    if (0 < mp <= max_cand_pos) and (mp not in special_pos):
                        masked_pos.add(mp)
                    else:
                        break

            masked_pos = list(masked_pos)
            if len(masked_pos) > n_pred:
                shuffle(masked_pos)
                masked_pos = masked_pos[:n_pred]

            masked_tokens = [tokens[pos] for pos in masked_pos]
            for pos in masked_pos:
                if rand() < 0.8:  # 80%
                    tokens[pos] = '[MASK]'
                elif rand() < 0.5:  # 10%
                    tokens[pos] = get_random_word(self.vocab_words)
            # when n_pred < max_pred, we only calculate loss within n_pred
            masked_weights = [1]*len(masked_tokens)

            # Token Indexing
            masked_ids = self.indexer(masked_tokens)
        # Token Indexing
        input_ids = self.indexer(tokens)

        # Zero Padding
        n_pad = self.max_len - len(input_ids)
        input_ids.extend([0]*n_pad)
        segment_ids.extend([0]*n_pad)

        if self.num_qkv > 1:
            mask_qkv = [1] * (len(tokens_b)+2)
            mask_qkv.extend([0]*n_pad)
        else:
            mask_qkv = None

        input_mask = torch.zeros(self.max_len, self.max_len, dtype=torch.long)
        if self.mode == "l2r":
            st, end = 0, len(tokens_b) + 2
            input_mask[st:end, st:end].copy_(self._tril_matrix[:end, :end])
        else:
            st, end = 0, len(tokens_b) + 2
            input_mask[st:end, st:end].copy_(self._tril_matrix_upper[:end, :end])

        # Zero Padding for masked target
        if self.max_pred > n_pred:
            n_pad = self.max_pred - n_pred
            if masked_ids is not None:
                masked_ids.extend([0]*n_pad)
            if masked_pos is not None:
                masked_pos.extend([0]*n_pad)
            if masked_weights is not None:
                masked_weights.extend([0]*n_pad)

        oracle_pos = None
        oracle_weights = None
        oracle_labels = None
        # if self.has_oracle:
        #     s_st, labls = instance[2:]
        #     oracle_pos = []
        #     oracle_labels = []
        #     for st, lb in zip(s_st, labls):
        #         st = st - num_truncated_a[0]
        #         if st > 0 and st < len(tokens_a):
        #             oracle_pos.append(st)
        #             oracle_labels.append(lb)
        #     oracle_pos = oracle_pos[:20]
        #     oracle_labels = oracle_labels[:20]
        #     oracle_weights = [1] * len(oracle_pos)
        #     if len(oracle_pos) < 20:
        #         x_pad = 20 - len(oracle_pos)
        #         oracle_pos.extend([0] * x_pad)
        #         oracle_labels.extend([0] * x_pad)
        #         oracle_weights.extend([0] * x_pad)

        #     return (input_ids, segment_ids, input_mask, mask_qkv, masked_ids,
        #             masked_pos, masked_weights, -1, self.task_idx,
        #             oracle_pos, oracle_weights, oracle_labels)

        return (input_ids, segment_ids, input_mask, mask_qkv, masked_ids, masked_pos, masked_weights, -1, self.task_idx)


