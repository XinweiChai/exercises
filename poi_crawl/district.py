import requests

# post_str = {"searchWord": "朝阳区", "searchType": "1", "needSubInfo": "true", "needAll": "true", "needPolygon": "true",
#             "needPre": "true"}
# x = requests.get('http://api.tianditu.gov.cn/administrative?',
#                  params={'postStr': str(post_str), 'tk': '9277e61c34682657cf599844a7a668fa'})

# x = requests.get('https://restapi.amap.com/v3/config/district?',
#                  params={"key": "29c66d77721e218e411655d5d7988d86", "keywords": "北京", "subdistrict": "1", "extensions": "all"})
x = requests.get("https://restapi.amap.com/v3/place/text?keywords=北京大学&city=beijing&output=json&offset=20&page=1&key=29c66d77721e218e411655d5d7988d86&extensions=base")
y = x.json()
