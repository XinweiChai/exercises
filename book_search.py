import os
import webbrowser

import requests as rq
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
books = []
if not os.path.exists('temp'):
    os.mkdir('temp')
with open('C:\\Users\\Lenovo\\Desktop\\book_list.txt', encoding='utf-8') as f:
    books = f.read().splitlines()

sites = {'京东': 'https://search.jd.com/Search?keyword=',
         '当当': 'http://search.dangdang.com/?key=',
         '淘宝': 'https://s.taobao.com/search?q=',
         '孔夫子': 'https://search.kongfz.com/product_result/?key=',
         '有路网': 'https://www.youlu.net/search/result3/?bookName=',
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
         '苏宁易购': 'https://search.suning.com/',
         '亚马逊': 'https://www.amazon.cn/s?k=',
         }


def browsers(book):
    for i in sites:
        if i == '中国图书网':
            url = sites[i] + book.encode('unicode_escape').decode().replace('\\', '%')
        else:
            url = sites[i] + book
        if i == '苏宁易购':
            url += '/'
        webbrowser.open(url, new=2)


def post_exception(book):
    res = rq.post('http://www.iisbn.com/search.html', params={'keyword': book})
    soup = BeautifulSoup(res.content, 'html.parser')
    lst = soup.find_all('section', class_='bookscats')[0]
    items = [str(i) + '\n' for i in lst.find_all('h3')]
    if items:
        fn = os.path.join('temp', f'{book}.txt')
        with open(fn, 'w', encoding='utf-8') as f:
            f.writelines(items)
        os.system(f'notepad {fn}')


def clear():
    # for windows
    if os.name == 'nt':
        os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')


if __name__ == '__main__':
    for idx, book in enumerate(books):
        input(f'To next book {book}, please press Enter')
        # clear()
        browsers(book)
        post_exception(book)
    if os.name == 'nt':
        os.system('pause')