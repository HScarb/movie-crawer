import requests
import re
import random
import chardet
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
    print('Crawing current movie...: ')
    try:
        print('Requesting url: ',url)
        text = requests.get(url, headers=headers).text
    except:
        print('Error when request url=',url)
        return None
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
        text = requests.get(url,headers=headers).text
    except:
        print('Error when request url=',url)
        return None

    soup = BeautifulSoup(text,'lxml')
    tab = soup.find('div',class_='table-responsive')        #不是一般的标签，比如table，是找不到的
    odds = tab.find_all('tr',class_='odd')                   #table-responsive的Tag内容中的中文显示乱码
    evens = tab.find_all('tr',class_='even')
    # for odd in odds:
        # odd_city = odd.find('a').get('href')
        # if odd_city is not None:
        #     print(odd_city)
        # odd_img = element.find('img').get('src')
        # print(odd_img)
    # pass

    # for even in evens:
        # even_city = even.find('a').get('href')       #还有一个问题。href最好用table-responsive,而img最好用长的那个
        # print(even_city)
    # pass
        # even_img = element.find('img').get('src')
        # if even_img is None:
        #     pass
        # else:
        #     print(even_img)
    print('***********************************************************************************')  #分不清楚谁是谁

def ActorsOfMovies():
    url = 'http://www.cbooo.cn/p/1893'      #周杰伦
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    text = ''
    try:
        print('Request url: ', url)
        text = requests.get(url, headers=headers,timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    soup = BeautifulSoup(text, "lxml")
    taxi = soup.find('div', class_='cont')
    for taxi in taxi.stripped_strings:
        print(taxi.replace('\r','').replace('\n','').replace(' ', ''))
    pass
    cars = soup.find('div',class_='ziliaofr').find('div',class_='starring')
    for car in cars.stripped_strings:
        print(car)

def crawActorID():
    pass



def main():
   crawCurrentMovie()
   pictureofMovie()
   ActorsOfMovies()
   return None

if __name__ == '__main__':
    main()