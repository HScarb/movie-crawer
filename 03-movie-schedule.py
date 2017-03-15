# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import mysql.connector

#默认等待时间
DEFAULT_TIMEOUT = 10
# conn = mysql.connector.connect(user='movie', password='movie', database='movie', host='106.14.26.144')
# cursor = conn.cursor()

def crawSchedule():
    url = 'http://pp.58921.com/film/6189'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    text = ''
    # 抓取整个网页
    try:
        print('Requesting url: ', url)
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    #解析电影的ID
    soup = BeautifulSoup(text, "lxml")
    results = soup.find_all('tr')
    print(results)

def main():
    crawSchedule()
    return

if __name__ == '__main__':
    main()