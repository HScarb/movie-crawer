import MovieUtils
import requests
import re
import execjs   # execute javascript from python
import datetime #

DEFAULT_TIMEOUT = 10                # 默认等待时间

def getCinemaMovie(cinemaId, date):
    '''
    根据影院ID和日期，获取该影院该日的拍片情况
    :param cinemaId: 影院ID
    :param date: 日期，格式为 20170404
    :return: 包含所有shotimes信息的list
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
        return var['value']['showtimes']
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

def main():
    getCinemaMovie(3065, 20170405)
    getMovieInfoFromMtime(195064)

if __name__ == '__main__':
    main()