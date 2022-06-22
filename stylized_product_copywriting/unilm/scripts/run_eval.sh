PAR_DIR=/export/likaijian/gitlab/spc_model/unilm
DATA_DIR=$PAR_DIR/data/feat/v3/processed
OUTPUT_DIR=save
recover_step=15
export CUDA_VISIBLE_DEVICES=0,1,2,3

eval "ssh occupy 'ps -ef | grep occupy | grep -v grep | grep python | cut -c 9-15 | xargs kill -SIGKILL' >/dev/null 2>&1"

python -m torch.distributed.launch --nproc_per_node 4 --master_port 29501 biunilm/run_eval.py --do_train --fp16 --amp --num_workers 12 \
  --bert_model bert-base-chinese --new_segment_ids --tokenized_input \
  --recover_step $recover_step \
  --data_dir ${DATA_DIR} --src_file eval.src --tgt_file eval.tgt \
  --output_dir ${OUTPUT_DIR}/bert_save_v3 \
  --log_dir ${OUTPUT_DIR}/bert_log_v3 \
  --max_seq_length 512 --max_position_embeddings 512 \
  --trunc_seg a --always_truncate_tail --max_len_b 90 \
  --mask_prob 0.7 --max_pred 90 \
  --train_batch_size 32 --gradient_accumulation_steps 1 \
  --learning_rate 0.00003 --warmup_proportion 0.1 --label_smoothing 0.1 \
  --num_train_epochs 400
