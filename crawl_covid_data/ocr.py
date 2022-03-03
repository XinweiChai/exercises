# # 导入easyocr
# import easyocr
#
# # 创建reader对象
# reader = easyocr.Reader(['ch_sim', 'en'])
# # reader = easyocr.Reader(['ch_sim'])
# # 读取图像
# # result = reader.readtext('test.jpg')
# result = reader.readtext('test2.png')
# # 结果
# for i in result:
#     print(i[1])


# !/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import time
import base64
import requests
from datetime import datetime
print(datetime.now())

start = time.time()
# 获取access_token
# client_id 为官网获取的AK， client_secret 为官网获取的SK
appid = "25667100"
client_id = "SgBFqf3AbUGo6AGqZ4BBGccw"
client_secret = "Tu6WAMR0qmUMx9LpRpv0CXWFG2UoU9Oe"
print("appid:" + appid)
print("client_id:" + client_id)
print("client_secret:" + client_secret)

token_url = "https://aip.baidubce.com/oauth/2.0/token"
host = f"{token_url}?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

response = requests.get(host)
access_token = response.json().get("access_token")


# 调用通用文字识别高精度版接口
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
# 以二进制方式打开图文件
# 参数image：图像base64编码
# 下面图片路径请自行切换为自己环境的绝对路径
with open("test2.png", "rb") as f:
	image = base64.b64encode(f.read())

body = {
	"image": image,
	"language_type": "auto_detect",
    "detect_direction": "true",
    "paragraph": "true",
    "probability": "true",
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
request_url = f"{request_url}?access_token={access_token}"
response = requests.post(request_url, headers=headers, data=body)
content = response.content.decode("UTF-8")
# 打印调用结果
print(content)


end = time.time()
print(f"Running time: {(end-start):.2f} Seconds")