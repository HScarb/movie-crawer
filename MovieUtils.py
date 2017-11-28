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
    290,    # beijing北京
    292,    # shanghai上海
    365,    # guangzhou广州
    880,    # chengdu成都
    974,    # hangzhou杭州
    293,    # tianjin天津
    628,    # nanjing南京
    291,    # chongqing重庆
    561,    # wuhan武汉
    791,    # xian西安
    805,    # jinan济南
    829,    # qingdao青岛
    991,    # ningbo宁波
    323,    # xiamen厦门
    729,    # dalian大连
    528,    # haerbin哈尔滨
    722,    # shenyang沈阳
    693,    # changchun长春
    598,    # changsha长沙
    328,    # fuzhou福州
    489,    # zhengzhou郑州
    453,    # shijiazhuang石家庄
    1332,   # suzhou苏州
    373,    # foshan佛山
    843,    # yantai烟台
    371,    # dongguan东莞
    854,    # taiyuan太原
    662,    # wuxi无锡
    295,    # hefei合肥
    674,    # nanchang南昌
    411,    # nanning南宁
    950,    # kunming昆明
    1001,   # wenzhou温州
    851,    # zibo淄博
    480,    # tangshan唐山
    # 三线城市
    926,    # 
    433,    # 
    450,    # 
    347,    # 
    777,    # 
    785,    # 
    753,    # 
    338,    # 
    756,    # 
    649,    # 
    533,    # 
    664,    # 
    839,    # 
    630,    # 
    759,    # 
    997,    # 
    818,    # 
    665,    # 
    1983,   # 
    1687,   # 
    503,    # 
    809,    # 
    667,    # 
    1355,   # 
    981,    # 
    458,    # 
    1763,   # 
    657,    # 
    671,    # 
    645,    # 
    2463,   # 
    670,    # 
    1003,   #
    984,    #
    455,    # 
    703,    # 
    724,    # 
    837,    # 
    590,    # 
    586,    # 
    1529,   # 
    379,    # 
    505,    # 
    840,    # 
    808,    # 
    623,    # 
    823,    # 
    600,    # 
    345,    # 
    1342,   # 
    389,    # 
    636,    # 
    380,    # 
    2613,   # 
    407,    # 
    470,    # 
    813,    # 
    425,    # 
    793,    # 
    368,    # 
    901,    # 
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