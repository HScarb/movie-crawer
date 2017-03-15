import requests
import re
import random
from urllib.request import urlopen
from time import sleep
from bs4 import BeautifulSoup

DEFAULT_TIMEOUT = 10

def crawCurrentMovie():
    url = 'http://58921.com/schedule/date/20170306'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    text = ''
    box_office_dataList = {}
    print('Crawing current movie...: ')
    try:
        print('Requesting url: ',url)
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=',url)
        return None
    #############################################################################################
    soup = BeautifulSoup(text,"lxml")
    results = soup.find('div',class_='table-responsive')
    for result in results.stripped_strings:
       print(result)
    pass


def pictureofMovie():
    url = 'http://58921.com/schedule/date/20170307'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    text = ''
    print('Now crawName...:')
    try:
        print('Request url: ',url)
        text = requests.get(url,headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=',url)
        return None
    ##############################################################################################
    soup = BeautifulSoup(text,'lxml')
    all_o = soup.find_all('tr',class_='odd')
    all_e = soup.find_all('tr',class_='even')
    for o in all_o:
        print(o)
        #print(o.a)                 #a是地方名，img是票房数据图片
    #for o in all_o:
        #print(o.img)
    print('***********************************************************************************')  #分不清楚谁是谁

    for e in all_e:
        print(e)

def ActorsOfMovies():
    url = 'http://www.cbooo.cn/p/1893'      #周杰伦
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    text = ''
    try:
        text = requests.get(url, headers=headers).text
    except:
        print('Error when request url=', url)
        return None
    print('Favorite Actor ...:')
    soup = BeautifulSoup(text, "lxml")
    taxi = soup.find('div', class_='cont')
    for taxi in taxi.stripped_strings:
        print(taxi.replace('\r','').replace('\n','').replace(' ', ''))
    print('\n已发布作品：')
    cars = soup.find('div',class_='mainbox fr').find_all('li')
    for car in cars:
        #print(car.replace('\r','').replace('\n','').replace(' ', ''))
        print(car.get_text())

        #1soup.find_all(href=re.compile(“elsie”))
# [<a class=”sister” href=”http://example.com/elsie” id=”link1″>Elsie</a>]



def main():
   crawCurrentMovie()
   pictureofMovie()
   ActorsOfMovies()
   return None

if __name__ == '__main__':
    main()