import re

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

def main():
    print(str2date('2017-3-3'))
    print(str2date('2017-3-13'))
    print(str2date('2017-03-3'))

if __name__ == '__main__':
    main()