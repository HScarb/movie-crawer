import re
from urllib import request
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract


def str2date(str):
    '''
    将 yyyy-m-d 的字符串转换成 yyyymmdd
    比如将 2017-3-3 转换成 20170303
    :param str: 待转换字符串
    :return: 转换好的字符串
    '''
    r = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})', str)
    text = r.group(1)
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
    return pytesseract.image_to_string(Image.open(imgPath))
    pytesseract.image_to_string(Image.open())

def main():
    print(str2date('2017-3-3'))
    print(str2date('2017-3-13'))
    print(str2date('2017-03-3'))

    downloadImg('http://img.58921.com/sites/all/movie/files/protec/56153c5cd7384803a2f16bfcd7bd720d.png', 'Img1.png')   # 60506
    downloadImg('http://img.58921.com/sites/all/movie/files/protec/1821c285e91bc945269941b32f5e0fe5.png', 'Img2.png')   # 30934

    #print(parseImg('Img1.png'))
    #print(parseImg('Img2.png'))

if __name__ == '__main__':
    main()