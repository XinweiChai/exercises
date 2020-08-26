import re
import sys
import csv
import xgboost


def find_line(fn, words):
    res = []
    count = 0
    for word in words:
        # flag = True
        with open(fn, 'r', encoding='utf-8') as file:
            for line in file:
                format_1 = line.strip().replace("[", "").replace("]", "")
                format_2 = re.split(",", format_1)
                temp_0 = re.split("\s", format_2[0].replace("(", "").replace(")", ""))
                temp_1 = re.split("\s", format_2[1].replace("(", "").replace(")", ""))
                if float(word[0]) - float(temp_0[1]) < 0.00001 and float(word[1]) - float(temp_0[2]) < 0.00001:
                    count = count + 1
                    print(count)
                    res.append(temp_1[1:] + [format_2[2]] + [word[2]])
                    # file2.write(line+" "+str(word[1])+"\n")
                    # flag = False
                    break
        # if flag:
        #     print(word)
    with open(fn + "res", 'w+', newline='', encoding='utf-8') as file2:
        writer = csv.writer(file2)
        writer.writerows(res)
        # res.sort(key=lambda x: x[1],reverse=True)
        # for i in res:
        #
        #     file2.write(i[0] + " " + str(i[1]) + "\n")
    return res


def extract(fn):
    res = []
    with open(fn, 'r') as file:
        for line in file:
            # temp = re.split("\)\),", line.strip())
            # res.append([temp[0] + "))", temp[1]])
            temp = re.split("\s\(?|\),", line.strip())
            res.append(temp[1:])  # dist1,dist2,count
    return res


def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield len(stack), string[start + 1: i]


if __name__ == "__main__":
    x = parenthetic_contents('(a(b(c)(d)e)(f)g)')
    fn2 = sys.argv[2]
    fn1 = sys.argv[1]
    find_line(fn1, extract(fn2))
