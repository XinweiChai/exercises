import requests

# url = "https://api.map.baidu.com/place/v2/search?"
key = 'UKG1G71ttFxlVRwOqCrllVXLfRs4MegB'
# param = {'query': 'ATM机', 'tag': '银行', 'region': '北京', 'output': 'json', 'ak': key}
# param = {'query': 'ATM机', 'region': '河北省石家庄市藁城区', 'output': 'json', 'ak': key}
# param = {'region': '河北省石家庄市藁城区', 'output': 'json', 'ak': key}


url = 'https://api.map.baidu.com/place/v2/suggestion?'
# param = {'query': '藁城', 'region': '河北省石家庄市',  'output': 'json', 'ak': key}
param = {'query': '', 'region': '广东省广州市',  'output': 'json', 'ak': key}
req = requests.get(url, params=param)
req.encoding = 'utf-8'
# req = requests.get(url)
print(req.text)
