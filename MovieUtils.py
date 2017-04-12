import re
import subprocess           # for jar
from urllib import request
# try:
#     import Image
# except ImportError:
#     from PIL import Image
# import pytesseract
DBCONFIG = {
    'host': '106.14.26.144',
    'user': 'movie',
    'password': 'movie',
    'port':3306,
    'database': 'movie',
    'charset': 'utf8'
}

# 要爬的一线、二线城市
CRAWING_CITIES = [
    290,    # beijing
    292,    # shanghai
    365,    # guangzhou
    880,    # chengdu
    974,    # hangzhou
    293,    # tianjin
    628,    # nanjing
    291,    # chongqing
    561,    # wuhan
    791,    # xian
    805,    # jibnan
    829,    # qingdao
    991,    # ningbo
    323,    # xiamen
    729,    # dalian
    528,    # haerbin
    722,    # shenyang
    693,    # changchun
    598,    # changsha
    328,    # fuzhou
    489,    # zhengzhou
    453,    # shijiazhuang
    1332,   # suzhou
    373,    # foshan
    843,    # yantai
    371,    # dongguan
    854,    # taiyuan
    662,    # wuxi
    295,    # hefei
    674,    # nanchang
    411,    # nanning
    950,    # kunming
    1001,   # wenzhou
    851,    # zibo
    480,    # tangshan
]

def str2date(str):
    '''
    将 yyyy-m-d 的字符串转换成 yyyymmdd
    比如将 2017-3-3 转换成 20170303
    :param str: 待转换字符串
    :return: 转换好的字符串
    '''
    try:
        r = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})', str)
        text = r.group(1)
    except Exception as e:
        print('Error when excute MovieUtil !' )
        print(e)
        return None
    for i in [2, 3]:
        if r.group(i).__len__() == 1:
            text = text + '0' + r.group(i)
        else:
            text = text + r.group(i)
    return text

def downloadImg(url, filename):
    '''
    从一个url下载图片
    :param url:
    :param filename: 要下载的图片名称
    :return: 无
    '''
    header = {
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    request.urlretrieve(url, filename)

def parseImg(imgPath):
    '''
    从图片解析数字，返回一个字符串
    :param imgPath: 图片在本地的地址
    :return: 一个字符串，存储图片中的数字
    '''
    result = None
    try:
        result = subprocess.check_output("java -jar ImageRecognize.jar " + imgPath, shell=True).splitlines()[0].decode('gb2312')
    except Exception as e:
        print('Parse image error: ', e)
        result = None
    return result

def main():
    print(str2date('2017-3-3'))
    print(str2date('2017-3-13'))
    print(str2date('2017-03-3'))

    #downloadImg('http://img.58921.com/sites/all/movie/files/protec/56153c5cd7384803a2f16bfcd7bd720d.png', 'Img1.png')   # 60506
    #downloadImg('http://img.58921.com/sites/all/movie/files/protec/1821c285e91bc945269941b32f5e0fe5.png', 'Img2.png')   # 30934

    print(parseImg('Img4.png'))
    print(parseImg('Img5.png'))

if __name__ == '__main__':
    main()