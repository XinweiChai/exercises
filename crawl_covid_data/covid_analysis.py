import time

import requests
import re
import os

import xmltojson
from bs4 import BeautifulSoup
import json
import jieba

url_pic = []
search_url = "http://search.gd.gov.cn/api/search/all/"
path = '/home/chai/Documents/data/covid_warning_areas'
os.chdir(path)

# Direct_administered_municipalities
dam = ('北京市', '天津市', '上海市', '重庆市')
exceptions = {'广东省东莞市': '441900', '广东省中山市': '442000'}


def page_with_pics(keyword):
    y = []
    for i in url_pic:
        response = requests.get(i)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.text
        # assert keyword in title
        if keyword in title:
            # year = re.search(r"\d{4}(?=年)", title).group()
            month = re.search(r"\d{1,2}(?=月)", title).group().zfill(2)
            day = re.search(r"\d{1,2}(?=日)", title).group().zfill(2)
            # hour = re.search(r"\d{1,2}(?=时)", title).group().zfill(2)
            # x = year + month + day
            x = month + day
            paras = soup.select('p[style="text-align: justify;"]')
            if paras:
                paras = [i.find_all(text=True) for i in paras[:-2]]
                paras = [x for x in paras if x != []]
                paras = [''.join([j.strip() for j in i]) for i in paras]
                fname = 'new/' + x + ".txt"
                with open(fname, 'a') as f:
                    for t in paras:
                        if len(t) > 0:
                            f.writelines(t + "\n")
            else:
                fname = 'pic/' + x + ".txt"
                with open(fname, 'a') as f:
                    f.writelines(i + '\n')
    print(y)


def reorganize():
    directory = 'dat/'
    for i in os.listdir(directory):
        with open(directory + i, 'r', encoding='UTF-8-sig') as f:
            contents = f.read().split()
            flag = 0
            high = []
            mid = []
            for j in contents:
                if j == '高风险地区：':
                    flag = 1
                    continue
                elif j == '中风险地区：':
                    flag = 2
                else:
                    if '暂无' == j:
                        continue
                    if flag == 1:
                        high.append(j + '\n')
                    elif flag == 2:
                        mid.append(j + '\n')
            with open('high/' + i, 'w') as f1:
                f1.writelines(high)
            with open('mid/' + i, 'w') as f2:
                f2.writelines(mid)


class Crawl_page:
    def __init__(self):
        self.title = None

    def getHTML(self, url):
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.content

    def getContent(self, url):
        html = self.getHTML(url)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            title = soup.title.text
            assert "全国疫情" in title
            year = re.search(r"\d{4}(?=年)", title).group()
            month = re.search(r"\d{1,2}(?=月)", title).group().zfill(2)
            day = re.search(r"\d{1,2}(?=日)", title).group().zfill(2)
            # hour = re.search(r"\d{1,2}(?=时)", title).group().zfill(2)
            self.title = year + month + day
        except (IndexError, AttributeError, AssertionError):
            return

        paras = soup.select('.article p')
        paras = [x.get_text().strip() for x in paras]
        paras = [x for x in paras if x]

        if not paras:
            url_pic.append(url)
            return None
        if '来源' in paras[-1] or '国务院' in paras[-1]:
            paras.pop()
            if '来源' in paras[-1] or '国务院' in paras[-1]:
                paras.pop()
        elif '来源' in paras[-2] or '国务院' in paras[-2]:
            paras.pop(-2)
        return paras

    def saveFile(self, text):
        if self.title and text:
            fname = 'dat/' + self.title + ".txt"
            with open(fname, 'w') as f:
                for t in text:
                    if len(t) > 0:
                        f.writelines(t + "\n")

    def overall(self, url):
        self.saveFile(self.getContent(url))


def crawl(keyword):
    x = []
    params = {"gdbsDivision": "440000", "gdbsOrgNum": "0", "keywords": keyword, "page": 1, "position": "title",
              "range": "site", "recommand": 1, "service_area": 1, "site_id": "162", "sort": "smart"}
    for i in range(1, 15):
        params['page'] = i
        response = requests.post(search_url, json=params)
        res = response.json()
        for j in res['data']['news']['list']:
            x.append(j['url'])
    with open('urls.txt', 'w') as f:
        for i in x:
            f.writelines(i + '\n')
    with open('urls.txt', 'r') as f:
        x = f.read().split('\n')
        for i in x:
            print(i)
            Crawl_page().overall(i)
    print(url_pic)


