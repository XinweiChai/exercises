from xpinyin import Pinyin
import os
import json

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


def check(name):
    if name in table.keys():
        name = name.split('_')
        if len(name) > 1:
            return name[0] + '_' + str(int(name[1]) + 1)
        else:
            return name[0] + '_1'
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
    elements = path.split(os.sep)
    filename = elements[-1]
    if '陕西' in path:
        x = 1
    if depth == 1:
        fullname = filename + '.' + filename
    elif depth == 2:
        fullname = table[path.split(os.sep)[0]]['pinyin'] + '.' + filename
    else:
        fullname = table[path.split(os.sep)[0]]['pinyin'] + '.' + \
                   table[os.path.split(path)[0]]['pinyin'] + '_' + elements[2]
    fullname = p.get_pinyin(fullname, splitter='')
    pinyin = p.get_pinyin(filename, splitter='')
    if fullname in table.values():
        fullname = check(fullname)
        pinyin = pinyin + '_' +fullname.split('_')[-1]
    # if fullname in table.keys() and depth == table[fullname]['depth']:
    table[path] = {'id': count, 'pId': parent_id, 'depth': depth, 'name': filename,
                   'pinyin': pinyin, 'fullname': fullname}
    return count


def dependent_tree(root, path, depth, parent_id):
    for i in os.listdir(path):
        temp = os.path.join(path, i)
        item_id = write_to_table(temp, depth, parent_id)
        if os.path.isdir(temp):
            dependent_tree(root, temp, depth + 1, item_id)


if __name__ == '__main__':
    for todo in ['2', '3']:
        root = "data/chinese/" + todo + "-level/"
        dependent_tree(root, root, 1, 0)
    with open('table.json', 'w') as file:
        for i in table:
            json.dump(i, file, ensure_ascii=False)
            file.write(',\n')
    # to_pinyin()
