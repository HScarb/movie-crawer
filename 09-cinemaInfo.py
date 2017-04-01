import mysql.connector
import requests
import lxml
from bs4 import BeautifulSoup
import MovieUtils
import json

DEFAUT_TIME = 10

conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()
def crawlCityCinema(cityCinemaDict):
    url = 'http://theater.mtime.com/' + cityCinemaDict['stringid'] + '/' + str(cityCinemaDict['cinemaid']) + '/info.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    text = ''
    print("Crawling city cinema ...")
    try:
        print('Requesting url=', url)
        text = requests.get(url, headers=headers, timeout=DEFAUT_TIME).text
    except Exception as e:
        print(e)
        print('Error when request url=', url)
        return cityCinemaDict
    try:
        soup = BeautifulSoup(text, "lxml")
        cinemaInner = soup.find('table', class_='lovetable').find_all('b')
        cinemacinemaPhoneTimeAdd = soup.find('div', class_='ci_title').find_all('p')
        cimenaRequept = soup.find('div', class_='ci_mon').find_all('dd')
    except Exception as e:
        print(e)
        return cityCinemaDict

    try:
        if (soup.find('table', class_='lovetable').find_all('p'))[0].get_text()[-2:] == '座位':
            cityCinemaDict['hallsum'] = None
        else:
            cityCinemaDict['hallsum'] = cinemaInner[0].get_text().split()[0]
    except Exception as e:
        print('hallsum', e)
        cityCinemaDict['hallsum'] = None
    try:
        if (soup.find('table', class_='lovetable').find_all('p'))[0].get_text()[-2:] == '座位':
            cityCinemaDict['sitsum'] = cinemaInner[0].get_text().split()[0]
        else:
            cityCinemaDict['sitsum'] = cinemaInner[1].get_text().split()[0]
    except Exception as e:
        print('sitsum', e)
        cityCinemaDict['sitsum'] = None
    try:
        cityCinemaDict['address'] = cinemacinemaPhoneTimeAdd[0].get_text().split()[1]
    except Exception as e:
        print('address', e)
        cityCinemaDict['address'] = None
    try:
        if cinemacinemaPhoneTimeAdd[1].get_text().split()[0].split('：', 1)[0] == '营业时间':
            cityCinemaDict['tel'] = None
        else:
            cityCinemaDict['tel'] = cinemacinemaPhoneTimeAdd[1].get_text().split()[0].split('：', 1)[1]
    except Exception as e:
        print('tel', e)
        cityCinemaDict['tel'] = None
    try:
        if len(cinemacinemaPhoneTimeAdd[1].get_text().split()[1].split('：',1)[1]) <= 50:
            cityCinemaDict['businesshour'] = cinemacinemaPhoneTimeAdd[1].get_text().split()[1].split('：',1)[1]
        else:
            cityCinemaDict['businesshour'] = cinemacinemaPhoneTimeAdd[1].get_text().split()[1].split('：', 1)[1][:50]
        if cinemacinemaPhoneTimeAdd[1].get_text().split()[0].split('：', 1)[0] == '营业时间':
            cityCinemaDict['businesshour'] = cinemacinemaPhoneTimeAdd[1].get_text().split()[0].split('：', 1)[1]
    except Exception as e:
        print('businesshour', e)
        cityCinemaDict['businesshour'] = None
    print(cityCinemaDict)
    return cityCinemaDict
    #print(soup)
def saveCinemainfoIntoDatabase(cityCinemaDict):
    print('save cinema # ', cityCinemaDict['name'],'into db')
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    conn.commit()
    try:
        cursor.execute('replace into cinema'
                           '(CinemaID, CityID, DistrictID, Name, HallSum, SitSum, Address, Tel, BusinessHour)'
                           'values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           [cityCinemaDict['cinemaid'], cityCinemaDict['cityid'], cityCinemaDict['districtid'],
                            cityCinemaDict['name'], cityCinemaDict['hallsum'], cityCinemaDict['sitsum'],
                            cityCinemaDict['address'], cityCinemaDict['tel'], cityCinemaDict['businesshour']])
    except Exception as e:
        print(e)
        return None
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')
    conn.commit()
def runCrawlCinemaInfo():
    cursor.execute('select * from city')
    cityDataList = cursor.fetchall()
    cursor.execute('select * from cinema')
    cinemaDataList = cursor.fetchall()
    cityCinemaList = []
    crawlCinemaList = []
    for cityData in cityDataList:
        for cinemaData in cinemaDataList:
            cityCinemaDict = {'cinemaid': None,
                              'stringid': None,
                              'cityid': None,
                              'districtid': None,
                              'name': None,
                              'hallsum': None,
                              'sitsum': None,
                              'address': None,
                              'tel': None,
                              'businesshour':None}
            if cityData[0] == cinemaData[2] or (cinemaData[2] == 0 and cityData[0] == cinemaData[1]):
                cityCinemaDict['stringid'] = cityData[2]
                cityCinemaDict['cinemaid'] = cinemaData[0]
                cityCinemaDict['cityid'] = cinemaData[1]
                cityCinemaDict['districtid'] = cinemaData[2]
                cityCinemaDict['name'] = cinemaData[3]
                if cinemaData[4]:
                    cityCinemaDict['hallsum'] = cinemaData[4]
                else:
                    cityCinemaDict['hallsum'] = None
                if cinemaData[5]:
                    cityCinemaDict['sitsum'] = cinemaData[5]
                else:
                    cityCinemaDict['sitsum'] = None
                if cinemaData[6]:
                    cityCinemaDict['address'] = cinemaData[6]
                else:
                    cityCinemaDict['address'] = None
                if cinemaData[7]:
                    cityCinemaDict['tel'] = cinemaData[7]
                else:
                    cityCinemaDict['tel'] = None
                if cinemaData[8]:
                    cityCinemaDict['businesshour'] = cinemaData[8]
                else:
                    cityCinemaDict['businesshour'] = None
                cityCinemaList.append(cityCinemaDict)

    for cityCinemaDict in cityCinemaList:
        if (cityCinemaDict['hallsum'] == None
            and cityCinemaDict['sitsum'] == None
            and cityCinemaDict['address'] == None
            and cityCinemaDict['tel'] == None
            and cityCinemaDict['businesshour'] == None):
            saveCinemainfoIntoDatabase(crawlCityCinema(cityCinemaDict))
        #saveCinemainfoIntoDatabase(crawlCityCinema(cityCinemaDict))
def main():
    runCrawlCinemaInfo()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()