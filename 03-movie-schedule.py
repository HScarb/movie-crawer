# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
import sys
import MovieUtils

# 默认等待时间
DEFAULT_TIMEOUT = 10


# conn = mysql.connector.connect(user='movie', password='movie', database='movie', host='106.14.26.144')
# cursor = conn.cursor()

def crawSchedule(movieID):
    url = 'http://pp.58921.com/film/' + str(movieID)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/48.0.2564.116 Safari/537.36 '
    }
    text = ''
    cityList = []
    for i in range(0, 15):
        movieSceneDict = {'movieid': None,
                          'moviename': None,
                          'cityid': None,
                          'date': None,
                          'scene': None
                          }
        cityList.append(movieSceneDict)

    # 抓取整个网页
    try:
        print('Requesting url: ', url)
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None

    text = text.encode('latin1').decode('utf-8')
    soup = BeautifulSoup(text, "lxml")

    # 将表头存到list中，这里先不考虑不是城市的情况，最后统一处理删去无用数据
    i = 0
    theadResults = soup.find_all('thead')
    for theadResult in theadResults:
        th_list = theadResult.find_all('th')
        for th in th_list:
            cityList[i]['city'] = th.get_text()
            i += 1
    results = soup.find_all('tr')
    for result in results:
        td_list = result.find_all('td')
        for td in td_list:
            if td.img is not None:
                # print(td.img['src'])
                MovieUtils.downloadImg(td.img['src'], 'img.png')
                print(MovieUtils.parseImg('img.png'))
            else:
                print(td.get_text())


def main():
    # todo
    crawSchedule(6189)
    return


if __name__ == '__main__':
    main()
