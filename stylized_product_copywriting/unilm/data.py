import csv
import time


def process_line(line):
    for i in range(3):
        line[i] = line[i].replace(",", " ")


def process_file(src_path, save_path):
    with open(src_path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    with open(save_path, "w") as f:
        f.write("\t".join(data[0]) + "\n")
        for line in data[1:]:
            process_line(line)
            f.write("\t".join(line) + "\n")


# 测试只用品牌型号做输入的数据处理
def process_file2(src_path, save_path):
    def process(line):
        line[0] = ",".join(line[0].split(",")[:3])
        line[1] = line[1].split("|||")[0] + "|||" + line[0]
        line[2] = line[2].split("|||")[0] + "|||" + line[0]
    with open(src_path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    with open(save_path, "w") as f:
        f.write("\t".join(data[0]) + "\n")
        for line in data[1:]:
            process(line)
            f.write("\t".join(line) + "\n")


# 重新分割后的tsv数据处理
def process_file3(src_path, save_path):
    with open(src_path, "r") as f:
        data = []
        for line in f:
            data.append(line.strip())
    with open(save_path, "w") as f:
        f.write("attr\taspect\tcode\twrite\tsku\n")
        for line in data:
            attr, aspect, code, write, sku = line.split("\t")
            f.write(attr + "\t" + aspect + "|||" + attr + "\t" + code + "|||" + attr + "\t" + write + "\t" + sku + "\n")




def remove_(s, a, b):
    res = ""
    if a in s:
        s = s.split(a)
        for i in s:
            i = i.split(b)
            res += i[-1]
    else:
        res = s
    return res


def remove_s(s, a):
    if a in s:
        s = s.split(a)
        s = s[1].strip(" ")
    return s


def _count(path):
    with open(path, "r") as f:
        data = f.readlines()
    max_l = 0
    for line in data:
        line = line.strip()
        line = line.split(" ")
        a = len(line)
        if a > max_l:
            max_l = a
    print(max_l)


def count():
    path = "data/feat/v3/processed/eval.tgt"
    _count(path)


def _cut(src_path, tgt_path, max_l=512-3):
    with open(src_path, "r") as fs:
        with open(tgt_path, "r") as ft:
            src_data = fs.readlines()
            tgt_data = ft.readlines()
    
    assert len(src_data) == len(tgt_data)
    with open(src_path, "w") as fs:
        l = len(src_data)
        for i in range(l):
            src_line = src_data[i].strip()
            tgt_line = tgt_data[i].strip()
            l_tgt = len(tgt_line.split(" "))
            src_list = src_line.split(" ")
            src_list = src_list[:(max_l - l_tgt)]
            src_line = " ".join(src_list)
            fs.write(src_line + "\n")


def cut():
    src_path = "data/feat/v1/processed/train.src"
    tgt_path = "data/feat/v1/processed/train.tgt"
    _cut(src_path, tgt_path)


def main():
    src_path = "data/raw/1343/test.tsv"
    save_path = "data/processed/1343/v1/test.tsv"
    process_file3(src_path, save_path)


def token():
    from transformers import BertTokenizer
    tokenizer = BertTokenizer.from_pretrained("config/vocab.txt")
    a = "易百年EZ908老年手机 国产770芯片 前后双摄 512MB+32GB 玫瑰金 移动联通电信4G手机 双卡双待全网通（512MB 32GB）玫瑰金支持存储卡 3.5英寸屏幕 录音机 不支持无线充电 T9传统键盘 超大音量 一键报警 非触控 不支持5G 3.5英寸 塑料后盖 前置300万像素 后置200像素 2000mAh大电池 120g超轻机身 可拆卸电池 后置单摄 国产770"
    res = tokenizer.tokenize(a)
    a = " ".join(res)
    print(a)


def get_part():
    for i in ["train", "validation", "test"]:
        src_path = "data/raw/" + i + ".csv"
        save_path = "data/processed/v2/" + i + ".txt"
        with open(src_path, "r") as f:
            reader = csv.reader(f)
            data = list(reader)
        with open(save_path, "w") as f:
            for line in data[1:]:
                a = line[0].split(",")
                res = a[0]
                for i in a[1:]:
                    if len(res) < 25:
                        res += "," + i
                    else:
                        break
                f.write(res + "\n")


def test():
    a = "魅族（MEIZU）,PRO7标准版,全网通4G手机,双卡双待,提香红,(4G,RAM+128G,ROM）(4G,RAM+128G,ROM）提香红双卡双待单通,金属后盖,5.2英寸,WiFi热点,MTKP系列,金属边框,录音,蓝牙"
    a = a.replace("（", "(")
    a = a.replace("）", ")")
    a = remove_(a, "【", "】")
    a = remove_(a, "（", "）")
    a = remove_(a, "(", ")")
    print(a)


def all_aspect():
    # required by xiaojie
    path = "data/feat/v3/processed/test.src"
    data = set()
    with open(path, "r" ) as f:
        for line in f:
            line = line.strip()
            attr = line.split(" [SEP] ")
            assert len(attr) == 2
            attr = attr[1]
            data.add(attr)
    save = "data/feat/v3/processed/test2.src"
    with open(save, "w") as f:
        for line in data:
            for key in ["机 身 外 观", "屏 幕 音 效", "网 络 5 g", "拍 照 摄 影", "性 能 存 储", "电 池 充 电", "解 锁 识 别"]:
                new_line = key + " [SEP] " + line + "\n"
                f.write(new_line)


def merge_xiaojie():
    a = "save/bert_save_v3/model.15.txt2"
    with open(a, "r") as f:
        data = []
        for line in f:
            line = line.strip()
            data.append(line)

    b = "data/feat/v3/processed/test2.src"
    with open(b, "r") as f:
        data_ = []
        for line in f:
            line = line.strip()
            line = line.replace(" ##", "")
            line = line.replace(" ", "")
            line = line.replace("[SEP]", "|||")
            data_.append(line)

    c = "data/feat/v3/processed/output2.csv"
    with open(c, "w") as f:
        cf = csv.writer(f)
        cf.writerow(["pred", "product"])
        for a, b in zip(data, data_):
            line = [a, b]
            cf.writerow(line)



if __name__ == "__main__":
    a = time.time()

    main()
    # get_part()
    # count()
    # cut()
    # token()
    # test()
    all_aspect()
    # merge_xiaojie()

    a = time.time() -a 
    print("Finished!")
    print("Time: " + str(a) + "s")