import json
import MovieUtils
import mysql.connector

conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()

def readData(dataFileName = 'cinemadata.txt'):
    f = open(dataFileName, 'r', encoding='utf-8')
    data = f.read()
    f.close()
    return data

def pretifyDataAndSave(data):
    '''
    将data美化并且存为json文件
    :param data: python object, 这里为dict
    '''
    with open('cinemadata.json', 'w', encoding='utf-8') as fout:
        fout.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))     # ensure_ascii=False: 将unicode转中文

def parseData(data):
    '''

    :param data:
    :return: 两个list 分别是city_list和cinema_list
    '''
    city_list = []
    cinema_list = []
    data = data['locations']['List']
    for districts in data:
        city = {
            'cityid': None,
            'parentid' : 0,
            'stringid' : None,
            'ename' : None,
            'cname' : None
        }
        city['cityid'] = districts['Id']
        city['parentid'] = districts['Id']
        city['cname'] = districts['NameCn']
        city['ename'] = districts['NameEn']
        city['stringid'] = districts['NameEn']
        city_list.append(city)

        for cinema in districts['Cinemas']['List']:
            cinema_list.append(cinema)

        if 'Districts' in districts:
            for district in districts['Districts']['List']:
                print(district)
                city = {
                    'cityid': None,
                    'parentid' : 0,
                    'stringid' : None,
                    'ename' : None,
                    'cname' : None
                }
                city['cityid'] = district['Id']
                city['parentid'] = district['ParentId']
                city['stringid'] = district['StringId']
                city['cname'] = district['NameCn']
                city_list.append(city)

                for cinema in district['Cinemas']['List']:
                    cinema_list.append(cinema)
    return city_list, cinema_list

def saveCinemaInDataBase(cinema_list):
    '''
    cinema : {
        'CityId'
        'DistrictId'
        'Id'
        'NameCn'
    }
    :param cinema_list: list of cinema
    :return:
    '''
    print('Saving cinemas into database...')

    cursor.execute('SET FOREIGN_KEY_CHECKS=0')
    conn.commit()

    for cinema in cinema_list:
        try:
            print('Saveing cinema # ', cinema['Id'])
            cursor.execute('replace into c'
                           '(CinemaID, CityID, DistrictID, Name)'
                           'values (%s, %s, %s, %s)',
                           [cinema['Id'], cinema['CityId'], cinema['DistrictId'], cinema['NameCn']])
        except Exception as e:
            print('Error when saving cinema data...')
            print(e)

    cursor.execute('SET FOREIGN_KEY_CHECKS=1')      # 重新开启外键检测
    conn.commit()

def saveCityInDataBase(city_list):
    '''
    city : {
        'cityid'
        'cname'
        'ename'
        'parentid'
        'stringid'
    }
    :param city_list: list of city
    :return:
    '''
    print('Saving cities into database...')

    cursor.execute('SET FOREIGN_KEY_CHECKS=0')
    conn.commit()

    for city in city_list:
        try:
            print('Saveing city # ', city['cityid'])
            cursor.execute('replace into city'
                           '(CityID, ParentID, StringID, CName, EName)'
                           'values (%s, %s, %s, %s, %s)',
                           [city['cityid'], city['parentid'], city['stringid'], city['cname'], city['ename']])
        except Exception as e:
            print('Error when saving city data...')
            print(e)

    cursor.execute('SET FOREIGN_KEY_CHECKS=1')      # 重新开启外键检测
    conn.commit()

def main():
    data = json.loads(readData())
    #pretifyDataAndSave(data)
    # 解析、处理data
    city_list, cinema_list = parseData(data)
    #saveCinemaInDataBase(cinema_list)
    saveCityInDataBase(city_list)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
    