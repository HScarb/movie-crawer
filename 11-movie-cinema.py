import MovieUtils
import requests
import re
import execjs   # execute javascript from python
import datetime #
import mysql.connector

DEFAULT_TIMEOUT = 10                # 默认等待时间

conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()

def getCinemaShowtime(cinemaId, date):
    '''
    根据影院ID和日期，获取该影院该日的拍片情况
    :param cinemaId: 影院ID
    :param date: 日期，格式为 20170404
    :return: 一个dict，可通过['value']['showtimes']得到showtimes
    '''
    url = 'http://service.theater.mtime.com/Cinema.api?Ajax_CallBack=true' \
          '&Ajax_CallBackType=Mtime.Cinema.Services&Ajax_CallBackMethod=GetShowtimesJsonObjectByCinemaId&' \
          'Ajax_CallBackArgument0=' + str(cinemaId) + '&Ajax_CallBackArgument1=' + str(date)
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
    text = ''
    movieIDList = []
    # 抓取整个网页
    try:
        print('Requesting url: ', url)
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    var = re.match(r'^var GetShowtimesJsonObjectByCinemaResult = (.+);', text).group(1)     # 获取javascript值
    if var:
        var = execjs.eval(var)      # 用库处理js值
        return var
    return None

def getMovieInfoFromMtime(mtimeMovieID):
    '''
    根据时光网的movieID，获得电影的中英文名
    :param mtimeMovieID: 时光网的movieID
    :return: 一个dict,包含movieID和中英文名
    '''
    url = 'http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&' \
          'Ajax_CallBackMethod=GetOnlineTicketByMovieId&Ajax_CallBackArgument0=' + str(mtimeMovieID)
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
    text = ''
    dict = {
        'MovieID' : mtimeMovieID,
        'CName' : None,
        'EName' : None
    }
    try:
        print('Requesting url: ', url)
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    var = re.match(r'^var GetOnlineTicketByMovieIdResult = (.+);', text).group(1)
    if var:
        var = execjs.eval(var)
    else:
        return dict
    if 'titlecn' in var['value']:
        dict['CName'] = var['value']['titlecn']
    if 'titleen' in var['value']:
        dict['EName'] = var['value']['titleen']
    return dict

def saveShowtime(showtime, cinemaID):
    dict = {
        'CinemaID': cinemaID,
        'MtimeMovieID': None,
        'ID': None,             # 可以用来查该场次座位情况 http://piao.mtime.com/onlineticket/showtime/ID/
        'ShowtimeID': None,
        'HallID': None,
        'SeatCount': None,
        'HallName': None,
        'Language': None,
        'StartTime': None,
        'EndTime': None,
        'Price': None,
        'Version': None
    }
    try:
        dict['MtimeMovieID'] = showtime['movieId']
        dict['ID'] = showtime['id']
        dict['ShowtimeID'] = showtime['showtimeId']
        dict['HallID'] = showtime['hallId']
        dict['SeatCount'] = showtime['seatCount']
        dict['HallName'] = showtime['hallName']
        dict['Language'] = showtime['language']
        dict['StartTime'] = showtime['realtime']
        dict['EndTime'] = showtime['movieEndTime']
        dict['Price'] = showtime['mtimePrice']
        dict['Version'] = showtime['version']
    except Exception as e:
        print(e)
    # save into db
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')      # 关闭外键检测
    conn.commit()
    try:
        cursor.execute(
            'replace into showtime'
            '(CinemaID, MtimeMovieID, ID, ShowtimeID, HallID, SeatCount, HallName, Language, StartTime, EndTime, Price, Version)'
            'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            [dict['CinemaID'], dict['MtimeMovieID'], dict['ID'], dict['ShowtimeID'], dict['HallID'], dict['SeatCount'], dict['HallName'],
            dict['Language'], dict['StartTime'], dict['EndTime'], dict['Price'], dict['Version']]
        )
        conn.commit()
    except Exception as e:
        print('Error in saveShowtime.')
        print(e)

def carweAndSaveMtimeMovieInfo():
    cursor.execute('SELECT MtimeMovieID FROM showtime GROUP BY MtimeMovieID')
    movieIdList = cursor.fetchall()
    print(movieIdList)

def saveShowtimes(cinemaShowtimes):
    # 截取showtimes
    cinemaId = cinemaShowtimes['value']['cinemaId']
    cinemaShowtimes = cinemaShowtimes['value']['showtimes']
    for showtime in cinemaShowtimes:
        saveShowtime(showtime, cinemaId)

def main():
    saveShowtimes(getCinemaShowtime(3065, 20170405))
    getMovieInfoFromMtime(195064)
    carweAndSaveMtimeMovieInfo()

if __name__ == '__main__':
    main()