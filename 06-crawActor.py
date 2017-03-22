import requests
import MovieUtils
import re
import random
import chardet
from urllib.request import urlopen
from time import sleep
from bs4 import BeautifulSoup
import mysql.connector

DEFAULT_TIMEOUT = 10
conn = mysql.connector.connect(user='root', password='3347689',database = 'movie')
cursor = conn.cursor()


def crawActor(actorID):     #获得演员的数据，返回一个字典
    '''
        根据演员的ID,爬取演员信息
        包括 名称,已发布作品,未发布作品
        :param actorID:
        :return:
        '''
    url = 'http://www.cbooo.cn/p/' + str(actorID) # 周杰伦1893
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    text = ''
    actorDataDict = {  'ActorID':actorID,
                       'CName':None,
                       'EName':None,
                       'Nation':None }
    print('Crawing actor info: ',url)
    #抓取整个网页
    try:
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    soup = BeautifulSoup(text, "lxml")
    taxi = soup.find('div', class_='cont')
    i = 0
    isActorReady = False
    if str(actorID) != 2265340:
        for element in taxi.stripped_strings:
            #print(element.replace('\r', '').replace('\n', '').replace(' ', ''))
            if isActorReady == True:
                isActorReady = False
            elif i == 0:
                actorDataDict['CName'] = element
            elif i == 1:
                actorDataDict['EName'] = element
            elif element[0] == '国':
                actorDataDict['Nation'] = element[3:]
            elif element[0] == '生':
                isActorReady = True
            i = i + 1
    i = 0
    pass
    cars = soup.find('div', class_='ziliaofr').find('div', class_='starring')
    for car in cars.stripped_strings:
        #print(car)
        pass
    pass
    # soup_IO = BeautifulSoup(text_IO, "lxml")
    # buses = soup_IO.find('p')
    # for bus in buses:
    #     print(bus['MovieName'])
    # pass
    #添加把这里得到的东西移入到actorDataDict字典里面
    return actorDataDict

def saveActorInDatabase(actorDataDict):
    print('Saving actor # ', actorDataDict['ActorID'],'into data base...')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')  # 关闭外键检测
    conn.commit()
    try:
        cursor.execute(
            'replace into actor'
            '(ActorID, CName, EName, Nation)'
            'values(%s, %s, %s, %s)',
            [actorDataDict['ActorID'],actorDataDict['CName'],actorDataDict['EName'],actorDataDict['Nation']]
        )
        conn.commit()
    except Exception as e:
        print('Error in saveActorInDatabase: ', e)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')  # 重新开启外键检测
    conn.commit()

def main():
    #ID = 1893
    #saveActorInDatabase(crawActor(ID))          #参数是字典
    cursor.execute('select ActorID from movie.movie_actor')
    val = cursor.fetchall()
    for element in val:
        for value in element:
            if(value != 2265340):
                saveActorInDatabase(crawActor(value))
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()