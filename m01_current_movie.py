import MovieUtils
import requests
import re
import random
from time import sleep
from bs4 import BeautifulSoup
import mysql.connector
import json
from datetime import datetime, timedelta

DEFAULT_TIMEOUT = 10                # 默认等待时间

conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()

def crawCurrentMovie():
    '''
    获取当前正在上映的电影
    :return: 返回一组正在上映电影的ID  List格式
    '''
    url = 'http://www.cbooo.cn/'
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
    text = ''
    movieIDList = []
    print('Crawing current movie...')
    # 抓取整个网页
    try:
        print('Requesting url: ', url)
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    # 解析电影的ID
    soup = BeautifulSoup(text, "lxml")                      # 把网页保存为一个BeautifulSoup对象
    results = soup.find_all('tr', class_='trtop', onmouseover='ChangeTopR(this.id)')
    for result in results:
        print(result['id'])
        movieIDList.append(result['id'])
    return movieIDList

def crawMovie(movieID):
    '''
    根据电影的ID,爬取电影的信息
    包括 名称,类型,片长,制式,导演,主演,制作公司,发行公司
    :param movieID: CBO上电影的ID
    :return:一个Dict,存储有电影的信息
    '''
    url = 'http://www.cbooo.cn/m/' + str(movieID)
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
    text = ''
    movieDataDict = {'id':movieID,
                     'cname':None,
                     'ename':None,
                     'type':None,
                     'length':None,
                     'releasetime':None,
                     'standard':None,
                     'director':None,
                     'actor':None,
                     'producer':None,
                     'publisher':None,
                     'sumboxoffice':None}
    print('Crawing movie info ', url)
    # 抓取整个网页
    try:
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    # 解析电影的信息
    soup = BeautifulSoup(text, "lxml")
    result1 = soup.find('div', class_='cont')               # 标题等信息
    result2 = soup.find('dl', class_='dltext')
    result2 = result2.find_all('dd')
    #print(result1.h2.text)
    i = 0
    isSumBoxOffice = False
    for element in result1.stripped_strings:
        if isSumBoxOffice == True:
            movieDataDict['sumboxoffice'] = int(float(element[0:-1]) * 10000)
            isSumBoxOffice = False
        elif i == 0:
            movieDataDict['cname'] = element
        elif i == 2:
            movieDataDict['ename'] = element
        elif element[0] == '类':
            movieDataDict['type'] = element[3:]
        elif element[0] == '片':
            movieDataDict['length'] = element.replace('\r','').replace('\n','').replace(' ', '')[3:-3]
        elif element[0] == '上':
            # 需要处理字符串成日期的形式
            movieDataDict['releasetime'] = MovieUtils.str2date(element[5:-4])
        elif element[0] == '制':
            movieDataDict['standard'] = element[3:]
        elif element[0] == '累':
            isSumBoxOffice = True
        i = i + 1

    i = 0
    for element in result2:
        '''
        i = 0: 导演
            1: 主演
            2: 制作公司
            3: 发行公司
        '''
        memberList = []
        rank = 0
        links = element.find_all('a')
        for link in links:
            rank = rank + 1
            idMatched = re.match(r'^(http://www.cbooo.cn/(p|c)/)(\d+)$', link['href'])
            if idMatched:
                memberList.append({'id':int(idMatched.group(3)), 'rank':rank})

        if i == 0:
            movieDataDict['director'] = memberList
        elif i == 1:
            movieDataDict['actor'] = memberList
        elif i == 2:
            movieDataDict['producer'] = memberList
        elif i == 3:
            movieDataDict['publisher'] = memberList
        i = i + 1
    try:
        print(movieDataDict)
    except:
        return None
    return movieDataDict

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

def getMovieAvg(dailyMovieBoxOfficeList):
    movieAvgList = []
    for dailyBoxOffice in dailyMovieBoxOfficeList:
        for boxOffice in dailyBoxOffice:
            flag = 0
            movieAvgDict = {'id': None,
                            'avgPrice': None,
                            'avgPeople': None,
                            'movieDay': None,
                            'womIndex': None}
            if movieAvgList :
                for avg in movieAvgList:
                    if boxOffice['MovieID'] == avg['id']:
                        if boxOffice['AvgPrice'] is not avg['avgPrice']:
                            if avg['avgPeople'] is not boxOffice['AvpPeoPle']:
                                avg['avgPrice'] = int(avg['avgPrice']) + int(boxOffice['AvgPrice'])
                                avg['avgPeople'] = int(avg['avgPeople']) + int(boxOffice['AvpPeoPle'])
                                if int(avg['movieDay']) < int(boxOffice['MovieDay']):
                                    avg['movieDay'] = boxOffice['MovieDay']
                        flag = 1
                        break
                if flag == 0:
                    movieAvgDict['id'] = boxOffice['MovieID']
                    movieAvgDict['avgPrice'] = boxOffice['AvgPrice']
                    movieAvgDict['avgPeople'] = boxOffice['AvpPeoPle']
                    movieAvgDict['movieDay'] = boxOffice['MovieDay']
                    movieAvgDict['womIndex'] = boxOffice['WomIndex']
                    movieAvgList.append(movieAvgDict)
            else:
                movieAvgDict['id'] = boxOffice['MovieID']
                movieAvgDict['avgPrice'] = boxOffice['AvgPrice']
                movieAvgDict['avgPeople'] = boxOffice['AvpPeoPle']
                movieAvgDict['movieDay'] = boxOffice['MovieDay']
                movieAvgDict['womIndex'] = boxOffice['WomIndex']
                movieAvgList.append(movieAvgDict)

    for avg in movieAvgList:
        #print(avg)
        if int(avg['movieDay']) < 8 and int(avg['movieDay']) >0:
            avg['avgPrice'] = round(int(avg['avgPrice']) / int(avg['movieDay']), 2)
            avg['avgPeople'] = round(int(avg['avgPeople']) / int(avg['movieDay']), 2)
        elif int(avg['movieDay']) >= 9:
            avg['avgPrice'] = round(int(avg['avgPrice']) / 8, 2)
            avg['avgPeople'] = round(int(avg['avgPeople']) / 8, 2)
        print(avg)
    return movieAvgList

