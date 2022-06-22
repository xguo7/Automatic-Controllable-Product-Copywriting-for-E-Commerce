
#nohup python process_daren_1342.py split /home/xiaojie.guo/daren_data/794/data_794_train.csv /home/xiaojie.guo/daren_data/794/daren794_split.csv >output 2>&1 & 
#nohup python process_daren_1342.py clean /home/xiaojie.guo/daren_data/794/daren794_split.csv /home/xiaojie.guo/daren_data/794/daren794_clean.csv >output 2>&1 &
nohup python process_daren_1342.py clean_with_title /home/xiaojie.guo/daren_data/794/daren794_split.csv /home/xiaojie.guo/daren_data/794/daren794_clean_title.csv >output 2>&1 &