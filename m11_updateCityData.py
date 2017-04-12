import mysql.connector
import MovieUtils

conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()

def flashCityMsg(flashDict):
    print("flash city message #", flashDict['id'], flashDict['stringid'], "into database")
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    conn.commit()
    try:
        cursor.execute('replace into city'
                           '(DistrictID, CityID, StringID, CName, EName)'
                           'values (%s, %s, %s, %s, %s)',
                           [flashDict['id'], flashDict['parentid'], flashDict['stringid'], flashDict['cname'], flashDict['ename']])
    except Exception as e:
        print("Error in flash city msg")
        print(e)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')
    conn.commit()


def main():
    flashList = []
    flashList2 = []
    cursor.execute("select * from city")
    data = cursor.fetchall()
    for da in data:
        #print(da)
        flashDict = {'id': None,
                     'stringid': None}
        flashDict2 = {'id': None,
                      'parentid' : None,
                     'stringid': None,
                      'cname': None,
                      'ename': None}
        if da[4] == None:
            # print(da[2].split('_'))
            str = ''
            for i in range(0, len(da[2].split('_')) - 1):
                str = str + da[2].split('_')[i] + '_'
            # print(str.rstrip('_'))
            flashDict['id'] = da[1]
            flashDict['stringid'] = str.rstrip('_')
            flashList.append(flashDict)
        if da[4]:
            flashDict2['id'] = da[0]
            flashDict2['parentid'] = da[1]
            flashDict2['stringid'] = da[2]
            flashDict2['cname'] = da[3]
            flashDict2['ename'] = da[4]
            flashList2.append(flashDict2)
    for fla in flashList2:
        for fl in flashList:
            if fl['id'] == fla['id']:
                fla['stringid'] = fl['stringid']
    for flashDict in flashList2:
        flashCityMsg(flashDict)
    cursor.close()
    conn.close()
if __name__ == '__main__':
    main()