import MovieUtils
import requests
import mysql.connector
import json
import m01_current_movie as cm
import re
from bs4 import BeautifulSoup

DEFAULT_TIMEOUT = 10
conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }

def crawhistoryMovie(year,page):
    url = 'http://www.cbooo.cn/Mdata/getMdata_movie?area=50&type=0&year=' + str(year) + '&initial=%E5%85%A8%E9%83%A8&pIndex=' + str(page)
    MovieDict = {
        'ID' : None,
        'tPage' : None
    }
    MovieList = []
    print('Crawing movie : ',url)
    text = ''
    try:
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    data = json.loads(text)
    db = data['pData']
    for element in db:
        MovieList.append(element['ID'])
    pass

    return MovieList

def saveMovieInDatabase(movieDataDict):
    print('Saving movie # ', movieDataDict['id'], ' into data base...')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')      # 关闭外键检测
    conn.commit()
    try:
        cursor.execute(
            'replace into movie'
            '(MovieID, CName, EName, Type, Length, ReleaseTime, Standard, SumBoxOffice)'
            'values (%s, %s, %s, %s, %s, %s, %s, %s)',
            [movieDataDict['id'], movieDataDict['cname'], movieDataDict['ename'],
             movieDataDict['type'], movieDataDict['length'], movieDataDict['releasetime'],
             movieDataDict['standard'], movieDataDict['sumboxoffice']]
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
    text = ''
    MovieList = []
    for year in range(2010,2018):
        url = 'http://www.cbooo.cn/Mdata/getMdata_movie?area=50&type=0&year=' + str(year) + '&initial=%E5%85%A8%E9%83%A8&pIndex=1'
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
        data = json.loads(text)
        tpage = data['tPage']
        for page in range(1,tpage+1):
            MovieList = crawhistoryMovie(year,page)
            for element in MovieList:
                saveMovieInDatabase(cm.crawMovie(element))


if __name__ == '__main__':
    main()






