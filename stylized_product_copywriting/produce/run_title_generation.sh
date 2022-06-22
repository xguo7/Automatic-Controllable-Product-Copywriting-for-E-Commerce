#CUDA_VISIBLE_DEVICES='0,1,2,3' nohup /home/xiaojie.guo/anaconda3/envs/personal_write/bin/python -u  /home/xiaojie.guo/stylized_product_copywriting/title_generation/gpt/generate.py >output_gen \
#--model_dir /home/xiaojie.guo/daren_data/title_653/gpt_pw/ \
#--model_id gpt-Sep_13_16_17_56 \
#--model_epoch 7 \
#--tokenizer /home/xiaojie.guo/stylized_product_copywriting/title_generation/gpt/cache/bert-base-chinese/vocab.txt \
#--data_dir /home/xiaojie.guo/daren_data/title_653/theme_pw \
#--data_mode test_df \
#--uniq_column sku \
#--output_file /home/xiaojie.guo/tmp/653_produce/generated_write_title/write_title_653_20211013.csv \
#--test_df /home/xiaojie.guo/tmp/653_produce/generated_data/write_653_20211013_final.csv  \

CUDA_VISIBLE_DEVICES='0' nohup /home/xiaojie.guo/anaconda3/envs/personal_write/bin/python -u  /home/xiaojie.guo/stylized_product_copywriting/title_generation/gpt/generate.py >output_gen \
--model_dir /home/xiaojie.guo/daren_data/1343/title_1343/gpt_pw/ \
--model_id gpt-Sep_21_19_43_24 \
--model_epoch 12 \
--tokenizer /home/xiaojie.guo/stylized_product_copywriting/title_generation/gpt/cache/bert-base-chinese/vocab.txt \
--data_dir /home/xiaojie.guo/daren_data/title_1343/theme_pw \
--data_mode test_df \
--uniq_column sku \
--output_file /home/xiaojie.guo/tmp/1343_produce/generated_write_title/write_title_1343_20211030.csv \
--test_df /home/xiaojie.guo/tmp/1343_produce/generated_data/write_1343_20211030_final.csv  \