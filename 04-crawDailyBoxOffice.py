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
        json_data = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text  #爬取json数据并转换类型
    except:
        print('Error when request url=', url)
        return None
    movieBoxOfficeList = json.loads(json_data)['data1']  #将json网页数据通过json库转换为list
    for movieBoxOfficeDict in movieBoxOfficeList:
        movieBoxOfficeDict['Date'] = MovieUtils.str2date(current_Date.strftime('%Y-%m-%d'))  #在每日的票房Dict中添加日期
        del movieBoxOfficeDict['MovieImg']   #删除Dict中的无效键值
        movieBoxOfficeDict['BoxOffice'] = 10000 * int(movieBoxOfficeDict['BoxOffice'])   #票房数值单位转换
        print(movieBoxOfficeDict)
    return movieBoxOfficeList

def saveBoxOfficeInDataBase(boxOffice):
    print('Saving movie box office # ', boxOffice['Date'], boxOffice['MovieID'], boxOffice['MovieName'],
          ' into data base...')
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
    print('Flash movie box office # ', boxOffice['date'], boxOffice['id'], ' into data base...')
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
    if data1:
        newestData = int(data1[0][1])
        flashMovieBoxOfficeList = []
        for da in data1:
            flashMovieBoxOfficeDict = {'id': None,
                                       'date': None,
                                       'boxoffice': None,
                                       'avgpeople': None}
            if int(da[2]) < 10000:   #检查已经存在db的票房数据是否有未转换的Dict
                flashMovieBoxOfficeDict['id'] = da[0]
                flashMovieBoxOfficeDict['date'] = str(da[1])
                flashMovieBoxOfficeDict['boxoffice'] = int(da[2]) * 10000
                flashMovieBoxOfficeDict['avgpeople'] = da[3]
                flashMovieBoxOfficeList.append(flashMovieBoxOfficeDict)
                print(da)
            if newestData < int(da[1]):
                newestData = int(da[1])
        if flashMovieBoxOfficeList:
            for boxOfficeInDatabase in flashMovieBoxOfficeList:
                flashBoxOfficeInDataBase(boxOfficeInDatabase)       #更新字典里面的票房数据
        currentDate = MovieUtils.str2date(datetime.now().strftime('%Y-%m-%d'))
        return (newestData - int(currentDate))  #如果db中的movie_boxoffice已有数据则返回db中的最新日期和当前日期的差值
    else:
        return data1   #如果服务器中没有数据则返回空



def movieBoxOffice():
    dailyMovieBoxOfficeList = []
    newestDay = getMovieBoxOfficeNewestDateInDatabase()
    print(newestDay)
    if newestDay :
        if newestDay <= -8:
            for i in range(-8, 1):
                dailyMovieBoxOfficeList.append(crawDailyBoxOffice(i))
        else:
            for i in range(newestDay, 1):
                dailyMovieBoxOfficeList.append(crawDailyBoxOffice(i))
    elif newestDay ==0:
        dailyMovieBoxOfficeList.append(crawDailyBoxOffice(0))
    else:
        for i in range(-8, 1):
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