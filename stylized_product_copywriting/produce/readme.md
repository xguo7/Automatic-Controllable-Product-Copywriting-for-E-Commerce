过程中所有生产的数据都保存在12的tmp文件夹下

1. 处理刚拉取的数据 nohup python preprocess_1343.py /home/xiaojie.guo/tmp/1343_produce/orig_data/data_1343_20211030.csv /home/xiaojie.guo/tmp/1343_produce/orig_data/data_1343_20211030_clean.csv >output 2>&1 & 

2. 生成write： 
      (1)在.4机器上预处理 sh process.sh (/home/xiaojie.guo/stylized_personal_write/unilm/script, 输入data_653_20211013_clean.csv 输出test2.src)
      (2)在.4机器上做生成  inference.sh （/home/xiaojie.guo/stylized_personal_write/unilm/, 输入test2.src，）
      (3)在.4机器上配sku整理输出 combine_sku_prodcut.py (/home/xiaojie.guo/stylized_personal_write/unilm/, 输入是生成的内容，以及orig_data， 输出/home/xiaojie.guo/tmp/653_produce/generated_data/write_653_20211013.csv)
      (4)在.12机器上后处理 sh run_postprocess.sh (run both the two steps: filter/aggregate) 
          write_653_20211013.csv-->write_653_20211013_clean.csv--->write_653_20211013_final.csv

3. title生产：
   GPT:
      (1) 生成标题 sh run_title_generation.sh  write_653_20211013_final.csv-->write_title_653_20211013.csv
      (2) 将标题后处理，并根据sku与文案配起来： python postprocess_title.py write_title_653_20211013.csv--->generation_653_20211013.txt
      (3)对比实验 拆分数据，每个集合6000个数据 （其中一半把标题中的一部分换成中心词）这一步只在对比实验时候做
      python split_test.py
      generation_653_20211013.txt-->generation_653_20211013_1.txt, generation_653_20211013_2.txt, generation_653_20211013_3.txt, generation_653_20211013_4.txt...
   unilm:
       (1)在.4机器上title_script文件夹里预处理 sh process.sh (/home/xiaojie.guo/stylized_personal_write/unilm/title_script, 输入 data_653_20211013_clean.csv 输出test2.src)
       (2)在.4机器上做生成  inference.sh （/home/xiaojie.guo/stylized_personal_write/title_scripts/, 输入test.src，）
       (3)在.4机器上配sku整理输出 process_title.py, 输出直接保存在t12机子tmp里。
             

4. 转到堡垒机做上传


      