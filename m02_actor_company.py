import MovieUtils
import requests
from bs4 import BeautifulSoup
import mysql.connector

DEFAULT_TIMEOUT = 10
conn = mysql.connector.connect(**MovieUtils.DBCONFIG)
cursor = conn.cursor()

def diff(listA,listB):
    retC = list(set(listB).difference(set(listA)))
    return retC

def crawActor(actorID):
    '''
        根据演员的ID,爬取演员信息
        包括 名称,已发布作品,未发布作品
        :param actorID:
        :return:
        '''
    url = 'http://www.cbooo.cn/p/' + str(actorID)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    text = ''
    actorDataDict = {  'ActorID':actorID,
                       'CName':None,
                       'EName':None,
                       'Nation':None,
                       'IsLoad':None}
    print('Crawing actor info: ',url)
    #抓取整个网页
    try:
        text = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT).text
    except:
        print('Error when request url=', url)
        return None
    soup = BeautifulSoup(text, "lxml")
    taxi = soup.find('div', class_='cont')
    i = 0
    try:
        for element in taxi.stripped_strings:
            actorDataDict['IsLoad'] = True
            if i == 0:
                actorDataDict['CName'] = element
            elif i == 1:
                actorDataDict['EName'] = element
            elif element[0] == '国':
                actorDataDict['Nation'] = element[3:]
            elif element[0] == '生':
                pass
            i = i + 1
        i = 0
    except Exception as e:
        print('Error in CRAWING # ' + str(actorID) ,'into data base: ' + e)
    pass
    return actorDataDict

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
            if i == 0:
                companyDataDict['CName'] = apple
            elif i == 1:
                companyDataDict['Nation'] = apple
            elif i == 2:
                companyDataDict['EName'] = apple
            i = i + 1
        i = 0
    except Exception as a:
        print('Error in CRAWING #' + str(companyID) ,'into data base', + a)
    pass
    return companyDataDict

def saveActorInDatabase(actorDataDict):
    print('Saving actor # ', actorDataDict['ActorID'],'into data base...')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')  # 关闭外键检测
    conn.commit()
    try:
        cursor.execute(
            'replace into actor'
            '(ActorID, ActorCName, ActorEName, ActorNation)'
            'values(%s, %s, %s, %s)',
            [actorDataDict['ActorID'],actorDataDict['CName'],actorDataDict['EName'],actorDataDict['Nation']]
        )
        conn.commit()
    except Exception as e:
        print('Error in saveActorInDatabase: ', e)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')  # 重新开启外键检测
    conn.commit()

def saveCompanyDatabase(companyDataDict):
    print('Saving company # ', companyDataDict['CompanyID'],'into data base')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')     #关闭外键检测
    conn.commit()
    try:
        cursor.execute(
                'replace into company'
                '(CompanyID,CompanyCName,CompanyEName,CompanyNation)'
                'value(%s, %s, %s, %s)',
                [companyDataDict['CompanyID'],companyDataDict['CName'],companyDataDict['EName'],companyDataDict['Nation']]
        )
        conn.commit()
    except Exception as b:
        print('Error in saveCompanyDatabase: ', + b)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')  #重新开启外键检测
    conn.commit()

def main():
    cursor.execute('select ActorID from movie_actor')
    val_movie_actor = cursor.fetchall()
    cursor.execute('select ActorID from actor')
    val_actor = cursor.fetchall()
    val_DiffenectAct_list = diff(val_actor,val_movie_actor)
    for tuple in val_DiffenectAct_list:
        saveActorInDatabase(crawActor(tuple[0]))
    pass

    cursor.execute('select CompanyID from movie_company')
    val_movie_company = cursor.fetchall()
    cursor.execute('select CompanyID from company')
    val_company = cursor.fetchall()
    val_DiffenectCom_list = diff(val_movie_company, val_company)
    for tuple in val_DiffenectCom_list:
        saveActorInDatabase(crawCompany(tuple[0]))
    pass

    print('Finish actors and companys!!')
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()