def avgMovieBoxOffice():
    dailyMovieBoxOfficeList = []
    for i in range(-8, 0):
        dailyMovieBoxOfficeList.append(crawDailyBoxOffice(i))
    return getMovieAvg(dailyMovieBoxOfficeList)

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
    except Exception as e:
        print('Error when request url=', url)
        print(e)
        return None
    movieBoxOfficeList = json.loads(json_data)['data1']  #将json网页数据通过json库转换为list
    for movieBoxOfficeDict in movieBoxOfficeList:
        movieBoxOfficeDict['Date'] = MovieUtils.str2date(current_Date.strftime('%Y-%m-%d'))  #在每日的票房Dict中添加日期
        del movieBoxOfficeDict['MovieImg']   #删除Dict中的无效键值
        movieBoxOfficeDict['BoxOffice'] = 10000 * int(movieBoxOfficeDict['BoxOffice'])   #票房数值单位转换
        # print(movieBoxOfficeDict)
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
                #print(da)
            if newestData < int(da[1]):
                newestData = int(da[1])
        if flashMovieBoxOfficeList:
            for boxOfficeInDatabase in flashMovieBoxOfficeList:
                flashBoxOfficeInDataBase(boxOfficeInDatabase)       #更新字典里面的票房数据
        currentDate = MovieUtils.str2date(datetime.now().strftime('%Y-%m-%d'))
        return (newestData - int(currentDate))  #如果db中的movie_boxoffice已有数据则返回db中的最新日期和当前日期的差值
    else:
        return data1   #如果服务器中没有数据则返回空

def crawMovieScene(i):
    url = 'http://www.cbooo.cn/Screen/getScreenData?days=' + str(i)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }  # headers这一段不需要改动
    text = ''
    try:
        print('Requesting url: ', url)
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None

    current_Date = datetime.now() + timedelta(days=i)
    print(current_Date.strftime('%Y-%m-%d'))
    test_json = json.loads(text)
    cityMovieData = test_json['data2']

    for city in cityMovieData:
        for id in test_json['data3']:
            if city['cityname'] == id['name']:
                city['cityid'] = id['id']
        city['date'] = MovieUtils.str2date(current_Date.strftime('%Y-%m-%d'))
    return cityMovieData

def getCrawedMovieSceneDate():
    cursor.execute("select * from movie_scene")
    movieSceneTuple = cursor.fetchall()
    print(movieSceneTuple)
    if movieSceneTuple :
        leastDate = int(movieSceneTuple[0][2])
        for da in movieSceneTuple:
            if int(da[2]) > leastDate:
                leastDate = int(da[2])
        print(len(movieSceneTuple))
        currentDate = MovieUtils.str2date(datetime.now().strftime('%Y-%m-%d'))
        return (leastDate - int(currentDate))
    else:
        return movieSceneTuple

def getMovieSceneDate():
    cursor.execute("select * from movie_scene")
    movieSceneTuple = cursor.fetchall()
    return movieSceneTuple

def saveMovieSceneInDatabase(cityMovieSceneDataDict):
    print('Saving movie scene # ', cityMovieSceneDataDict['date'],
          cityMovieSceneDataDict['cityname'], cityMovieSceneDataDict['cnName'], ' into data base...')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')  # 关闭外键检测
    conn.commit()
    try:
        cursor.execute(
            'replace into movie_scene'
            '(MovieID, CityName, Date, Scene)'
            'values (%s, %s, %s, %s)',
            [cityMovieSceneDataDict['movieid'], cityMovieSceneDataDict['cityname'],
             cityMovieSceneDataDict['date'], cityMovieSceneDataDict['citynum']]
        )
        conn.commit()
    except Exception as e:
        print('Error in saveMovieInDatabase Step 1.')
        print(e)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')  # 重新开启外键检测
    conn.commit()

