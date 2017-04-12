import MovieUtils
import requests
import mysql.connector
import json
import m01_current_movie
import re
from bs4 import BeautifulSoup

DEFAULT_TIMEOUT = 10
conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()

def crawhistoryMovie(page):
    #      http://www.cbooo.cn/Mdata/getMdata_movie?area=50&type=0&year=0&initial=%E5%85%A8%E9%83%A8&pIndex=9
    #      http://www.cbooo.cn/Mdata/getMdata_movie?area=50&type=0&year=0&initial=%E5%85%A8%E9%83%A8&pIndex=22
    url = 'http://www.cbooo.cn/Mdata/getMdata_movie?area=50&type=0&year=2017&initial=%E5%85%A8%E9%83%A8&pIndex=' + str(page)        #每个年份的page数都不一样
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    MovieDict = {
        'ID' : None         #根据ID，用01去爬影片
    }
    MovieList = []
    print('Crawing movie : ',url)
    text = ''
    try:
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
        print(text)
    except:
        print('Error when request url=', url)
        return None

    data = json.loads(text)
    data = data['pData']
    for element in data:
        MovieList.append(element['ID'])
    pass

    for element in MovieList:
        print(element)
    return MovieList

# def crawMovie(movieID):
#     '''
#     根据电影的ID,爬取电影的信息
#     包括 名称,类型,片长,制式,导演,主演,制作公司,发行公司
#     :param movieID: CBO上电影的ID
#     :return:一个Dict,存储有电影的信息
#     '''
#     url = 'http://www.cbooo.cn/m/' + str(movieID)
#     headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
#         }
#     text = ''
#     movieDataDict = {'id':movieID,
#                      'cname':None,
#                      'ename':None,
#                      'type':None,
#                      'length':None,
#                      'releasetime':None,
#                      'standard':None,
#                      'director':None,
#                      'actor':None,
#                      'producer':None,
#                      'publisher':None,
#                      'sumboxoffice':None}
#     print('Crawing movie info ', url)
#     # 抓取整个网页
#     try:
#         text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
#     except:
#         print('Error when request url=', url)
#         return None
#     # 解析电影的信息
#     soup = BeautifulSoup(text, "lxml")
#     result1 = soup.find('div', class_='cont')               # 标题等信息
#     result2 = soup.find('dl', class_='dltext')
#     result2 = result2.find_all('dd')
#     #print(result1.h2.text)
#     i = 0
#     isSumBoxOffice = False
#     for element in result1.stripped_strings:
#         if isSumBoxOffice == True:
#             movieDataDict['sumboxoffice'] = int(float(element[0:-1]) * 10000)
#             isSumBoxOffice = False
#         elif i == 0:
#             movieDataDict['cname'] = element
#         elif i == 2:
#             movieDataDict['ename'] = element
#         elif element[0] == '类':
#             movieDataDict['type'] = element[3:]
#         elif element[0] == '片':
#             movieDataDict['length'] = element.replace('\r','').replace('\n','').replace(' ', '')[3:-3]
#         elif element[0] == '上':
#             # 需要处理字符串成日期的形式
#             movieDataDict['releasetime'] = MovieUtils.str2date(element[5:-4])
#         elif element[0] == '制':
#             movieDataDict['standard'] = element[3:]
#         elif element[0] == '累':
#             isSumBoxOffice = True
#         i = i + 1
#
#     i = 0
#     for element in result2:
#         '''
#         i = 0: 导演
#             1: 主演
#             2: 制作公司
#             3: 发行公司
#         '''
#         memberList = []
#         rank = 0
#         links = element.find_all('a')
#         for link in links:
#             rank = rank + 1
#             idMatched = re.match(r'^(http://www.cbooo.cn/(p|c)/)(\d+)$', link['href'])
#             if idMatched:
#                 memberList.append({'id':int(idMatched.group(3)), 'rank':rank})
#
#         if i == 0:
#             movieDataDict['director'] = memberList
#         elif i == 1:
#             movieDataDict['actor'] = memberList
#         elif i == 2:
#             movieDataDict['producer'] = memberList
#         elif i == 3:
#             movieDataDict['publisher'] = memberList
#         i = i + 1
#     print(movieDataDict)
#     return movieDataDict

def saveMovieInDatabase(movieDataDict):
    print('Saving movie # ', movieDataDict['id'], ' into data base...')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')      # 关闭外键检测
    conn.commit()
    try:
        cursor.execute(
            'replace into movie'
            '(MovieID, CName, EName, Type, Length, ReleaseTime, Standard, SumBoxOffice, AvgPrice, AvgPeople, WomIndex)'
            'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            [movieDataDict['id'], movieDataDict['cname'], movieDataDict['ename'],
             movieDataDict['type'], movieDataDict['length'], movieDataDict['releasetime'],
             movieDataDict['standard'], movieDataDict['sumboxoffice'], movieDataDict['AvgPrice'], movieDataDict['AvgPeople'], movieDataDict['WomIndex']]
        )
        conn.commit()
    except Exception as e:
        print('Error in saveMovieInDatabase Step 1.')
        print(e)
    for person in movieDataDict['director']:
        try:
            cursor.execute(
                'replace into movie_actor'
                '(MovieID, ActorID, Rank, Role)'
                'values (%s, %s, %s, %s)',
                [movieDataDict['id'], person['id'], person['rank'], 'director']
            )
            conn.commit()
        except Exception as e:
            print('Error in saveMovieInDatabase Step 2 director.')
            print(e)
    for person in movieDataDict['actor']:
        try:
            cursor.execute(
                'replace into movie_actor'
                '(MovieID, ActorID, Rank, Role)'
                'values (%s, %s, %s, %s)',
                [movieDataDict['id'], person['id'], person['rank'], 'actor']
            )
            conn.commit()
        except Exception as e:
            print('Error in saveMovieInDatabase Step 3 actor.')
            print(e)
    for person in movieDataDict['producer']:
        try:
            cursor.execute(
                'replace into movie_company'
                '(MovieID, CompanyID, Rank, Role)'
                'values (%s, %s, %s, %s)',
                [movieDataDict['id'], person['id'], person['rank'], 'producer']
            )
            conn.commit()
        except Exception as e:
            print('Error in saveMovieInDatabase Step 4 producer.')
            print(e)
    for person in movieDataDict['publisher']:
        try:
            cursor.execute(
                'replace into movie_company'
                '(MovieID, CompanyID, Rank, Role)'
                'values (%s, %s, %s, %s)',
                [movieDataDict['id'], person['id'], person['rank'], 'publisher']
            )
            conn.commit()
        except Exception as e:
            print('Error in saveMovieInDatabase Step 5 publisher.')
            print(e)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')      # 重新开启外键检测
    conn.commit()

def main():
    MovieList = []
    for page in range(1,9):
        MovieList = crawhistoryMovie(page)
        for element in MovieList:
            sys.crawMovie(element)
    pass

if __name__ == '__main__':
    main()







