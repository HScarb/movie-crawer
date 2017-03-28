import requests
import json
from datetime import datetime, timedelta
import MovieUtils
import mysql.connector

DEFAULT_TIMEOUT = 10                # 默认等待时间
conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()
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
    for ci in cityMovieData:
        print(ci)
    return cityMovieData

def getCrawedMovieSceneDate():
    cursor.execute("select * from movie_scene")
    data1 = cursor.fetchall()
    print(data1)
    if data1 :
        leastDate = int(data1[0][2])
        for da in data1:
            if int(da[2]) > leastDate:
                leastDate = int(da[2])
        print(len(data1))
        currentDate = MovieUtils.str2date(datetime.now().strftime('%Y-%m-%d'))
        return (leastDate - int(currentDate))
    else:
        return data1

def saveMovieSceneInDatabase(cityMovieSceneDataDict):
    print('Saving movie scene # ', cityMovieSceneDataDict['date'],
          cityMovieSceneDataDict['cityname'], cityMovieSceneDataDict['cnName'], ' into data base...')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')  # 关闭外键检测
    conn.commit()
    try:
        cursor.execute(
            'replace into movie_scene'
            '(MovieID, CityId, Date, Scene)'
            'values (%s, %s, %s, %s)',
            [cityMovieSceneDataDict['movieid'], cityMovieSceneDataDict['cityid'],
             cityMovieSceneDataDict['date'], cityMovieSceneDataDict['citynum']]
        )
        conn.commit()
    except Exception as e:
        print('Error in saveMovieInDatabase Step 1.')
        print(e)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')  # 重新开启外键检测
    conn.commit()

def main():
    crawedDays = getCrawedMovieSceneDate()
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
    for cityMovieSceneDailyDataList in cityMovieSceneDataList:
        print(len(cityMovieSceneDailyDataList))
        for cityMovieSceneDataDict in cityMovieSceneDailyDataList:
            #print(cityMovieSceneDataDict)
            saveMovieSceneInDatabase(cityMovieSceneDataDict)


if __name__ == '__main__':
    main()