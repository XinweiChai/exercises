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
for i in paths:
    names = []
    for j in i[1] + i[2]:
        new_name = p.get_pinyin(j, splitter='')
        new_name = rename(new_name, names, count=0)
        names.append(new_name)
        table[os.path.join(i[0], j)] = new_name
        os.rename(os.path.join(i[0], j), os.path.join(i[0], new_name))
with open('table.json', 'a') as file:
    json.dump(table, file, ensure_ascii=False)
