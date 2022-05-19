import requests as rq

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}

books = ['军人的眼光']

sites = {'京东': 'https://search.jd.com/Search?keyword=',
         '当当': 'http://search.dangdang.com/?key=',
         '淘宝': '',
         '孔夫子': 'https://search.kongfz.com/product_result/?key=',
         '有路网': 'https://www.youlu.net/search/result3/bookName=',
         '多抓鱼': 'https://www.duozhuayu.com/search/book/',
         # '拼多多': '',
         # '转转': '',
         '旧书街': 'http://www.jiushujie.com/sell?q=',
         '7788收藏': 'https://www.997788.com/all_0/0/?searchtype=1&www=all&t2=0&s0=',
         # '漫游鲸': '',
         # '闲鱼': '',
         '中国图书网': 'http://www.bookschina.com/book_find2/?stp=',
         '二手教材网': 'http://so.2sjc.com/search.aspx?q=',
         # '丁书网': 'http://www.iisbn.com/search.html',
         '布衣书局': 'http://www.booyee.com.cn/searchresult.jsp?bookname=',
         # '渔书': '',
         '典书旧书网': 'https://dianshu.diytrade.com/sdp/2962676/2/pl-7809337/0.html?qs=',
         '苏宁易购': 'https://search.suning.com//',
         '亚马逊': 'https://www.amazon.cn/s?k=',
         }

for i in sites:
    for book in books:
        res = rq.get(sites[i] + book)
        content = res.text


def post_exception():
    res = rq.post('http://www.iisbn.com/search.html', params={'keyword': 'adobe'})
    content = res.text
    a = 1
