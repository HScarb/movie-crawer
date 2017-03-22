import MovieUtils
import requests
from bs4 import BeautifulSoup
import mysql.connector

DEFAULT_TIMEOUT = 10
conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()


def crawActor(actorID):
    '''
        根据演员的ID,爬取演员信息
        包括 名称,已发布作品,未发布作品
        :param actorID:
        :return:
        '''
    url = 'http://www.cbooo.cn/p/' + str(actorID)
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
    try:
        for element in taxi.stripped_strings:
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
    except Exception as a:
        print('Error in CRAWING # ' + str(actorID) ,'into data base')
    pass
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
    cursor.execute('select ActorID from movie.movie_actor')
    val = cursor.fetchall()
    for element in val:
        for value in element:
            saveActorInDatabase(crawActor(value))
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()