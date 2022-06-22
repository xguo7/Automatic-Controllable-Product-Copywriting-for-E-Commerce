
with open('/home/xiaojie.guo/daren_data/daren653_split.csv', encoding = 'utf-8') as f:
    data = f.readlines()
items=[]
for item in data:
    items.append(item.split('\t'))
from utils import *

for i in items[:1000]:
  if i[22]!= 'NULL\n':
     print(i[22])

nohup python process_daren.py clean /home/xiaojie.guo/daren_data/daren653_split.csv  /home/xiaojie.guo/daren_data/daren653_clean.csv