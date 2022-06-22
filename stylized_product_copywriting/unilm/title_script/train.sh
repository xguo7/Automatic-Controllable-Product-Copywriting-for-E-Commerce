DATA_DIR=/mnt/10.252.199.12/home/xiaojie.guo/daren_data/671/processed_title/processed
OUTPUT_DIR=/home/xiaojie.guo/Data/unilm_671/title_with_pretrain
#export CUDA_VISIBLE_DEVICES=0,1,2,3

#eval "ssh occupy 'ps -ef | grep occupy | grep -v grep | grep python | cut -c 9-15 | xargs kill -SIGKILL' >/dev/null 2>&1"
#-m torch.distributed.launch --nproc_per_node 4 
#
CUDA_VISIBLE_DEVICES='2,3' nohup python ../run_seq2seq.py --do_train --fp16 --amp \
--num_workers 0 \
--bert_model /home/xiaojie.guo/Data/unilm_pretrain/model_epoch34/ \
--new_segment_ids --tokenized_input \
--data_dir ${DATA_DIR} --src_file train.src \
--tgt_file train.tgt \
--output_dir ${OUTPUT_DIR}/bert_save_v4 \
--log_dir ${OUTPUT_DIR}/bert_log_v4 \
--max_seq_length 250 --max_position_embeddings 512 \
--trunc_seg a --always_truncate_tail --max_len_b 20 \
--mask_prob 0.7 --max_pred 20 \
--train_batch_size 128 --gradient_accumulation_steps 2 \
--learning_rate 0.00003 --warmup_proportion 0.1 --label_smoothing 0.1 \
--num_train_epochs 400
 