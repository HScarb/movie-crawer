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
        movieBoxOfficeDict['BoxOffice'] = 10000 * int(movieBoxOfficeDict['BoxOffice'])
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

def flashBoxOfficeInDataBase(boxOffice):
    print('Saving movie box office # ', boxOffice['date'], boxOffice['id'], ' into data base...')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')  # 关闭外键检测
    conn.commit()
    try:
        cursor.execute(
            'replace into movie_boxoffice'
            '(MovieID, Date, BoxOffice, AvgPeople)'
            'values (%s, %s, %s, %s)',
            [boxOffice['id'], boxOffice['date'], boxOffice['boxoffice'], boxOffice['avgpeople']]
        )
        conn.commit()
    except Exception as e:
        print('Error in saveMovieInDatabase Step 1.')
        print(e)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')  # 重新开启外键检测
    conn.commit()

def getMovieBoxOfficeNewestDateInDatabase():
    cursor.execute("select * from movie_boxoffice")
    data1 = cursor.fetchall()
    newestData = int(data1[0][1])
    flashMovieBoxOfficeList = []
    for da in data1:
        flashMovieBoxOfficeDict = {'id': None,
                        'date': None,
                        'boxoffice': None,
                        'avgpeople': None}
        if int(da[2]) < 10000:
            flashMovieBoxOfficeDict['boxoffice'] = int(da[2])*10000
            flashMovieBoxOfficeDict['id'] = da[0]
            flashMovieBoxOfficeDict['date'] = str(da[1])
            flashMovieBoxOfficeDict['avgpeople'] = da[2]
            flashMovieBoxOfficeList.append(flashMovieBoxOfficeDict)
        #print(da)
        if int(da[1]) > newestData:
            newestData = int(da[1])
    if flashMovieBoxOfficeList:
        for boxOfficeDict in flashMovieBoxOfficeList:
            flashBoxOfficeInDataBase(boxOfficeDict)
    currentDate = MovieUtils.str2date(datetime.now().strftime('%Y-%m-%d'))
    return (newestData - int(currentDate))

def movieBoxOffice():
    dailyMovieBoxOfficeList = []
    newestDay = getMovieBoxOfficeNewestDateInDatabase()
    if newestDay <=-8:
        for i in range(-8, 1):
            dailyMovieBoxOfficeList.append(crawDailyBoxOffice(i))
    else:
        for i in range(newestDay, 1):
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