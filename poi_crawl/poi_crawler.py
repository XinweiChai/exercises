import requests
import json
import xmltodict
from dicttoxml import *
import pandas as pd
import re
import os
from time import sleep

decimal = 6


class Area:
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def divide_rect(self):
        mid_x = round((self.x1 + self.x2) / 2, decimal)
        mid_y = round((self.y1 + self.y2) / 2, decimal)
        return [Area(self.x1, self.y1, mid_x, mid_y), Area(mid_x, self.y1, self.x2, mid_y),
                Area(self.x1, mid_y, mid_x, self.y2), Area(mid_x, mid_y, self.x2, self.y2)]

    def to_string(self):
        return str(self.x1) + "," + str(self.y1) + "|" + str(self.x2) + "," + str(self.y2)


def read_poi_code(fn):
    poi_code = []
    with open(fn, 'r') as file:
        file.__next__()
        for i in file:
            poi_code.append(re.split(",", i)[1])
    return poi_code


def has_subdiv(code, codes):
    if len(codes) == codes.index(code) + 1:
        return False
    if int(code) % 10000 == 0:
        if int(codes[codes.index(code) + 1]) % 10000 != 0:
            return True
    elif int(code) % 100 == 0:
        if int(codes[codes.index(code) + 1]) % 100 != 0:
            return True
    return False


def crawl(ad_codes, poi_codes, url, key):
    for ad_code in ad_codes:
        poi_folder = "pois/" + ad_code
        if not os.path.exists(poi_folder):
            os.mkdir(poi_folder)
        for poi_code in poi_codes:
            if has_subdiv(poi_code, poi_codes):
                continue
            para = {'keywords': '', 'types': poi_code, 'city': ad_code, 'citylimit': 'true', 'offset': '20',
                    'key': key, 'extensions': 'all'}
            crawl_one(ad_code, poi_code, url, para, False)
    # with open("data", 'r', encoding='utf-8') as file:
    #     x = json.loads(file)
    # pd.DataFrame(x["pois"]).to_csv('x.csv')


def crawl_one(ad_code, poi_code, url, para, numbering):
    page = 1
    while True:
        file_name = "pois/" + ad_code + '/' + poi_code
        # if not numbering:
        #     if os.path.exists(file_name):
        #         break
        sleep(0.021)  # Concurrency limit
        para['page'] = page
        r = requests.get(url, para).json()
        # if not numbering:
        #     if int(r['count']) >= 900:
        #         with open("crowd.csv", "w+") as file:
        #             file.write(ad_code + "," + poi_code)
        #         print([ad_code, poi_code])
        #         break
        if numbering:
            for i in r['pois'][:]:
                # if ad_code not in i['adcode']:
                if not re.match('11', i['adcode']):
                    r['pois'].remove(i)
        if not r['pois']:
            break
        if len(r['pois']) == 20 and page >= 45:
            print(ad_code + "," + poi_code + "pages: " + str(page))
        with open(file_name, 'a+', encoding='utf-8') as outfile:
            for i in r['pois']:
                json.dump(i, outfile, ensure_ascii=False)
                outfile.write("\n")
        page = page + 1


def district_area(ad_codes, url_dist, key):
    area = {}
    for adcode in ad_codes:
        para = {'keywords': adcode, 'subdistrict': '0', 'extensions': 'all', 'key': key}
        r = requests.get(url_dist, para).json()
        temp = r['districts'][0]['polyline']
        temp = re.split(";|\|", temp.strip())
        temp = [[float(j) for j in i.split(",")] for i in temp]
        area[adcode] = Area(min(temp, key=lambda x: x[0])[0], max(temp, key=lambda x: x[1])[1],
                            max(temp, key=lambda x: x[0])[0], min(temp, key=lambda x: x[1])[1])
    return area


def district_area_all(ad_codes, url_dist, key):
    coordinates = []
    for adcode in ad_codes:
        para = {'keywords': adcode, 'subdistrict': '0', 'extensions': 'all', 'key': key}
        r = requests.get(url_dist, para).json()
        temp = r['districts'][0]['polyline']
        temp = re.split("[;|]", temp.strip())
        temp = [[float(j) for j in i.split(",")] for i in temp]
        coordinates += temp
    return Area(min(coordinates, key=lambda x: x[0])[0], max(coordinates, key=lambda x: x[1])[1],
                max(coordinates, key=lambda x: x[0])[0], min(coordinates, key=lambda x: x[1])[1])


def rec_crawl(area, ad_code, poi_code, url, key):
    para = {'polygon': area.to_string(), 'types': poi_code,
            'offset': '20', 'key': key, 'extensions': 'all'}
    sleep(0.021)
    r = requests.get(url, para).json()
    if int(r['count']) >= 900:
        for i in area.divide_rect():
            rec_crawl(i, ad_code, poi_code, url, key)
    else:
        if not os.path.exists("pois/" + ad_code):
            os.mkdir("pois/" + ad_code)

        crawl_one(ad_code, poi_code, url, para, True)


# def foo(x, count):
#     if x % 2 == 0 and x > 2:
#         for i in [x // 2, x // 2 + 1]:
#             count = foo(i, count)
#     else:
#         print(count)
#         count += 1
#         return count

def combine_contents(folder, poi_type):
    count_all = 0
    for maindir, subdir, file_name_list in os.walk(folder):
        for filename in file_name_list:
            if filename == poi_type:
                path = os.path.join(maindir, filename)
                count = 0
                for index, line in enumerate(open(path, 'r', encoding='utf-8')):
                    count += 1
                count_all += count
    print(count_all)


if __name__ == "__main__":
    combine_contents("pois", "050117")
    ad_codes_test = [110115]
    # ad_codes_test = [110101, 110102, 110105, 110106, 110107, 110108, 110111, 110112, 110114, 110115]
    # ad_codes_test = [110100]
    ad_codes_test = [str(i) for i in ad_codes_test]
    poi_codes_test = read_poi_code('amap_poicode.csv')
    key_test = '29c66d77721e218e411655d5d7988d86'
    url_poi = "https://restapi.amap.com/v3/place/text?"
    url_district = "https://restapi.amap.com/v3/config/district?"
    url_polygon = "https://restapi.amap.com/v3/place/polygon?"
    crawl(ad_codes_test, poi_codes_test, url_poi, key_test)
    # para = {'keywords': '', 'types': '050117', 'city': '110105', 'citylimit': 'true', 'offset': '20',
    #         'key': key_test, 'extensions': 'all'}
    # crawl_one('110105', '050117', url_poi, para, True)
    # with open("crowd.csv", "r") as file:
    #     big_crowd = [[val for val in line.strip().split(",")] for line in file]
    # area = district_area(ad_codes_test, url_district, key_test)
    # area = district_area_all(ad_codes_test, url_district, key_test)
    # for poi in big_crowd:
    #     rec_crawl(area[poi[0]], poi[0], poi[1], url_polygon, key_test)
    # for poi in poi_codes_test:
    #     if has_subdiv(poi, poi_codes_test):
    #         continue
    #     rec_crawl(area[ad_codes_test[0]], ad_codes_test[0], poi, url_polygon, key_test)
    # rec_crawl(area[ad_codes_test[0]], ad_codes_test[0], '010104', url_polygon, key_test)
