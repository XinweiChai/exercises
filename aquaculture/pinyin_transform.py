from xpinyin import Pinyin
import os
import json
import copy
import shapefile
import shutil

p = Pinyin()


def rename(name, names, freq):
    if name not in names:
        return name
    else:
        freq += 1
        name = name.split("_")[0] + "_" + str(freq)
        return rename(name, names, freq)


def to_pinyin():
    x = os.walk("data/3-level")
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
    root = "data/2-level"
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


def check_validity():
    for i in os.walk('data/chinese/'):
        for j in i[2]:
            if j.split('.')[-1] == 'shp':
                x = shapefile.Reader(os.path.join(i[0], j))
                y = x.fields
                x.close()
                z = [i[0].upper() for i in y[1:]]
                if '平潭县' in j:
                    temp = 1
                # if 'AERA' in z:
                #     shapefile.Writer()
                #     print(os.path.join(i[0], j))
                # if not ('ID' in z and 'CAT' in z and 'AREA' in z):
                if not ('X' in z and 'Y' in z):
                # pos = z.index('CAT') + 1
                # pos_id = z.index('ID') + 1
                # if 'N' not in y[pos]:
                    # continue
                # if 'N' not in y[pos_id]:
                    # aa=1
                    print(os.path.join(i[0], j))
                    # name = j.split(".")[0] + '.*'
                    # source = os.path.join(i[0], name).replace('\\', '/')
                    # temp = f'mv {source} temp'
                    # os.system(temp)


if __name__ == '__main__':
    # for todo in ['2', '3']:
    #     root = "data/chinese/" + todo + "-level/"
    #     dependent_tree(root, root, 1, 0)
    # with open('table.json', 'w') as file:
    #     for i in table.values():
    #         json.dump(i, file, ensure_ascii=False)
    #         file.write(',\n')
    # to_pinyin()
    check_validity()
