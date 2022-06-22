
# UniLM_CodeBase

This project is our version of UniLM for pratraining and fine-turning.

## Requirments
* apex

Before install apex, please install cuda (with the same version as cudatoolkit in your anaconda enviroment). Please refer to the [link](https://blog.csdn.net/weixin_41278720/article/details/81255265) to install locally.
``` bash
PWD_DIR=$(pwd)
cd $(mktemp -d)
git clone -q https://github.com/NVIDIA/apex.git
cd apex
python setup.py install --user --cuda_ext --cpp_ext
cd $PWD_DIR
```
Then you can import apex without any error.


## Data prepare and processing
### 1. We expect the original(raw) data are stored in "*.tsv" files with the following format:
``` bash
Attrbute_Name_1 \t Attrbute_Name_2 \t ... \t Attrbute_Name_N
xxxx \t yyyy \t ... \t zzzz
```
Please make sure that the training folder contains ``bi.tsv``, ``uni.tsv``,``s2s.tsv``

Please check the [readme](https://git.jd.com/jd_smart_shopping/pretraininglm_ecommerce/blob/pretrain-Xueying/data_preprocess/readme.md) for more details about how to get the traning data.

Please specify the input and output attributes' name. 

- Bi-direction: bi.tsv, need to specify attribute name for input, output, nsp.
- Uni-direction: uni.tsv, need to specify attribute name for output.
- S2S: s2s.tsv, need to specify attribute name for input, output.

### 2. processing the raw data.
check the [readme](https://git.jd.com/jd_smart_shopping/pretraininglm_ecommerce/blob/pretrain-Xueying/preprocess/readme.md) for more details 

## Run training
``` bash
CUDA_VISIBLE_DEVICES=0,1,2,3 python biunilm/run_seq2seq_merge.py --do_train --fp16 --amp --num_workers 0 \
  --bert_model bert-base-chinese --new_segment_ids --tokenized_input \
  --data_dir /export/Data/zhangxueying17/smart_shopping/Pretrain_Data/unilm_v2/processed \
  --output_dir /export/Data/zhangxueying17/Pretrain_Text_Generation/unilm_v2/bert_save \
  --log_dir export/Data/zhangxueying17/Pretrain_Text_Generation/unilm_v2/bert_log \
  --max_seq_length 250 --max_position_embeddings 250 \
  --trunc_seg a --always_truncate_tail --max_len_b 90 \
  --mask_prob 0.15 --max_pred 64 \
  --mask_source_words \
  --train_batch_size 330 --gradient_accumulation_steps 2 \
  --learning_rate 0.00003 --warmup_proportion 0.1 --label_smoothing 0.1 \
  --num_train_epochs 100
```



## Run eval
``` bash
CUDA_VISIBLE_DEVICES=4 python biunilm/eval_merge.py --do_eval --fp16 --amp --num_workers 0 \
  --bert_model bert-base-chinese --new_segment_ids --tokenized_input \
  --model_recover_path /export/Data/zhangxueying17/Pretrain_Text_Generation/unilm_v3/bert_save \
  --data_dir /export/Data/zhangxueying17/smart_shopping/Pretrain_Data/unilm_v3_eval/processed \
  --output_dir /export/Data/zhangxueying17/Pretrain_Text_Generation/unilm_v3_eval/bert_save \
  --log_dir /export/Data/zhangxueying17/Pretrain_Text_Generation/unilm_v3_eval/bert_log \
  --max_seq_length 250 --max_position_embeddings 250 \
  --trunc_seg a --always_truncate_tail --max_len_b 90 \
  --mask_prob 0.15 --max_pred 64 \
  --mask_source_words \
  --train_batch_size 330 --gradient_accumulation_steps 1 \
  --eval_data_type uni/bi/s2s 
```
We evaluate the result separately, need to specify the eval_data_type for each run.
You may use plot_eval.py to get the evaluation figure.  
For running plot_eval.py, pip install matplotlib
