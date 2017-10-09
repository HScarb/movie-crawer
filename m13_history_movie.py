import MovieUtils
import requests
import mysql.connector
import json
import m01_current_movie as cm
import m02_actor_company as ac
import re
from bs4 import BeautifulSoup

DEFAULT_TIMEOUT = 10
conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }

def crawhistoryMovie(area,year,page):
    url = 'http://www.cbooo.cn/Mdata/getMdata_movie?area=' + str(area) + '&type=0&year=' + str(year) + '&initial=%E5%85%A8%E9%83%A8&pIndex=' + str(page)
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
    try:
        print('Saving movie # ', movieDataDict['id'], ' into data base...')
    except:
        print('error in saving id')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')      # 关闭外键检测
    conn.commit()
    try:
        cursor.execute(
            'replace into movie'
            '(MovieID, MovieCName, MovieEName, MovieType, MovieLength, MovieReleaseTime, MovieStandard, MovieSumBoxOffice)'
            'values (%s, %s, %s, %s, %s, %s, %s, %s)',
            [movieDataDict['id'], movieDataDict['cname'], movieDataDict['ename'],
             movieDataDict['type'], movieDataDict['length'], movieDataDict['releasetime'],
             movieDataDict['standard'], movieDataDict['sumboxoffice']]
        )
        conn.commit()
    except Exception as e:
        print('Error in saveMovieInDatabase Step 1.')
        print(e)
    try:
        for person in movieDataDict['director']:
            try:
                cursor.execute(
                    'replace into movie_actor'
                    '(MovieID, ActorID, ActorRank, ActorRole)'
                    'values (%s, %s, %s, %s)',
                    [movieDataDict['id'], person['id'], person['rank'], 'director']
                )
                conn.commit()
            except Exception as e:
                print('Error in saveMovieInDatabase Step 2 director.')
                print(e)
    except Exception as f:
        print('Error in director')
        print(f)
    try:
        for person in movieDataDict['actor']:
            try:
                cursor.execute(
                    'replace into movie_actor'
                    '(MovieID, ActorID, ActorRank, ActorRole)'
                    'values (%s, %s, %s, %s)',
                    [movieDataDict['id'], person['id'], person['rank'], 'actor']
                )
                conn.commit()
            except Exception as e:
                print('Error in saveMovieInDatabase Step 3 actor.')
                print(e)
    except Exception as f:
        print('Error in actor')
        print(f)
    for person in movieDataDict['producer']:
        try:
            cursor.execute(
                'replace into movie_company'
                '(MovieID, CompanyID, CompanyRank, CompanyRole)'
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
                '(MovieID, CompanyID, CompanyRank, CompanyRole)'
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
    # 美area=1,德area=16,中area=50,台湾area=40,英area=25,法area=4, 日area=30,加拿大area=2
    areaID = ['50', '40', '1', '25', '4', '2', '30']
    text = ''
    MovieList = []
    for year in range(2015,2018):
        for area in range(0,7):
            url = 'http://www.cbooo.cn/Mdata/getMdata_movie?area=' + str(areaID[area]) + '&type=0&year=' + str(year) + '&initial=%E5%85%A8%E9%83%A8&pIndex=1'
            text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
            data = json.loads(text)
            tpage = data['tPage']
            for page in range(1,tpage+1):
                MovieList = crawhistoryMovie(areaID[area],year,page)
                for element in MovieList:
                    cursor.execute('select ' + str(element) + ' from movie.actor')
                    diffList = cursor.fetchall()
                    ## if diffList == None:
                    saveMovieInDatabase(cm.crawMovie(element))


if __name__ == '__main__':
    main()







