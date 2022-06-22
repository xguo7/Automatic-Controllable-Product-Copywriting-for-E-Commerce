import argparse, os, tqdm


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
        ret.append(s.lower().replace("|||", " [SEP] "))
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
    parser.add_argument("--output_attr", type=str, default="match_ad_word", help="output attribute")
    parser.add_argument("--output_dir_path", default="/export/shenkai/data/dapei/data_kai")
    args = parser.parse_args()


    # read raw data, then extract input and output, respectively.
    raw_tsv_path = os.path.join(args.raw_tsv_dir, "{}.tsv".format(args.split_name))
    input_collect , output_collect = read_tsv(raw_tsv_path, args.input_attr, args.output_attr)
    
    # save original data in ori_dir
    ori_dir = os.path.join(args.output_dir_path, "original")
    os.makedirs(ori_dir, exist_ok=True)
    with open(os.path.join(ori_dir, "{}.src".format(args.split_name)), "w") as f:
        src_str = "\n".join(input_collect)
        f.write(src_str)

    with open(os.path.join(ori_dir, "{}.tgt".format(args.split_name)), "w") as f:
        src_str = "\n".join(output_collect)
        f.write(src_str)

    
    # pre-process: replace "|||" by "\n"
    input_collect = preprocess(input_collect)
    output_collect = preprocess(output_collect)

    # then apply tokenize

    from transformers import BertTokenizer

    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    print("Tokenizing src")
    input_collect_tokenized = tokenize(input_collect, tokenizer)

    # string lize & save
    input_tokenized_str = "\n".join([" ".join(tokens) for tokens in input_collect_tokenized])
    processed_dir = os.path.join(args.output_dir_path, "processed")
    os.makedirs(processed_dir, exist_ok=True)

    with open(os.path.join(processed_dir, "{}.src".format(args.split_name)), "w") as f:
        f.write(input_tokenized_str)

    print("Tokenizing tgt")
    output_collect_tokenized = tokenize(output_collect, tokenizer)
    output_tokenized_str = "\n".join([" ".join(tokens) for tokens in output_collect_tokenized])
    with open(os.path.join(processed_dir, "{}.tgt".format(args.split_name)), "w") as f:
        f.write(output_tokenized_str)

