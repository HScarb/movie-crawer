import requests
import re
import random
from time import sleep
from bs4 import BeautifulSoup

DEFAULT_TIMEOUT = 10                # 默认等待时间

def crawCurrentMovie():
    '''
    获取当前正在上映的电影
    :return: 返回一组正在上映电影的ID  List格式
    '''
    url = 'http://www.cbooo.cn/'
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
    text = ''
    movieIDList = []
    print('Crawing current movie...')
    # 抓取整个网页
    try:
        print('Requesting url: ', url)
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    # 解析电影的ID
    soup = BeautifulSoup(text, "lxml")                      # 把网页保存为一个BeautifulSoup对象
    results = soup.find_all('tr', class_='trtop', onmouseover='ChangeTopR(this.id)')
    for result in results:
        print(result['id'])
        movieIDList.append(result['id'])
    return movieIDList

def crawMovie(movieID):
    '''
    根据电影的ID,爬取电影的信息
    包括 名称,类型,片长,制式,导演,主演,制作公司,发行公司
    :param movieID: CBO上电影的ID
    :return:一个Dict,存储有电影的信息
    '''
    url = 'http://www.cbooo.cn/m/' + str(movieID)
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
    text = ''
    movieDataDict = {}
    print('Crawing movie info ', url)
    # 抓取整个网页
    try:
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    # 解析电影的信息
    soup = BeautifulSoup(text, "lxml")
    result1 = soup.find('div', class_='cont')               # 标题等信息
    result2 = soup.find('dl', class_='dltext')
    #print(result1.h2.text)
    for element in result1.stripped_strings:
        print(element.replace('\r','').replace('\n','').replace(' ', ''))
    for element in result2.stripped_strings:
        print(element)
    pass

def crawActor(actorID):
    '''
    根据演员的ID,爬取演员信息
    包括 名称,已发布作品,未发布作品
    :param actorID:
    :return:
    '''

def main():
    list = crawCurrentMovie()
    moveDataList = []
    for movieID in list:
        moveDataList.append(crawMovie(movieID))
    return list

if __name__ == '__main__':
    main()