import MovieUtils
import requests
import mysql.connector
import json
from datetime import datetime, timedelta

DEFAULT_TIMEOUT = 10                # 默认等待时间
conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()

def crawDailyBoxOffice(i):
    url = 'http://www.cbooo.cn/BoxOffice/GetDayBoxOffice?num=' + str(i)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    json_data = ''
    current_Date = datetime.now() - timedelta(days=abs(i))
    print(current_Date.strftime('%Y-%m-%d'))
    print('Crawing movie Booking', url)
    # 抓取整个网页# 抓取整个网页
    try:
        json_data = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    movieBoxOfficeList = json.loads(json_data)['data1']
    for movieBoxOfficeDict in movieBoxOfficeList:
        movieBoxOfficeDict['Date'] = MovieUtils.str2date(current_Date.strftime('%Y-%m-%d'))
        del movieBoxOfficeDict['MovieImg']
        print(movieBoxOfficeDict)
    return movieBoxOfficeList

def saveBoxOfficeInDataBase(boxOffice):
    print('Saving movie box office # ', boxOffice['Date'], boxOffice['MovieName'], ' into data base...')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')  # 关闭外键检测
    conn.commit()
    try:
        cursor.execute(
            'replace into movie_boxoffice'
            '(MovieID, Date, BoxOffice, AvgPeople)'
            'values (%s, %s, %s, %s)',
            [boxOffice['MovieID'], boxOffice['Date'], boxOffice['BoxOffice'], boxOffice['AvpPeoPle']]
        )
        conn.commit()
    except Exception as e:
        print('Error in saveMovieInDatabase Step 1.')
        print(e)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')  # 重新开启外键检测
    conn.commit()

def movieBoxOffice():
    dailyMovieBoxOfficeList = []
    for i in range(-8, 0):
        dailyMovieBoxOfficeList.append(crawDailyBoxOffice(i))
    return dailyMovieBoxOfficeList
def main():
    dailyMovieBoxOfficeList = movieBoxOffice()
    for dailyBoxOffice in dailyMovieBoxOfficeList:
        for boxOffice in dailyBoxOffice:
            saveBoxOfficeInDataBase(boxOffice)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()