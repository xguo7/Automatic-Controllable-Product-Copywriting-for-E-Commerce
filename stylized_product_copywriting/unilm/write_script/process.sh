# this file is used to seperate the .tst file to .tgt and .src file

Sec_cid=1342
PAR_DIR=/mnt/10.252.199.12/home/xiaojie.guo/tmp/1342_produce
Raw_tsv_dir=$PAR_DIR/orig_data/data_1342_20211202_clean.csv
Input_attr=product
#Output_attr= 
Output_dir_path=$PAR_DIR/processed_data/
#mkdir -p $Output_dir_path
# eval "ssh occupy 'ps -ef | grep occupy | grep -v grep | grep python | cut -c 9-15 | xargs kill -SIGKILL' >/dev/null 2>&1"

python ../preprocess/tokenizing.py --split_name test --for_produce produce --sec_cid $Sec_cid --raw_tsv_dir $Raw_tsv_dir --input_attr $Input_attr  --all_aspect True --output_dir_path $Output_dir_path
