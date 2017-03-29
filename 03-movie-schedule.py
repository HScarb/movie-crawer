# -*- coding: utf-8 -*-
import requests
import re
import pandas as pd
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

    # 获取图片的url
    img_urls = re.findall('<img src="(http.*?)"', html_text)

    # 解析图片并将解析结果替换原来的html文本
    for i in range(len(img_urls)):
        MovieUtils.downloadImg(img_urls[i], 'schedule.png')
        img_urls[i] = MovieUtils.parseImg('schedule.png')
        html_text = re.sub('<img src="(http.*?)" />', img_urls[i], html_text, count=1)

    # 利用pandas的read_html函数获取到表格
    table = pd.read_html(html_text, header=0)[0]
    return table


# 主函数
def main():
    craw_schedule(6189)  # 这里因为movieID不一致，先做模拟测试
    return


if __name__ == '__main__':
    main()
