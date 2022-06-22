# stylized_product_copywriting

This project is to generate a stylized product copywriting (for single product).

## Data download
1. Download data from 达人：
   
         run /data_download/get_daren_653.pig
   
2. Download data from OCR:
   
         run /data_download/get_ocr_653.pig 

For the process in generating the immideiate table of daren data: https://git.jd.com/jd_smart_shopping/stylized_product_copywriting/tree/data-likaijian/collect/hive


## Data preprocess

1. Deal with data from the source from 达人：

         run python /preprocess/process_daren.py split daren653.csv  splitted_daren653.csv
         
         run python /preprocess/process_daren.py clean splitted_daren653.csv  clean_daren653.csv

2. Deal with the data from source OCR:



3. Get the attribute as topics:

         run python process_daren.py get_attr daren653.csv   attribute653.csv


