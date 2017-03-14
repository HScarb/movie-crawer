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
    movieDataDict = {'cname':None,
                     'ename':None,
                     'type':None,
                     'length':None,
                     'releasetime':None,
                     'standard':None,
                     'director':None,
                     'productioncompany':None,
                     'publisher':None,
                     'sumboxoffice':None}
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
    result2 = result2.find_all('dd')
    #print(result1.h2.text)
    i = 0
    isSumBoxOffice = False
    for element in result1.stripped_strings:
        if isSumBoxOffice == True:
            movieDataDict['sumboxoffice'] = int(float(element[0:-1]) * 10000)
            isSumBoxOffice = False
        elif i == 0:
            movieDataDict['cname'] = element
        elif i == 2:
            movieDataDict['ename'] = element
        elif element[0] == '类':
            movieDataDict['type'] = element[3:]
        elif element[0] == '片':
            movieDataDict['length'] = element.replace('\r','').replace('\n','').replace(' ', '')[3:-3]
        elif element[0] == '上':
            dateStr = element[5:-6]
            # 需要处理字符串成日期的形式
            movieDataDict['releasetime'] = element[5:-4]
        elif element[0] == '制':
            movieDataDict['standard'] = element[3:]
        elif element[0] == '累':
            isSumBoxOffice = True
        i = i + 1

    i = 0
    print(movieDataDict)
    for element in result2:
        '''
        i = 0: 导演
            1: 主演
            2: 制作公司
            3: 发行公司
        '''
        links = element.find_all('a')
        for link in links:
            print(link)

        i = i + 1

    pass

def crawActor(actorID):
    '''
    根据演员的ID,爬取演员信息
    包括 名称,已发布作品,未发布作品
    :param actorID:
    :return:
    '''
    pass

def main():
    list = crawCurrentMovie()
    moveDataList = []
    for movieID in list:
        moveDataList.append(crawMovie(movieID))
        crawMovie(movieID)
    return list

if __name__ == '__main__':
    main()