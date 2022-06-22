'''xiaojie guo'''



all_data = []
folder_path = '../daren_data/'

for i in range(7):
    with open(folder_path+'part-r-0000'+str(i), 'r', encoding = 'utf-8') as f:
        data = f.readlines()
        all_data.extend(data)


with open('653.csv', 'w', encoding = 'utf-8') as f:
    for item in all_data:
        f.write(item)
