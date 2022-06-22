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

( I just use the old version in original UNILM code )

## Data prepare and processing
### 1. We expect the original(raw) data are stored in "*.tsv" files with the following format:
``` bash
SKU_ID \t Attrbute_Name_1 \t Attrbute_Name_2 \t ... \t Attrbute_Name_N
11111 \t xxxx \t yyyy \t ... \t zzzz
```
Please make sure that the train/eval files are named with ``train/eval.tsv``

Please specify the input and output attributes' name. We assume the input attribute is ``A`` and output attributes name is ``B``.

`data.py process()`

### 2. processing the raw data.
``` bash
Raw_tsv_dir=/export/shenkai/data/dapei/data_v1
Input_attr=A
Output_attr=B
Output_dir_path=/export/shenkai/data/dapei/data_processed_v1
python preprocess/tokenizing.py --split_name train --raw_tsv_dir $Raw_tsv_dir --input_attr $Input_attr --output_attr $Output_attr --output_dir_path $Output_dir_path
python preprocess/tokenizing.py --split_name eval --raw_tsv_dir $Raw_tsv_dir --input_attr $Input_attr --output_attr $Output_attr --output_dir_path $Output_dir_path
```

* for support 000001 encoding , I change the `process` function
* Input too long, use `data.py cut()` to cut src file

## Run training
``` bash
DATA_DIR=/export/shenkai/data/dapei/data_processed_v1/processed
OUTPUT_DIR=save
MODEL_RECOVER_PATH=pretrain_ckpt # no use
export CUDA_VISIBLE_DEVICES=0,1,2,3
python biunilm/run_seq2seq.py --do_train --fp16 --amp --num_workers 12 \
  --bert_model bert-base-chinese --new_segment_ids --tokenized_input \
  --data_dir ${DATA_DIR} --src_file train.src --tgt_file train.tgt \
  --output_dir ${OUTPUT_DIR}/bert_save \
  --log_dir ${OUTPUT_DIR}/bert_log \
  --max_seq_length 250 --max_position_embeddings 250 \
  --trunc_seg a --always_truncate_tail --max_len_b 90 \
  --mask_prob 0.7 --max_pred 64 \
  --train_batch_size 330 --gradient_accumulation_steps 2 \
  --learning_rate 0.00003 --warmup_proportion 0.1 --label_smoothing 0.1 \
  --num_train_epochs 400
```

**When you find it really slow, try ``ddp`` with the following code:**
``` bash
python -m torch.distributed.launch --nproc_per_node 4 biunilm/run_seq2seq.py --do_train --fp16 --amp --num_workers 12 \
  --bert_model bert-base-chinese --new_segment_ids --tokenized_input \
  --data_dir ${DATA_DIR} --src_file train.src --tgt_file train.tgt \
  --output_dir ${OUTPUT_DIR}/bert_save \
  --log_dir ${OUTPUT_DIR}/bert_log \
  --max_seq_length 250 --max_position_embeddings 250 \
  --trunc_seg a --always_truncate_tail --max_len_b 90 \
  --mask_prob 0.7 --max_pred 64 \
  --train_batch_size 330 --gradient_accumulation_steps 2 \
  --learning_rate 0.00003 --warmup_proportion 0.1 --label_smoothing 0.1 \
  --num_train_epochs 400
```

The ``DDP``is much faster than ``DP``.

### Notes about DDP:
When you use ``ctrl-c`` to terminate the training task, you will find that the GPU resources are not correctly released.
*1. use ``nvidia-smi`` to find the pids, and use ``kill -9 pid`` to kill them.
*2. If there are no pids but the GPU memories are still occupied, try
```bash
fuser -v /dev/nvidia*
```
and then kill the zombies.

## Run inference
``` bash
DATA_DIR=/export/shenkai/data/dapei/data_processed_v1/processed
MODEL_RECOVER_PATH=save/bert_save/model.170.bin # your checkpoint path
EVAL_SPLIT=eval
python biunilm/decode_seq2seq.py --amp --bert_model bert-base-chinese --new_segment_ids --mode s2s --need_score_traces \
  --input_file ${DATA_DIR}/${EVAL_SPLIT}.src --split ${EVAL_SPLIT} --tokenized_input \
  --model_recover_path ${MODEL_RECOVER_PATH} \
  --max_seq_length 250 --max_tgt_length 90 \
  --batch_size 64 --beam_size 5 --length_penalty 0 \
  --forbid_duplicate_ngrams --forbid_ignore_word "."
```
The output is saved in the same directory as ``MODEL_RECOVER_PATH``.