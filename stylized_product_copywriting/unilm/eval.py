from typing import List
from nlgeval import NLGEval
from sumeval.metrics.bleu import BLEUCalculator
from sumeval.metrics.rouge import RougeCalculator
import numpy as np
import warnings


class Eval:
    def __init__(self):
        self.nlgeval = NLGEval(no_skipthoughts=True, no_glove = True)
        self.nlgeval.valid_metrics = {'Bleu_1', 'Bleu_2', 'Bleu_3', 'Bleu_4',
                                'METEOR'
                                }
        self.bleu_scorer = BLEUCalculator(lang="zh")
        self.rouge_scorer = RougeCalculator(lang="zh")
        warnings.warn("Currently the BLEU@1-4 and METEOR metrics are based on pycocoeval, which is for English evaluation. Sacrebleu and Rouge1,2,L metrics are for Chinese evaluation.")
        pass

    def calculate(self, prediction_list : List[str], ground_truth_list: List[str], lda_model_name, lda_dct_path):
        """
            Calculate the automatic evaluation metrics: BLEU@1-4, METEOR, ROUGE1,2,L, Sacrebleu
            Currently the BLEU@1-4 and METEOR metrics are based on pycocoeval, which is for English evaluation. Sacrebleu and Rouge1,2,L metrics are for Chinese evaluation..
            Example:
                >>> tool = Eval()
                >>> prediction_list = ["我是好人", "北京欢迎你"]
                >>> ground_truth_list = ["我今天赖床了", "杭州欢迎您"]
                >>> results = tool.calculate(prediction_list, ground_truth_list)
                >>> print(results)
                >>> {'sacrebleu': 1.6375250515881363, 'rouge_1': 0.25, 'rouge_2': 0.0, 'rouge_L': 0.25, 'bleu_1': 0.21372679609582346, 'bleu_2': 0.13991703159056534, 'bleu_3': 1.3590970311700213e-06, 'bleu_4': 4.812852939642271e-09, 'meteor': 0.10808110962362019}
        parameters：
            prediction_list: List[str]
                The list contains all predictions.
            ground_truth_list: List[str]
                The list contains all references.
        return:
            results_dict: dict
                The dict contains all metrics.
                    {
                        "bleu_1": float, "bleu_2: float, "bleu_3": float, "bleu_4": float, 
                        "meteor": float,
                        "rouge_1": float, "rouge_2": float, "rouge_L": float,
                        "sacrebleu": float
                    }
        """
        sacrebleu_list = []
        rouge_1_list = []
        rouge_2_list = []
        rouge_L_list = []
        for pred, ref in zip(prediction_list, ground_truth_list):
            out = self.bleu_scorer.bleu(summary=pred, references=ref)
            sacrebleu_list.append(out)
            rouge_1_list.append(self.rouge_scorer.rouge_1(pred, ref))
            rouge_2_list.append(self.rouge_scorer.rouge_2(pred, ref))
            rouge_L_list.append(self.rouge_scorer.rouge_l(pred, ref))
        ret = {
            "sacrebleu": np.mean(sacrebleu_list),
            "rouge_1": np.mean(rouge_1_list),
            "rouge_2": np.mean(rouge_2_list),
            "rouge_L": np.mean(rouge_L_list) 
        }
            
        
        

        pred_list = [' '.join([x for x in pred.lower().replace(' ','')]) for pred in prediction_list]
        target_list = [' '.join([x for x in target.lower().replace(' ','')]) for target in ground_truth_list]

        metrics_dict = self.nlgeval.compute_metrics([target_list], pred_list)
        ret["bleu_1"] = metrics_dict["Bleu_1"]
        ret["bleu_2"] = metrics_dict["Bleu_2"]
        ret["bleu_3"] = metrics_dict["Bleu_3"]
        ret["bleu_4"] = metrics_dict["Bleu_4"]
        ret["meteor"] = metrics_dict["METEOR"]


        ret["aspect"] = calculate_aspect(prediction_list, ground_truth_list, lda_model_name, lda_dct_path)

        return ret


tool = Eval()

predicted_file = "/home/xiaojie.guo/Data/unilm_1342/bert_save_v4/model.52.bin.eval"
gt_file = "/mnt/10.252.199.12/home/xiaojie.guo/daren_data/1342/processed_data/processed/eval.tgt"

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
