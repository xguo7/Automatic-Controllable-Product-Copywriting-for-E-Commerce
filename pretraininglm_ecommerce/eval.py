import sys
sys.path.insert(0, "/export/shenkai/shiina/jd/evaluation")
from eval_tool import Eval
tool = Eval()

predicted_file = "save_title_v7/bert_save/model.100.bin.eval"
gt_file = "/export/shenkai/data/dapei/data_title_processed_v7/original/eval.tgt"

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.readlines()
    return content

def remove_blank(lines):
    return [l.replace(" ", "") for l in lines]

predicted_lines = remove_blank(load_file(predicted_file))
gt_lines = remove_blank(load_file(gt_file))

assert len(predicted_lines) == len(gt_lines)


results = tool.calculate(predicted_lines, gt_lines)
print(results) # 
