# -*- coding: utf-8 -*-
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
import m04_movie_schedule
import MovieUtils

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


# 获取影片在每个城市具体日期的具体片信息
def craw_city_movie_schedule(date_url):
    url = BASE_URL + date_url
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

    # 获取图片的url
    img_urls = re.findall('<img src="(http.*?)"', html_text)

    # 解析图片并将解析结果替换原来的html文本
    for i in range(len(img_urls)):
        # MovieUtils.downloadImg(img_urls[i], 'schedule.png')
        # img_urls[i] = MovieUtils.parseImg('schedule.png')
        html_text = re.sub('<img src="(http.*?)" />', img_urls[i], html_text, count=1)

    # 利用pandas的read_html函数获取到表格
    table = pd.read_html(html_text, header=0)[1]
    return table


# 保存到数据库
def save2db(table, date, movie_id, movie_name, city):
    # 打开数据库连接
    conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()

    # SQL 语句
    sql = 'replace into city_movie_schedule (MovieID58921, Name58921, ScheduleDate, ScheduleCity, ScheduleCinema, ' \
          'Total, Elapsed, Seats, Prime) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) '

    # 按行插入数据库
    for i in range(len(table.index)):
        try:
            # 执行sql语句
            # cursor.execute(sql, [movie_id, movie_name, date, city, table.ix[i][] table.ix[i][j]])
            # 提交到数据库执行
            conn.commit()
        except:
            # 发生错误时回滚
            conn.rollback()

def main():
    craw_city_list(6411)
    # 首页热门影片列表
    movie_list = m04_movie_schedule.craw_movie_list()


if __name__ == '__main__':
    main()
