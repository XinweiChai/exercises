import requests as rq

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}

sites = {'京东': 'https://search.jd.com/Search?keyword={name}&enc=utf-8&wq=aa&pvid=e48d8491231c475c9bd14ea011f944bd',
         '当当': 'http://search.dangdang.com/?key={name}&act=input',
         '淘宝': '',
         '孔夫子': 'https://search.kongfz.com/product_result/?key={name}&status=0&_stpmt=eyJzZWFyY2hfdHlwZSI6ImFjdGl2ZSJ9',
         '有路网': 'https://www.youlu.net/search/result3/?isbn=&publisherName=&author=&bookName={name}',
         '多抓鱼': 'https://www.duozhuayu.com/search/book/{name}',
         # '拼多多': '',
         # '转转': '',
         '旧书街': 'http://www.jiushujie.com/sell?q={name}',
         '7788收藏': 'https://www.997788.com/all_0/0/?searchtype=1&www=all&t2=0&s0={name}',
         # '漫游鲸': '',
         # '闲鱼': '',
         '中国图书网': 'http://www.bookschina.com/book_find2/?stp={name}&sCate=0',
         '二手教材网': 'http://so.2sjc.com/search.aspx?q={name}&x=0&y=0',
         '丁书网': 'http://www.iisbn.com/search.html',
         '布衣书局': 'http://www.booyee.com.cn/searchresult.jsp?bookname={name}',
         # '渔书': '',
         '典书旧书网': 'https://dianshu.diytrade.com/sdp/2962676/2/pl-7809337/0.html?qs={name}',
         '苏宁易购': 'https://search.suning.com/{name}/',
         '亚马逊': 'https://www.amazon.cn/s?k={name}&crid=2FR97FLUB4KEK&sprefix=%2Caps%2C45&ref=nb_sb_ss_recent_1_0_recent',
         }

for i in sites:
    res = rq.get(sites[i])
    content = res.text

