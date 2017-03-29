# -*- coding: utf-8 -*-
import requests
import 
from bs4 import BeautifulSoup

import MovieUtils

# 默认等待时间
DEFAULT_TIMEOUT = 10


# 爬虫
def crawSchedule(movieId):
    url = 'http://pp.58921.com/film/' + str(movieId)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/48.0.2564.116 Safari/537.36 '
    }
    text = ''
    # 抓取整个网页
    try:
        print('Requesting url: ', url)
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None

    # 编码修改，防止出现中文乱码
    text = text.encode('latin1').decode('utf-8')
    soup = BeautifulSoup(text, "lxml")

# 主函数
def main():
    crawSchedule(6189)  # 这里因为movieID不一致，先做模拟测试
    return


if __name__ == '__main__':
    main()
