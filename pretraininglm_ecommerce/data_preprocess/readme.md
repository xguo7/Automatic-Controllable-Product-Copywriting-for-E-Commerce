
# Data Collection and Preprocessing for Pretraining

## Download Data from database

### Download Daren Data
``` bash
%DEFAULT output '/user/recsys/rank_dev/zhangxueying17/smart_shopping/pretrain_all_select/'
ware = load 'app.app_text_writing_generation_pretraining_concat_pool_daren' using org.apache.hive.hcatalog.pig.HCatLoader();
j = foreach ware generate id,sku,sku_title,brandname_full,item_second_cate_name, attr2_value_name,recommend_theme,recommend_reason,status,source,split_tag;
rmf $output;
store j into '$output' using PigStorage('\t', '-schema');
```

### Download OCR Data
``` bash
%DEFAULT output '/user/recsys/rank_dev/zhangxueying17/smart_shopping/pretrain_ocr/'
ware = load 'app.app_text_writing_generation_pretraining_concat_pool' using org.apache.hive.hcatalog.pig.HCatLoader();
j = foreach ware generate $0..;
rmf $output;
store j into '$output' using PigStorage('\t', '-schema');
```

## Build Dataset for Pretraining
### Filter and Preprocess Data
### Select and Split Data to different tasks

After running data_preprocess.py successfully, the training folder should contain ``bi.tsv``, ``uni.tsv``,``s2s.tsv``

In current setting, the corresponding attributes are as follow:
- Bi-direction: bi.tsv
    1. input： title
    2. output： attr
    3. nsp: nsp
- Uni-direction: uni.tsv
    1. output: recommend_reason
- S2S: s2s.tsv
    1. input: input
    2. output: recommend_reason
