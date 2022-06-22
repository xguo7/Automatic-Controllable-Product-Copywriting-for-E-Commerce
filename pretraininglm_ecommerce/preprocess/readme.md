## The preprocessing procedure

### Data Preparation
``` bash
Attrbute_Name_1 \t Attrbute_Name_2 \t ... \t Attrbute_Name_N
xxxx \t yyyy \t ... \t zzzz
```
Please make sure that the training folder(Raw_tsv_dir) contains ``bi.tsv``, ``uni.tsv``,``s2s.tsv``

Please specify the input and output attributes' name. 

- Bi-direction: bi.tsv, need to specify attribute name for input(bi_seq1_name), output(bi_seq2_name), nsp(nsp_name).
- Uni-direction: uni.tsv, need to specify attribute name for output(uni_seq_name).
- S2S: s2s.tsv, need to specify attribute name for input(s2s_seq1_name), output(s2s_seq2_name).

### Run Preprocessing
``` bash
python preprocess.py --raw_tsv_dir $Raw_tsv_dir --output_dir_path $Output_dir_path \
--input_bi $bi_seq1_name --output_bi $bi_seq2_name --nsp_bi $nsp_name \
--output_uni $uni_seq_name \
--input_s2s $s2s_seq1_name --output_s2s $s2s_seq2_name \


```