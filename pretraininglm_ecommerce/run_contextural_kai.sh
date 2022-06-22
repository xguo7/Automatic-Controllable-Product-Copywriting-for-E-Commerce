DATA_DIR=/export/shenkai/data/dapei/data_kai_v3/processed
OUTPUT_DIR=/export/shenkai/shiina/jd/unilm/unilm-v1/src/save_v3
MODEL_RECOVER_PATH=/export/shenkai/shiina/jd/unilm/unilm-v1/src/pretrain_ckpt/
# export PYTORCH_PRETRAINED_BERT_CACHE=/{tmp_folder}/bert-cased-pretrained-cache
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