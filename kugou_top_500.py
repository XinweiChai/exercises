import requests
from bs4 import BeautifulSoup


def get_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text)
    ranks = soup.select('span.pc_temp_num')
    titles = soup.select('div.pc_temp_songlist > ul > li > a')
    times = soup.select('span.pc_temp_tips_r > span')
    for rank, title, time in zip(ranks, titles, times):
        str1 = title.get_text().split("-")
        data = {
            'rank': rank.get_text().strip(),
            'singer': str1[0].strip(),
            'song': str1[1].strip(),
            'time': time.get_text().strip()
        }
        print(data)


if __name__ == '__main__':
    urls = ['https://kugou.com/yy/rank/home/{}-8888.html'
                .format(i) for i in range(1, 30)]
    for url in urls:
        get_info(url)
