# this file is used to seperate the .tst file to .tgt and .src file

Sec_cid=794
PAR_DIR=/mnt/10.252.199.12/home/xiaojie.guo/daren_data/$Sec_cid
Raw_tsv_dir_train=$PAR_DIR/train.csv
Raw_tsv_dir_test=$PAR_DIR/test.csv
Raw_tsv_dir_eval=$PAR_DIR/eval.csv
#Input_attr= product_name
#Output_attr= write
Output_dir_path=$PAR_DIR/processed_data/
#mkdir -p $Output_dir_path
# eval "ssh occupy 'ps -ef | grep occupy | grep -v grep | grep python | cut -c 9-15 | xargs kill -SIGKILL' >/dev/null 2>&1"

#python ../preprocess/tokenizing_1342.py --split_name train --raw_tsv_dir $Raw_tsv_dir_train --input_attr product_name  --output_attr write --output_dir_path $Output_dir_path 
python ../preprocess/tokenizing.py --split_name eval --for_produce train --sec_cid $Sec_cid --raw_tsv_dir $Raw_tsv_dir_eval --input_attr product_name --output_attr write --output_dir_path $Output_dir_path
python ../preprocess/tokenizing.py --split_name train --for_produce train --sec_cid $Sec_cid --raw_tsv_dir $Raw_tsv_dir_train --input_attr product_name --output_attr write --output_dir_path $Output_dir_path
