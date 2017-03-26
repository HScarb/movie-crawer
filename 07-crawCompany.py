import MovieUtils
import requests
from bs4 import BeautifulSoup
import mysql.connector

DEFAULT_TIMEOUT = 10
conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()

def crawCompany(companyID):
    '''
        根据公司的ID，爬取公司的信息
        包括 名称，所属国家
        :param companyID:
        :return:
        '''
    url = 'http://www.cbooo.cn/c/' + str(companyID)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    #爬取CompanyID,CName,EName,Nation
    #CompanyID信息在movie_company里面
    text = ''
    companyDataDict = {     'CompanyID':companyID,
                            'CName':None,
                            'EName':None,
                            'Nation':None}
    print('Crawing company info: ', url)
    #抓取整个网页
    try:
        text = requests.get(url, headers = headers, timeout = DEFAULT_TIMEOUT).text
    except:
        print('Error when request url = ',url)
        return None
    soup = BeautifulSoup(text,'lxml')
    apples = soup.find('div',class_='cont')
    i = 0
    try:
        for apple in apples.stripped_strings:
            #print(apple)        #属性是第一个是CName，第二个是Nation，第三个是EMame
            if i == 0:
                companyDataDict['CName'] = apple
            elif i == 1:
                companyDataDict['Nation'] = apple
            elif i == 2:
                companyDataDict['EName'] = apple
            i = i + 1
        i = 0
    except Exception as a:
        print('Error in CRAWING #' + str(companyID) ,'into data base')
    pass
    return companyDataDict

def saveCompanyDatabase(companyDataDict):
    print('Saving company # ', companyDataDict['CompanyID'],'into data base')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')     #关闭外键检测
    conn.commit()
    try:
        cursor.execute(
                'replace into company'
                '(CompanyID,CName,EName,Nation)'
                'value(%s, %s, %s, %s)',
                [companyDataDict['CompanyID'],companyDataDict['CName'],companyDataDict['EName'],companyDataDict['Nation']]
        )
        conn.commit()
    except Exception as b:
        print('Error in saveCompanyDatabase: ', b)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')  #重新开启外键检测
    conn.commit()

def main():
    #crawCompany(6)
    cursor.execute('select CompanyID from movie.movie_company')
    val = cursor.fetchall()
    for element in val:
        for value in element:
            saveCompanyDatabase(crawCompany(value))
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()