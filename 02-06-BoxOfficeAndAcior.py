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
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
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
        text = requests.get(url,headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=',url)
        return None

    soup = BeautifulSoup(text,'lxml')
    odd = soup.find_all('tr',class_='odd')
    even = soup.find_all('tr',class_='even')
    # for element in odd:
    #     odd_img = element.find('img').get('src')
    #     print(odd_img)
    for element in even:
        even_img = element.find('img').get('src')
        if even_img is None:
            pass
        else:
            print(even_img)
    pass
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
    print('Favorite Actor ...:')
    soup = BeautifulSoup(text, "lxml")
    taxi = soup.find('div', class_='cont')
    for taxi in taxi.stripped_strings:
        print(taxi.replace('\r','').replace('\n','').replace(' ', ''))
    pass
    print('\n已发布作品：')
    cars = soup.find('ul',id='ulperm',class_='ulzx ulzx01').find_all('li')
    for element in cars:
        bike = element.find('a')
        for element in bike.stripped_strings:
            print(element)

def crawActorID():
    pass



def main():
   crawCurrentMovie()
   pictureofMovie()
   ActorsOfMovies()
   return None

if __name__ == '__main__':
    main()