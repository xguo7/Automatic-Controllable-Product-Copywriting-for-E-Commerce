import argparse, os, tqdm
import pandas as pd

def read_tsv(path, input_attr, output_attr):
    ret_input_collect = []
    ret_output_collect = []
    with open(path, "r") as f:
        lines = f.readlines()
        attr_name_cnt = len(lines[0].split("\t"))
        print("attr_cnt", attr_name_cnt)
        input_attr_idx = 0
        output_attr_idx = 0
        for idx, i in enumerate(lines[0].strip().split("\t")):
            print("*******", i, idx)
            if i == input_attr:
                input_attr_idx = idx
            elif i == output_attr:
                output_attr_idx = idx
        print("input attr idx", input_attr_idx)
        print("output attr idx", output_attr_idx)

        for idx in range(1, len(lines)):
            if lines[idx].strip() == "":
                continue
            line_attrs = lines[idx].strip().split("\t")
            assert attr_name_cnt == len(line_attrs)
            input_attr = line_attrs[input_attr_idx]
            output_attr = line_attrs[output_attr_idx]
            ret_input_collect.append(input_attr)
            ret_output_collect.append(output_attr)
    return ret_input_collect, ret_output_collect


def preprocess(str_list):
    ret = []
    for s in str_list:
        ret.append(s.lower().replace("|", ","))
        # ret.append(s.lower().replace("|||", " [SEP] "))
    return ret

def tokenize(str_list, tokenizer):
    ret = []
    for s in tqdm.tqdm(str_list):
        token_list = tokenizer.tokenize(s)
        ret.append(token_list)
    return ret

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--split_name", default="eval", type=str, help="Expect in ['train', 'eval']")
    parser.add_argument("--raw_tsv_dir", default="/export/shenkai/data/dapei/data_v1", type=str)
    parser.add_argument("--input_bi", type=str, default="title", help="input_bi")
    parser.add_argument("--output_bi", type=str, default="attr", help="output_bi")
    parser.add_argument("--nsp_bi", type=str, default="nsp", help="nsp_bi")
    parser.add_argument("--output_uni", type=str, default="recommend_reason", help="output_uni")
    parser.add_argument("--input_s2s", type=str, default="input", help="input_s2s")
    parser.add_argument("--output_s2s", type=str, default="recommend_reason", help="output_s2s")
    parser.add_argument("--output_dir_path", default="/export/shenkai/data/dapei/data_kai")
    args = parser.parse_args()

    ## bi: bi.src, bi.tgt, bi.nsp
    ## uni: uni.tgt
    ## s2s: s2s.src, s2s.tgt
    bi_tsv_path = os.path.join(args.raw_tsv_dir, 'bi.tsv')
    uni_tsv_path = os.path.join(args.raw_tsv_dir, 'uni.tsv')
    s2s_tsv_path = os.path.join(args.raw_tsv_dir, 's2s.tsv')
    df_bi = pd.read_csv(bi_tsv_path, sep = '\t')
    df_uni = pd.read_csv(uni_tsv_path, sep = '\t')
    df_s2s = pd.read_csv(s2s_tsv_path, sep = '\t')
    bi_src = list(df_bi[args.input_bi])
    bi_tgt = list(df_bi[args.output_bi])
    bi_nsp = list(df_bi[args.nsp_bi])
    uni_tgt = list(df_uni[args.output_uni])
    s2s_src = list(df_s2s[args.input_s2s])
    s2s_tgt = list(df_s2s[args.output_s2s])

    
    # save original data in ori_dir
    ori_dir = os.path.join(args.output_dir_path, "original")
    os.makedirs(ori_dir, exist_ok=True)
    with open(os.path.join(ori_dir, "bi.src"), "w") as f:
        x_str = "\n".join(bi_src)
        f.write(x_str)
    with open(os.path.join(ori_dir, "bi.tgt"), "w") as f:
        x_str = "\n".join(bi_tgt)
        f.write(x_str)
    with open(os.path.join(ori_dir, "bi.nsp"), "w") as f:
        x_str = "\n".join([str(a) for a in bi_nsp])
        f.write(x_str)
    with open(os.path.join(ori_dir, "uni.tgt"), "w") as f:
        x_str = "\n".join(uni_tgt)
        f.write(x_str)
    with open(os.path.join(ori_dir, "s2s.src"), "w") as f:
        x_str = "\n".join(s2s_src)
        f.write(x_str)
    with open(os.path.join(ori_dir, "s2s.tgt"), "w") as f:
        x_str = "\n".join(s2s_tgt)
        f.write(x_str)




    bi_src = preprocess(bi_src)
    bi_tgt = preprocess(bi_tgt)
    uni_tgt = preprocess(uni_tgt)
    s2s_src = preprocess(s2s_src)
    s2s_tgt = preprocess(s2s_tgt)


    # then apply tokenize

    from transformers import BertTokenizer

    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")

    processed_dir = os.path.join(args.output_dir_path, "processed")
    os.makedirs(processed_dir, exist_ok=True)


    print("Tokenizing bi src")
    bi_src_tokenized = tokenize(bi_src, tokenizer)
    with open(os.path.join(processed_dir, "bi.src"), "w") as f:
        tokenized_str = "\n".join([" ".join(tokens) for tokens in bi_src_tokenized])
        f.write(tokenized_str)

    print("Tokenizing bi tgt")
    bi_tgt_tokenized = tokenize(bi_tgt, tokenizer)
    with open(os.path.join(processed_dir, "bi.tgt"), "w") as f:
        tokenized_str = "\n".join([" ".join(tokens) for tokens in bi_tgt_tokenized])
        f.write(tokenized_str)

    with open(os.path.join(processed_dir, "bi.nsp"), "w") as f:
        x_str = "\n".join([str(a) for a in bi_nsp])
        f.write(x_str)

    print("Tokenizing uni tgt")
    uni_tgt_tokenized = tokenize(uni_tgt, tokenizer)    
    with open(os.path.join(processed_dir, "uni.tgt"), "w") as f:
        tokenized_str = "\n".join([" ".join(tokens) for tokens in uni_tgt_tokenized])
        f.write(tokenized_str)

    print("Tokenizing s2s src")
    s2s_src_tokenized = tokenize(s2s_src, tokenizer)      
    with open(os.path.join(processed_dir, "s2s.src"), "w") as f:
        tokenized_str = "\n".join([" ".join(tokens) for tokens in s2s_src_tokenized])
        f.write(tokenized_str)

    print("Tokenizing s2s tgt")
    s2s_tgt_tokenized = tokenize(s2s_tgt, tokenizer)      
    with open(os.path.join(processed_dir, "s2s.tgt"), "w") as f:
        tokenized_str = "\n".join([" ".join(tokens) for tokens in s2s_tgt_tokenized])
        f.write(tokenized_str)


