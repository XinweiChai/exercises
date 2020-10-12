from xpinyin import Pinyin
import os
import json

p = Pinyin()
path = "data/3-level/"
x = os.walk(path)
paths = [i for i in x]
paths.reverse()


def rename(name, names, count):
    if name not in names:
        return name
    else:
        count += 1
        name = name.split("_")[0] + "_" + str(count)
        return rename(name, names, count)


def to_pinyin():
    table = {}
    for i in paths:
        names = []
        for j in i[1] + i[2]:
            new_name = p.get_pinyin(j, splitter='')
            new_name = rename(new_name, names, count=0)
            names.append(new_name)
            table[os.path.join(i[0], j)] = new_name
            os.rename(os.path.join(i[0], j), os.path.join(i[0], new_name))


def dependent_tree():
    table = {}
    table2 = []
    count = 1

    for i in os.listdir(path):
        table[i] = [count, 0, i, p.get_pinyin(i, splitter=''), p.get_pinyin(i, splitter='')]
        table2.append({'id': count, 'pId': 0, 'name': i, 'pinyin': p.get_pinyin(i, splitter=''),
                       'fullname': p.get_pinyin(i, splitter='')})
        count += 1
        for j in os.listdir(path + i):
            if os.path.isfile(path + i + '/' + j) and (j.split('.')[1] == 'xls' or j.split('.')[1] == 'xlsx'):
                continue
            table[j] = [count, table[i][0], j, p.get_pinyin(j, splitter=''),
                        table[i][3] + '.' + p.get_pinyin(j, splitter='')]
            table2.append({'id': count, 'pId': table[i][0], 'name': j.split('.')[0], 'pinyin': p.get_pinyin(j.split('.')[0], splitter=''),
                           'fullname': table[i][3] + '.' + p.get_pinyin(j.split('.')[0], splitter='')})
            count += 1
            names = []
            if os.path.isdir(path + i + '/' + j):
                for k in os.listdir(path + i + '/' + j):
                    if k.split('.')[1] == 'xls' or k.split('.')[1] == 'xlsx':
                        continue
                    x = k.split('.')[0]
                    if x not in names:
                        names.append(x)
                        table[x] = [count, table[j][0], x, p.get_pinyin(x, splitter=''),
                                    table[i][3] + '.' + table[j][3] + '_' + p.get_pinyin(x, splitter='')]
                        table2.append(
                            {'id': count, 'pId': table[j][0], 'name': x, 'pinyin': p.get_pinyin(x, splitter=''),
                             'fullname': table[i][3] + '.' + table[j][3] + '_' + p.get_pinyin(x, splitter='')})
                        count += 1
    contents = list(table.values())

    with open('table.json', 'w') as file:
        # file.write(str(table))
        # file.write(str(table2))
        for i in table2:
            json.dump(i, file, ensure_ascii=False)
            file.write('\n')


if __name__ == '__main__':
    # dependent_tree()
    to_pinyin()