suffix_lvl1 = ['省', '自治区', '市']


def renew_name(s):
    for pos in range(len(s)):
        if s[:pos] in suffix_lvl1:
            return s[pos:], s[:pos]
    return s, ''


def req(region, query):
    key = 'UKG1G71ttFxlVRwOqCrllVXLfRs4MegB'
    url = 'https://api.map.baidu.com/place/v2/suggestion?'
    params = {'query': query, 'region': region, 'output': 'json', 'ak': key}
    return requests.get(url=url, params=params).json()['result']


def helper(k, dct, spl):
    if k[:6] in exceptions:
        return exceptions[k[:6]]
    for i in range(spl):
        for pos in range(1, len(k) + 1):
            try:
                if k[:pos] in dct:
                    dct = dct[k[:pos]]
                    k = k[pos:]
                    break
            except KeyError:
                raise
    return dct


def match_baidu(fn):
    with open(fn, 'r') as f:
        dct = json.loads(f.read())
    dirs = ['mid', 'high']
    cnt = 0
    cnt_baidu = 0
    for i in dirs:
        for j in os.listdir(os.path.join(path, i)):
            with open(os.path.join(path, i, j), 'r', encoding='UTF-8-sig') as f:
                contents = f.read().split()
            with open(os.path.join(path, i + '_code', j), 'w', encoding='utf-8') as f_out:
                for k in contents:
                    splits = 2 if k[:3] in dam else 3
                    try:
                        result = helper(k, dct, splits)
                        f_out.write(result + '\n')
                    except (KeyError, TypeError):
                        temp = list(jieba.cut(k))
                        province, city = temp[0:2]
                        region, query = ''.join(temp[:splits - 1]), ''.join(temp[splits - 1:6])
                        time.sleep(0.1)
                        res = req(region, query)
                        try:
                            for cand in res:
                                if cand['province'] == province and cand['city'] == city:
                                    adcode = cand['adcode']
                                    f_out.write(adcode + '\n')
                                    cnt_baidu += 1
                                    break
                            else:
                                raise KeyError
                        except (IndexError, KeyError):
                            print(i + '/' + j)
                            print(k)
                        cnt += 1
    print(cnt)
    print(cnt_baidu)


def helper_dic(ul, skip):
    if skip:
        uls = ul.find_all('ul')
        temp = {}
        for i in uls:
            temp.update(dictify(i))
        return temp
    else:
        return dictify(ul)


def dictify(ul):
    result = {}
    for li in ul.find_all("li", recursive=False):
        key = next(li.stripped_strings)
        ul = li.find("ul")
        if ul:
            result[key.split()[0]] = dictify(ul)
        else:
            key = key.split()
            result[key[0]] = key[1]
    return result


def precise_list():
    # url = "http://www.ip33.com/area_code.html"
    url = 'http://www.ip33.com/area/2019.html'
    req = requests.get(url)
    req.encoding = 'utf-8'
    xml = req.text.replace('&', '')
    soup = BeautifulSoup(xml, "html.parser")
    # test = soup.find_all('div', {"class": "ip"})
    test = soup.find_all('div', class_="ip")
    test.pop(0)
    res = {}
    for x in test:
        province = x.find('h4').text.split()[0]
        res[province] = helper_dic(x.find('ul'), province in dam)
    # Exceptions
    res["广东省"]["东莞市"] = "441900"
    res["广东省"]["中山市"] = "442000"
    with open('areas3.json', 'w') as f:
        json.dump(res, f, ensure_ascii=False)


if __name__ == '__main__':
    # keywords = ["全国疫情中高风险地区", "最新疫情风险等级提醒"]
    # for i in keywords:
    #     crawl(i)
    # page_with_pics("最新疫情风险等级提醒")
    # reorganize()
    # match_baidu('areas2.json')
    precise_list()
