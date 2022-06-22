import csv
from tqdm import tqdm
from collections import defaultdict

def get_sku():
    path = "data/raw/processed_daren653_sku.csv"
    # path = "data/raw/train.csv"
    with open(path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    new_data = defaultdict(lambda:set())
    for line in tqdm(data[1:]):
        new_data[line[0].lower()].add(line[-1])

    # for key in tqdm(new_data):
    #     if len(new_data[key]) > 1:
    #         print(key)
    #         print(new_data[key])

    path = "data/feat/v3/processed/output2.csv"
    with open(path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    save = "data/feat/v3/processed/output2_sku.csv"
    cnt = 0
    with open(save, "w") as f:
        cf = csv.writer(f)
        cf.writerow(data[0] + ["sku"])
        for a in tqdm(data[1:]):
            attr = a[1].split("|||")[-1]
            if attr in new_data:
                sku = list(new_data[attr])[0]
                cf.writerow(a+[sku])
            else:
                cnt += 1
    print(cnt)
get_sku()