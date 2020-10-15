from xpinyin import Pinyin
import os
import json
import copy
p = Pinyin()


def rename(name, names, freq):
    if name not in names:
        return name
    else:
        freq += 1
        name = name.split("_")[0] + "_" + str(freq)
        return rename(name, names, freq)


def to_pinyin():
    x = os.walk("data/2-level")
    paths = [i for i in x]
    paths.reverse()
    # table = {}
    for i in paths:
        names = []
        for j in i[1] + i[2]:
            new_name = p.get_pinyin(j, splitter='')
            new_name = rename(new_name, names, freq=0)
            names.append(new_name)
            # table[os.path.join(i[0], j)] = new_name
            os.rename(os.path.join(i[0], j), os.path.join(i[0], new_name))


count = 0
table = {}
fullname_table = {}


def pick_name(name):
    if name in fullname_table.values():
        name[-1] = name[-1].split('_')
        if len(name[-1]) > 1:
            name[-1] = name[-1][0] + '_' + str(int(name[-1][1]) + 1)
            pick_name(name)
        else:
            name[-1] = name[-1][0] + '_1'
    return name


def check(name):
    last = p.get_pinyin(name[-1], splitter='')
    if len(name) == 1:
        temp = [last]
    else:
        temp = copy.copy(fullname_table[name[:-1]])
        temp.append(last)
    fullname_table[tuple(name)] = pick_name(temp)
    return name


def write_to_table(path, depth, parent_id):
    global count
    if os.path.isfile(path):
        if path.split('.')[-1] != 'shp':
            return count
        else:
            path = path.split('.')[-2]
    count += 1
    path = path.replace(root, '')
    elements = tuple(path.split(os.sep))
    elements = check(elements)
    filename = elements[-1]
    if depth == 1:
        fullname = fullname_table[elements][0] + '.' + fullname_table[elements][0]
    elif depth == 2:
        fullname = fullname_table[elements][0] + '.' + fullname_table[elements][1]
    else:
        fullname = fullname_table[elements][0] + '.' + fullname_table[elements][1] + '_' + fullname_table[elements][2]
    table[path] = {'id': count, 'pId': parent_id, 'depth': depth, 'name': filename,
                   'pinyin': fullname_table[elements][-1], 'fullname': fullname}
    return count


def dependent_tree(root, path, depth, parent_id):
    for i in os.listdir(path):
        temp = os.path.join(path, i)
        item_id = write_to_table(temp, depth, parent_id)
        if os.path.isdir(temp):
            dependent_tree(root, temp, depth + 1, item_id)


if __name__ == '__main__':
    for todo in [ '3']:
        root = "data/chinese/" + todo + "-level/"
        dependent_tree(root, root, 1, 0)
    with open('table.json', 'w') as file:
        for i in table.values():
            json.dump(i, file, ensure_ascii=False)
            file.write(',\n')
    # to_pinyin()
