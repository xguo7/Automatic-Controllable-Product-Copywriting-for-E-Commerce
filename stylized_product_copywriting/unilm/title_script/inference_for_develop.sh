# run decoding
#DATA_DIR=/mnt/10.252.199.12/home/xiaojie.guo/tmp/1343_produce/processed_data/processed
DATA_DIR=/mnt/10.252.199.12/home/xiaojie.guo/daren_data/671/processed_title/processed
#MODEL_RECOVER_PATH=/home/xiaojie.guo/stylized_personal_write/unilm/save/1343/model.14.bin
MODEL_RECOVER_PATH=/home/xiaojie.guo/Data/unilm_671/title_with_pretrain/bert_save_v4/model.16.bin
EVAL_SPLIT=eval




# export PYTORCH_PRETRAINED_BERT_CACHE=/{tmp_folder}/bert-cased-pretrained-cache
#export CUDA_VISIBLE_DEVICES=0,1,2,3

#eval "ssh occupy 'ps -ef | grep occupy | grep -v grep | grep python | cut -c 9-15 | xargs kill -SIGKILL' >/dev/null 2>&1"

# run decoding
CUDA_VISIBLE_DEVICES='2,3' nohup  python ../decode_seq2seq.py >output_gen \
--bert_model bert-base-chinese \
--new_segment_ids \
--mode s2s \
--need_score_traces  \
--input_file ${DATA_DIR}/${EVAL_SPLIT}.src --split ${EVAL_SPLIT} --tokenized_input \
--model_recover_path ${MODEL_RECOVER_PATH} \
--max_seq_length 250 --max_tgt_length 20 \
--batch_size 128 --beam_size 5 --length_penalty 0 \
--forbid_duplicate_ngrams --forbid_ignore_word "."
