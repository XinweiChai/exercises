import requests
import re
import os
from bs4 import BeautifulSoup
import json

url_pic = []


def page_with_pics():
    y = []
    for i in url_pic:
        response = requests.get(i)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.text
        assert "全国疫情" in title
        year = re.search(r"\d{4}(?=年)", title).group()
        month = re.search(r"\d{1,2}(?=月)", title).group().zfill(2)
        day = re.search(r"\d{1,2}(?=日)", title).group().zfill(2)
        hour = re.search(r"\d{1,2}(?=时)", title).group().zfill(2)
        x = year + month + day
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
        date = i.split('.')[0]
        if i == '20210816.txt':
            c = 1
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


def create_embedded_location_list():
    req = requests.get('http://www.ip33.com/area_code.html')
    soup = BeautifulSoup(req.content, 'html.parser')
    content = soup.select('.ip')
    cities = [i.get_text().strip() for i in content]
    res = {}
    for i in cities:
        temp = re.split(r'\n+', i)
        loc = {}
        for j in temp[1:]:
            location, code = j.split()
            loc[location] = code
        prov, prov_code = temp[0].split()
        res[prov] = loc
        with open('cities.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(res, ensure_ascii=False))


def helper(k, dct):
    for pos in range(1, len(k) + 1):
        if k[:pos] in dct:
            province = k[:pos]
            if k[pos] in ['市', '省']:
                pos += 1
            for pos2 in range(pos + 2, len(k) + 1):
                for ele in dct[province]:
                    if k[pos:pos2] in ele:
                        return True
    return False


def match():
    with open('cities.json', 'r') as f:
        dct = json.loads(f.read())
    dirs = ['mid/', 'high/']
    # dirs = ['dat/']
    for i in dirs:
        for j in os.listdir(i):
            with open(i + j, 'r', encoding='UTF-8-sig') as f:
                contents = f.read().split()
                temp = []
                for k in contents:
                    # if k not in ['高风险地区：', '暂无', '中风险地区：'] and not helper(k, dct):
                    if not helper(k, dct):
                        temp.append(k)
                if temp:
                    print(j)
                    print('\n'.join(temp))


if __name__ == '__main__':
    # x = []
    # search_url = "http://search.gd.gov.cn/api/search/all/"
    # json = {"gdbsDivision": "440000", "gdbsOrgNum": "0", "keywords": "全国疫情中高风险地区", "page": 1, "position": "title",
    #         "range": "site", "recommand": 1, "service_area": 1, "site_id": "162", "sort": "smart"}
    # for i in range(1, 15):
    #     json['page'] = i
    #     response = requests.post(search_url, json=json)
    #     res = response.json()
    #     for j in res['data']['news']['list']:
    #         x.append(j['url'])
    # with open('urls.txt', 'w') as f:
    #     for i in x:
    #         f.writelines(i + '\n')
    # with open('urls.txt', 'r') as f:
    #     x = f.read().split('\n')
    #     for i in x:
    #         print(i)
    #         Crawl_page().overall(i)
    # print(url_pic)
    # reorganize()
    create_embedded_location_list()
    match()
