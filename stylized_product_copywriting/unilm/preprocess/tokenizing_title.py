import argparse, os, tqdm
import pandas as pd

def read_tsv(path, input_name, output_name):
    ret_input_collect = []
    ret_output_collect = []
    sku_collect = []
    if args.for_produce  == 'produce':
        df = pd.read_csv(path, sep=',')
    else:
        df = pd.read_csv(path, sep='\t')
    for row in df.iterrows():
            input_attr=row[1][input_name]
            if output_name == '':
                output_attr=''
            else:
              output_attr= row[1][output_name]              
            sku=row[1]['sku']
            if isinstance(output_attr, str): 
                ret_input_collect.append(input_attr) 
                sku_collect.append(sku)
                ret_output_collect.append(output_attr)            
    return ret_input_collect, ret_output_collect, sku_collect


def preprocess(str_list):
    ret = []
    for s in str_list:
        ret.append(s.lower().replace("|||", " [SEP] ", 1))
    return ret

def preprocess2(str_list):
    ret = []
    for s in str_list:
        a = s.lower().replace("|||", " [SEP] ", 1)
        b = a.split("[SEP]")
        if len(b) == 1:
            ret.append(a)
        else:
            c = ""
            for i in b[0]:
                c += i + " "
            b[0] = c
            ret.append("[SEP]".join(b))
    return ret

def tokenize(str_list, tokenizer):
    ret = []
    for s in tqdm.tqdm(str_list):
        token_list = tokenizer.tokenize(s)
        ret.append(token_list)
    return ret

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--split_name", default="eval", type=str, help="Expect in ['train', 'eval']")
    parser.add_argument("--raw_tsv_dir", default="/export/shenkai/data/dapei/data_v1", type=str)
    parser.add_argument("--input_attr", type=str, default="atitle_add_mergetitle", help="input attribute")
    parser.add_argument("--output_attr", type=str, default='', help="output attribute")
    parser.add_argument("--output_dir_path", default="/export/shenkai/data/dapei/data_kai")
    parser.add_argument("--all_aspect", default=False, type=bool, help="whether for generate all aspect output")
    parser.add_argument("--for_produce", default='produce', type=str, help="whether used for produce or develop")
    args = parser.parse_args()


    # read raw data, then extract input and output, respectively.
    #raw_tsv_path = os.path.join(args.raw_tsv_dir, "{}.tsv".format(args.split_name))
    input_collect , output_collect, sku = read_tsv(args.raw_tsv_dir, args.input_attr, args.output_attr)
    
  
    # save original data in ori_dir
    ori_dir = os.path.join(args.output_dir_path, "original")
    os.makedirs(ori_dir, exist_ok=True)
    with open(os.path.join(ori_dir, "{}.src".format(args.split_name)), "w") as f:
        src_str = "\n".join(input_collect)
        f.write(src_str)

    if len(args.output_attr)!=0:
       with open(os.path.join(ori_dir, "{}.tgt".format(args.split_name)), "w") as f:
           tgt_str = "\n".join(output_collect)
           f.write(tgt_str)
    
    
    # pre-process: replace "|||" by "\n"
    input_collect = preprocess2(input_collect)
    output_collect = preprocess2(output_collect)

    # then apply tokenize

    from transformers import BertTokenizer

    # tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    tokenizer = BertTokenizer.from_pretrained("/mnt/10.252.199.12/home/xiaojie.guo/stylized_product_copywriting/generation/conditionalT5/cache/bert-base-chinese/vocab.txt")


    print("Tokenizing src")
    input_collect_tokenized = tokenize(input_collect, tokenizer)
    # string lize & save
    input_tokenized_str = "\n".join([" ".join(tokens) for tokens in input_collect_tokenized])
    processed_dir = os.path.join(args.output_dir_path, "processed")
    os.makedirs(processed_dir, exist_ok=True)
    with open(os.path.join(processed_dir, "{}.src".format(args.split_name)), "w") as f:
        f.write(input_tokenized_str)

    if args.all_aspect:
        data = []
        save = os.path.join(processed_dir, "{}2.src".format(args.split_name))
        with open(os.path.join(processed_dir, "{}.src".format(args.split_name)), "r") as f:
            for line in f:
                data.append(line.strip())
        with open(save, "w") as f:
            for line in data:
                for key in ["面 料 材 质", "细 节 （ 袖 口 ）", "搭 配 方 式", "风 格 气 质",  "细 节 （ 口 袋 ）", "款 式 版 型", "图 案 花 纹", "细 节 （ 领 口 ）"]:
                    new_line = key + " [SEP] " + line+ '\n'
                    f.write(new_line)        
    
    if len(args.output_attr)!=0:
        print("Tokenizing tgt")
        output_collect_tokenized = tokenize(output_collect, tokenizer)
        output_tokenized_str = "\n".join([" ".join(tokens) for tokens in output_collect_tokenized])
        with open(os.path.join(processed_dir, "{}.tgt".format(args.split_name)), "w") as f:
            f.write(output_tokenized_str)

