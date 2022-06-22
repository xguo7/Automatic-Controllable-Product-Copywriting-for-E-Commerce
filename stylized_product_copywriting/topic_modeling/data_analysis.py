import openpyxl

#read data
path='/home/xiaojie.guo/daren_data/'
workbook1=openpyxl.load_workbook(path+'assigned_topic_1343_part1.xlsx')
workbook2=openpyxl.load_workbook(path+'assigned_topic_1343_part2.xlsx')
topic_data1=workbook1.worksheets[0]
topic_data2=workbook2.worksheets[0]
class_l=list(topic_data1.rows)[1:]+list(topic_data2.rows)[1:]
amount = {}
good_amount = {}
for i in range(13):
    amount[i]=0
    good_amount[i]=0
for sample in class_l:
    amount[sample[1].value]+=1
    if sample[2].value>0.6:
        good_amount[sample[1].value]+=1
print(amount)
print(good_amount)
print(sum(amount))
print(sum(good_amount))