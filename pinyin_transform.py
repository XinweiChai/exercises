from xpinyin import Pinyin
import os
import json

p = Pinyin()
x = os.walk("data")
paths = [i for i in x]
paths.reverse()


def rename(name, names, count):
    if name not in names:
        return name
    else:
        count += 1
        name = name.split("_")[0] + "_" + str(count)
        return rename(name, names, count)


table = {}
# for i in paths:
#     names = []
#     for j in i[1] + i[2]:
#         new_name = p.get_pinyin(j, splitter='')
#         new_name = rename(new_name, names, count=0)
#         names.append(new_name)
#         table[os.path.join(i[0], j)] = new_name
#         os.rename(os.path.join(i[0], j), os.path.join(i[0], new_name))


count = 1
# id:1, pId:0, name:"江苏", pinyin:''
for i in os.listdir('data'):
    table[i] = [count, 0, i, p.get_pinyin(i, splitter='')]
    count += 1
    for j in os.listdir('data/' + i):
        table[j] = [count, table[i][0], j, p.get_pinyin(j, splitter='')]
        count += 1
        names = []
        for k in os.listdir('data/' + i + '/' + j):
            x = k.split('.')[0]
            if x not in names:
                names.append(x)
                table[x] = [count, table[j][0], x, p.get_pinyin(x, splitter='')]
                count += 1
contents = list(table.values())

with open('table.json', 'w') as file:
    json.dump(table, file, ensure_ascii=False)
