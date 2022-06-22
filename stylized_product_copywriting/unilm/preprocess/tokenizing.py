import argparse, os, tqdm


def read_tsv(path, input_attr, output_attr):
    ret_input_collect = []
    ret_output_collect = []
    sku_collect = []
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
            if args.for_produce=='produce':
               line_attrs = lines[idx].strip().split("|||")
               #print(len(line_attrs))
            else:
               line_attrs = lines[idx].strip().split("\t")
            #print(args.for_produce)
            
            assert attr_name_cnt == len(line_attrs)
            input_attr = line_attrs[input_attr_idx]
            output_attr = line_attrs[output_attr_idx]
            sku = line_attrs[0]
            ret_input_collect.append(input_attr)
            ret_output_collect.append(output_attr)
            sku_collect.append(sku)
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
    parser.add_argument("--sec_cid", type=str, default='671', help="the second cid of product")
    parser.add_argument("--output_dir_path", default="/export/shenkai/data/dapei/data_kai")
    parser.add_argument("--all_aspect", default=False, type=bool, help="whether for generate all aspect output")
    parser.add_argument("--for_produce", default='train', type=str, help="whether used for produce or develop")
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


    if args.sec_cid == '653':
        aspect_l =[ "机 身 外 观", "屏 幕 音 效", "网 络 5 g", "拍 照 摄 影", "性 能 存 储", "电 池 充 电", "解 锁 识 别"]
    elif args.sec_cid == '1343':
        aspect_l = ["面 料 材 质", "细 节 （ 袖 口 ）", "搭 配 方 式", "风 格 气 质",  "细 节 （ 口 袋 ）", "款 式 版 型", "图 案 花 纹", "细 节 （ 领 口 ）", "细 节 （ 衣 摆 ）"]
    elif args.sec_cid == '1342':
        aspect_l = ["面 料 材 质", "细 节 （ 袖 口 ）", "搭 配 方 式", "风 格 气 质",  "细 节 （ 口 袋 ）", "款 式 版 型", "图 案 花 纹", "细 节 （ 领 口 ）"]
    elif args.sec_cid == '671':
        aspect_l = ["性 能 存 储", "显 卡 处 理", "机 身 外 观", "触 控 协 同",  "屏 幕 摄 像", "键 盘 音 效", "解 锁 安 全", "散 热 风 扇", "续 航 充 电"]
    elif args.sec_cid == '1381':
        aspect_l = ["防 晒 隔 离", "抗 皱 紧 致", "清 洁 控 油", "美 白 淡 斑",  "补 水 保 湿", "修 护 舒 缓", "成 分 质 地", "包 装 设 计"]
    elif args.sec_cid == '794':
        aspect_l = ['除 菌 自 洁', '容 量 多 档', '去 污 烘 干', '保 鲜 除 霜', '画 质 音 效', '制 冷 送 风', '性 能 高 效', '智 能 控 制', '外 观 材 质', '节 能 静 音']

    if args.all_aspect:
        data = []
        save = os.path.join(processed_dir, "{}2.src".format(args.split_name))
        with open(os.path.join(processed_dir, "{}.src".format(args.split_name)), "r") as f:
            for line in f:
                data.append(line.strip())
        with open(save, "w") as f:
            for line in data:
                for key in aspect_l:
                    new_line = key + " [SEP] " + line+ '\n'
                    f.write(new_line)        
    
    if len(args.output_attr)!=0:
        print("Tokenizing tgt")
        output_collect_tokenized = tokenize(output_collect, tokenizer)
        output_tokenized_str = "\n".join([" ".join(tokens) for tokens in output_collect_tokenized])
        with open(os.path.join(processed_dir, "{}.tgt".format(args.split_name)), "w") as f:
            f.write(output_tokenized_str)

