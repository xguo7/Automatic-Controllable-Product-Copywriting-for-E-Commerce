#run these two options one by one#
Sec_cid=1342
Date=20211202


#nohup /home/xiaojie.guo/anaconda3/envs/personal_write/bin/python -u  /home/xiaojie.guo/stylized_product_copywriting/postprocess/filter_aggregate.py >output \
#--task filter_part \
#--sec_id $Sec_cid \
#--data_path /home/xiaojie.guo/tmp/${Sec_cid}_produce/generated_data/write_${Sec_cid}_${Date}.csv \
#--save_path /home/xiaojie.guo/tmp/${Sec_cid}_produce/generated_data/write_${Sec_cid}_${Date}_clean.csv  \


nohup /home/xiaojie.guo/anaconda3/envs/personal_write/bin/python -u  /home/xiaojie.guo/stylized_product_copywriting/postprocess/filter_aggregate.py >output \
--task aggregate \
--sec_id $Sec_cid \
--data_path /home/xiaojie.guo/tmp/${Sec_cid}_produce/generated_data/write_${Sec_cid}_${Date}_clean.csv \
--save_path /home/xiaojie.guo/tmp/${Sec_cid}_produce/generated_data/write_${Sec_cid}_${Date}_final.csv \