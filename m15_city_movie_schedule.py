# -*- coding: utf-8 -*-
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import m04_movie_schedule

# 默认等待时间
DEFAULT_TIMEOUT = 10
# 58921的url
BASE_URL = 'http://pp.58921.com'


# 获取城市列表的爬虫
def craw_city_list(movie_id):
    url = 'http://pp.58921.com/film/' + str(movie_id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/48.0.2564.116 Safari/537.36 '
    }
    html_text = ''
    # 抓取整个网页
    try:
        print('Requesting url: ', url)
        html_text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None

    # 编码修改，防止出现中文乱码
    html_text = html_text.encode('latin1').decode('utf-8')

    # 电影名称
    soup = BeautifulSoup(html_text, "lxml")
    movie_name = str(soup.find_all('div', class_="page-header")[0].h1.text).split('排片')[0]

    # 获取城市url列表
    city_list = re.findall('<a href="(/film/.*?)" .*?>', html_text)
    return city_list, movie_name


# 获取城市具体排片日期列表的爬虫
def craw_movie_date_list(city):
    url = BASE_URL + city
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/48.0.2564.116 Safari/537.36 '
    }
    html_text = ''
    # 抓取整个网页
    try:
        print('Requesting url: ', url)
        html_text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None

    # 编码修改，防止出现中文乱码
    # html_text = html_text.encode('latin1').decode('utf-8')

    # 获取排片日期列表
    reg = r'<a href="(' + city + '/.*?)" .*?>'
    date_list = re.findall(reg, html_text)
    return date_list


def main():
    craw_city_list(6411)
    # 首页热门影片列表
    movie_list = m04_movie_schedule.craw_movie_list()


if __name__ == '__main__':
    main()
