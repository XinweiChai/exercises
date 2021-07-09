import json
import requests
import os

##########本程序可下载端口上所有已编辑的json文件#####
base_api = "http://localhost:3000/api/"
list_url = base_api + "listing"  # 列表URL地址
mask_api = base_api + "json"  # 标注JSON的api
path = "sse_json/"  # 下载地址
##################################################

r = requests.get(list_url)
jsonset = json.loads(r.text)  # json文件的列表(list)

for jsobj in jsonset:  # 得到逐条dic
    mask_url = mask_api + jsobj['url']

    mask = requests.get(mask_url).text  # 得到一张图片的JSON标注
    fn, _ = os.path.splitext(jsobj['file'])
    with open(path + fn + '.json', "w") as f:  # 写入JSON文件
        f.write(mask)
    print("Saving " + fn + '.json!')

print('finish!')
