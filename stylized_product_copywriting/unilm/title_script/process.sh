# this file is used to seperate the .tst file to .tgt and .src file

Sec_cid=1342
Date=20211202
PAR_DIR=/mnt/10.252.199.12/home/xiaojie.guo/tmp/${Sec_cid}_produce
Raw_tsv_dir=$PAR_DIR/generated_data/write_${Sec_cid}_${Date}_final.csv
Input_attr=sku_title_write
#Output_attr= 
Output_dir_path=$PAR_DIR/processed_title/
#mkdir -p $Output_dir_path
# eval "ssh occupy 'ps -ef | grep occupy | grep -v grep | grep python | cut -c 9-15 | xargs kill -SIGKILL' >/dev/null 2>&1"

python ../preprocess/tokenizing_title.py --split_name test --raw_tsv_dir $Raw_tsv_dir --input_attr $Input_attr  --output_dir_path $Output_dir_path --for_produce produce
#