def flushMovieSceneInDatabase(cityMovieSceneDataDict):
    print('Flushing movie scene # ', cityMovieSceneDataDict['date'],
          cityMovieSceneDataDict['cityname'], cityMovieSceneDataDict['movieid'], ' into data base...')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')  # 关闭外键检测
    conn.commit()
    try:
        cursor.execute(
            'replace into movie_scene'
            '(MovieID, CityName, Date, Scene)'
            'values (%s, %s, %s, %s)',
            [cityMovieSceneDataDict['movieid'], cityMovieSceneDataDict['cityname'],
             cityMovieSceneDataDict['date'], cityMovieSceneDataDict['citynum']]
        )
        conn.commit()
    except Exception as e:
        print('Error in saveMovieInDatabase Step 1.')
        print(e)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')  # 重新开启外键检测
    conn.commit()

def flushMovieSceneData(cityMovieSceneDataList):
    movieSceneTuple = getMovieSceneDate()
    flushCityDataInMovieSceneList = []
    for sceneTuple in movieSceneTuple:
        flushMovieSceneDict = {'movieid': None,
                               'cityname': None,
                               'cityid': None,
                               'date': None,
                               'citynum': None}
        flag = 0
        for cityMovieSceneDailyDataList in cityMovieSceneDataList:
            # print(len(cityMovieSceneDailyDataList))
            for cityMovieSceneDataDict in cityMovieSceneDailyDataList:
                flag = 1
                if sceneTuple[1] == cityMovieSceneDataDict['cityid']:
                    flushMovieSceneDict['movieid'] = sceneTuple[0]
                    flushMovieSceneDict['cityname'] = cityMovieSceneDataDict['cityname']
                    flushMovieSceneDict['cityid'] = sceneTuple[1]
                    flushMovieSceneDict['date'] = sceneTuple[2]
                    flushMovieSceneDict['citynum'] = sceneTuple[3]
                    flushCityDataInMovieSceneList.append(flushMovieSceneDict)
                    break
            if flag == 1:
                break
    for sceneDict in flushCityDataInMovieSceneList:
        print(sceneDict)
        flushMovieSceneInDatabase(sceneDict)

def excute():
    # get movie IDs
    movieIDList = crawCurrentMovie()  # 返回的是一个影片ID的字典
    # get movie data
    movieDataList = []
    for movieID in movieIDList:
        movieDataList.append(crawMovie(movieID))  # append得到的是影片的数据
    movieAvgList = avgMovieBoxOffice()
    # save movie data into data base
    for movieData in movieDataList:
        for avg in movieAvgList:
            if avg['womIndex'] == '':
                avg['womIndex'] = None
            if movieData['id'] == avg['id']:
                movieData['AvgPrice'] = avg['avgPrice']
                movieData['AvgPeople'] = avg['avgPeople']
                movieData['WomIndex'] = avg['womIndex']
    for movieData in movieDataList:
        saveMovieInDatabase(movieData)
    # get Movie Box Office
    dailyMovieBoxOfficeList = []
    newestDay = getMovieBoxOfficeNewestDateInDatabase()
    print(newestDay)
    if newestDay:
        if newestDay <= -8:
            for i in range(-8, 1):
                dailyMovieBoxOfficeList.append(crawDailyBoxOffice(i))
        else:
            for i in range(newestDay, 1):
                dailyMovieBoxOfficeList.append(crawDailyBoxOffice(i))
    elif newestDay == 0:
        dailyMovieBoxOfficeList.append(crawDailyBoxOffice(0))
    else:
        for i in range(-8, 1):
                dailyMovieBoxOfficeList.append(crawDailyBoxOffice(i))
    for dailyBoxOffice in dailyMovieBoxOfficeList:
        for boxOffice in dailyBoxOffice:
            saveBoxOfficeInDataBase(boxOffice)
    #getMovieScene
    crawedDays = getCrawedMovieSceneDate()#获取服务器上所存数据的最新日期
    cityMovieSceneDataList = []
    if crawedDays:
        if crawedDays >= 2:
            cityMovieSceneDataList.append(crawMovieScene(2))
        elif crawedDays <= 0:
            for i in range(0, 3):
                cityMovieSceneDataList.append(crawMovieScene(i))
        else:
            for i in range(crawedDays, 3):
                cityMovieSceneDataList.append(crawMovieScene(i))
    else:
        for i in range(0, 3):
            cityMovieSceneDataList.append(crawMovieScene(i))
    # 将数据库里面原有的cityid，改为cityname
    flushMovieSceneData(cityMovieSceneDataList)
    for cityMovieSceneDailyDataList in cityMovieSceneDataList:
        #print(len(cityMovieSceneDailyDataList))
        for cityMovieSceneDataDict in cityMovieSceneDailyDataList:
            # print(cityMovieSceneDataDict)
            saveMovieSceneInDatabase(cityMovieSceneDataDict)

def main():
    excute()
    cursor.close()
    conn.close()
    return

if __name__ == '__main__':
    main()
