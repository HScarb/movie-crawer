# -*- coding: utf-8 -*-
import requests
import re
import pandas as pd
import mysql.connector
from bs4 import BeautifulSoup

import MovieUtils

# 默认等待时间
DEFAULT_TIMEOUT = 10


# 爬虫
def craw_schedule(movie_id):
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

    # 获取图片的url
    img_urls = re.findall('<img src="(http.*?)"', html_text)

    # 解析图片并将解析结果替换原来的html文本
    for i in range(len(img_urls)):
        # MovieUtils.downloadImg(img_urls[i], 'schedule.png')
        # img_urls[i] = MovieUtils.parseImg('schedule.png')
        html_text = re.sub('<img src="(http.*?)" />', img_urls[i], html_text, count=1)

    # 利用pandas的read_html函数获取到表格
    table = pd.read_html(html_text, header=0)[0]
    return table, movie_name


# 获取首页热门影片列表的爬虫
def craw_movie_list():
    url = 'http://pp.58921.com'
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

    soup = BeautifulSoup(html_text, "lxml")
    links = soup.find_all('table', class_="table table-bordered table-condensed")[0].find_all('a')

    # 当前热门影片id列表
    movie_list = []
    for link in links:
        movie_list.append(str(link.get('href')).split('/film/')[1])
    return movie_list


# 保存数据到数据库,这里只是做一个简单的测试，确定用于工作时请将数据库连接写在配置文件中
def save2db(table, movie_id, movie_name):
    # 打开数据库连接
    conn = mysql.connector.connect(user='root', password='wanglixian', database='movie')
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()

    # SQL 语句
    sql = 'replace into movie_scene (movie_id, movie_name, city, date, scene) values (%s, %s, %s, %s, %s)'

    # 按行插入数据库
    for i in range(len(table.index)):
        date = table.ix[i]['日期']
        # 对每个城市操作
        for j in range(1, len(table.columns)):
            try:
                # 执行sql语句
                cursor.execute(sql, [movie_id, movie_name, table.columns[j], date, table.ix[i][j]])
                # 提交到数据库执行
                conn.commit()
            except:
                # 发生错误时回滚
                conn.rollback()

    # 关闭数据库连接
    cursor.close()
    conn.close()


# 主函数
def main():
    movie_list = craw_movie_list()

    for i in range(len(movie_list)):
        table, movie_name = craw_schedule(movie_list[i])  # 这里因为movieID不一致，先做模拟测试
        save2db(table=table, movie_id=movie_list[i], movie_name=movie_name)

    return


if __name__ == '__main__':
    main()
