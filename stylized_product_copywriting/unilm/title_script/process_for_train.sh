# this file is used to seperate the .tst file to .tgt and .src file


PAR_DIR=/mnt/10.252.199.12/home/xiaojie.guo/daren_data/794
Raw_tsv_dir_train=$PAR_DIR/train_title.csv
Raw_tsv_dir_test=$PAR_DIR/test_title.csv
Raw_tsv_dir_eval=$PAR_DIR/eval_title.csv

Output_dir_path=$PAR_DIR/processed_title/
#mkdir -p $Output_dir_path
# eval "ssh occupy 'ps -ef | grep occupy | grep -v grep | grep python | cut -c 9-15 | xargs kill -SIGKILL' >/dev/null 2>&1"

python ../preprocess/tokenizing_title.py --split_name train --raw_tsv_dir $Raw_tsv_dir_train --input_attr write_product  --output_attr title --output_dir_path $Output_dir_path --for_produce train
#python ../preprocess/tokenizing_title.py --split_name eval --raw_tsv_dir $Raw_tsv_dir_eval --input_attr write_product --output_attr title --output_dir_path $Output_dir_path --for_produce train
#python ../preprocess/tokenizing_1342.py --split_name train --raw_tsv_dir $Raw_tsv_dir_train --all_aspect True --input_attr product_name  --output_dir_path $Output_dir_path
