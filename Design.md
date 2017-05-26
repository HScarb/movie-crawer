# Movie-Crawler 全国电影、排片信息爬虫集

海量数据第1小组
- 金嘉浩 14051616
- 汪李贤 14208127
- 卢陈侃 14194813
- 徐明湖 14015124
- 褚浩臻 14194813

[TOC]

## 1. 简介
### 1.1 综述
- 基于Python的全国电影、排片信息爬虫集
- 包含信息展示的页面和信息查询后台，部署在阿里云服务器

### 1.2 数据来源
1. 中国票房网(CBO)
2. 时光网(Mtime)
3. 电影票房数据库(58921)

### 1.3 包含爬虫
1. 正在上映电影爬虫(来源:CBO)
    - 正在上映电影信息
    - 正在上映电影的每日票房和排片
2. 影人、公司爬虫(来源:CBO)
    - 影人信息(包含导演和演员)
    - 公司信息(电影制作商、发行商)
3. 电影影院排片爬虫(来源:Mtime)
    - 当天和之后一天的全国所有影院电影排片
    - 有排片的电影信息
4. 电影每日排片爬虫(来源:58921)
    - 正在上映的热门影片的每日拍片信息
5. 全国影院爬虫(来源:Mtime)
    - 全国所有的影院信息
6. 历史电影爬虫(来源:CBO)
    - 之前几年上映过电影和电影信息
7. 历史电影排片爬虫(来源:CBO)
    - 之前几年上映过的电影每日排片数量
8. 城市电影排片数爬虫(58921)
    - 特定城市的电影每日排片数

## 1. 成员分工
- 金嘉浩(组长)
    - 爬虫框架搭建
    - 组员分工统筹
    - 实验报告编写
    - 1.正在上映电影爬虫
    - 3.电影影院拍片爬虫
    - 5.全国影院爬虫
- 汪李贤
    - 展示页面后台编写
    - 4.电影每日排片爬虫
    - 8.城市电影排片数爬虫
    - 数字图片识别工具
- 卢陈侃
    - 实验报告编写
    - 2.影人、公司爬虫
    - 6.历史电影爬虫
    - 7.历史电影排片爬虫
- 徐明湖
    - 实验报告编写
    - 1.正在上映电影爬虫
    - 5.全国影院爬虫
- 褚浩臻
    - 展示页面前端设计
    - 展示页面前端编写

## 2. 开发环境(实用工具)

- Python 3.5
- IDE: JetBrains PyCharm
- Chrome 开发者工具
- Python第三方库:
    - requests
    - BeautifulSoup4
    - pandas

## 3.系统/算法设计
### 3.1 需求分析
- CBO中国票房网 需求:
    - 演员
        - 演员中文名
        - 演员英文名
        - 演员国籍
    - 公司
        - 公司中文名
        - 公司英文名
        - 公司所属国籍
    - 影片
        - 影片中文名
        - 影片英文名	
        - 影片类型
        - 影片放映长度
        - 影片首映日期
        - 影片制式
        - 票房总数
        - 平均票价
        - 平均观影人数
        - 口碑指数
    - 影片票房
        - 票房日期
        - 票房数量
        - 平均观影人数
    - 影片排片
        - 影片放映日期
        - 影片放映日期
        - 影片放映场次数
- Mtimes时光网 需求:
      - 影院
        - 影院名称
        - 影院厅总数
        - 影院座位总数
        - 影院地址
        - 影院联系电话
        - 影院营业时间
    - 城市
        - 地区字符串码
        - 城市中文名
        - 城市英文名
    - 影院-影片
        - 影片上映日期
        - 放映场次
        - 总票房数
        - 总观影人数
    - 时光网影片信息
        - 影片英文名
        - 影片中文名
        - 影片类型
        - 影片片场
        - 导演
        - 年份
    - 时光网放映信息
        - 影厅座位数量
        - 放映厅名称
        - 语言
        - 开始放映时间
        - 结束时间
        - 时光网票价
    - 制式
- 58921电影票房数据库 需求:
    - 影片每日排片 
    - 影片中文名
    - 排片信息日期
    - 排片信息城市名称
    - 排片数

### 3.2  详细设计
>注: 0开头的为每天都要运行的爬虫，1开头的为只需要隔较长一段时间运行一次的爬虫

- 01_current_movie:
    - 获取正在上映的电影的ID号
    - 根据ID获取正在上映电影详细信息
    - 根据获取的json文件获得正在上映影片的每日票房
- 02_actor_company：
    - 根据数据库中已经获取的演员的ID,爬取演员信息
    - 根据数据库中已经获取的公司的ID，爬取公司的信息
- 03_movie_showtime：
    - 根据影院ID和日期，获取该影院该日的拍片情况
    - 根据时光网的movieID，获得电影的中英文名
- 04_movie_schedule:
    - 获取首页热门影片列表
    - 根据获取的热门影片列表来爬取影片排片数据
- 10_cinema：
    - 通过读取的城市信息爬取所有影院名称
- 11_updateCityData：
    - 将城市列表中所有不是以“China_Privince_City”的形式展现的城市，以这种方式展示
- 12_cinemaInfo：
    - 根据m11更新后的城市拼音信息和m10的影院id来获取所有影院详细信息
- 13_history_movie：
    - 以年份、地区为条件获取网站上所有影片
- 14_history_scene：
    - 以月、日、地区信息来获取网站上面所有排片信息
- 15_city_movie_schedule：
    - 通过m04获取的热门影片列表来获取城市列表和电影名称列表
    - 通过获取的城市名称获取城市具体排片日期列表
    - 通过排片日期获取影片在每个城市具体日期的具体片信息

## 4.系统功能
- CBO:
    - 爬取演员信息
 [影人资料库](http://www.cbooo.cn/peoples)
    - 爬取发行和制作影片的公司信息
[影院公司](http://www.cbooo.cn/c/6)
    - 爬取所有的影片
[影片资料库](www.cbooo.cn/movie)
    - 爬取当前正在上映的影片的票房
[票房信息](http://www.cbooo.cn/BoxOffice/GetDayBoxOffice?num=0)
    - 爬取正在上映影片的排片
[排片信息](http://www.cbooo.cn/Screen/getScreenData?days=0)
- MTime:
    - 爬取全国所有影院信息
[影院信息](cinemadata.json)
    - 爬取所有影片信息和放映信息
[时光网影片信息](http://www.mtime.com/)
- 58921:
    - 影片每日排片
[58921](http://58921.com/schedule/)

## 5.实现方法
### 5.1 爬取当前热门影片信息
- **直接爬取网页上的内容：** 选择待爬取的URL，用浏览器查看网页html代码，先使用request库中request.get(url).text函数获得当前URL的text内容，这一步下载URL的内容，转换完毕后。再用BeautifulSoup把text保存为lxml对象，解析需要的内容。如在爬取当前每日的票房榜前十，我们需要获得影片名称（ID号），实时票房，票房占比，累计票房，排片占比和上映天数。

![](_image/1.jpg)
我们首先获得这些影片的ID值，在代码中实现，就如下：
```python
        results = soup.find_all('tr', class_='trtop', onmouseover='ChangeTopR(this.id)')
```
取得了信息之后，要保存这个信息。代码中实现：
```python
    for result in results:
        print(result['id'])
        movieIDList.append(result['id'])
    return movieIDList
```
返回一个List是为了后面更方便的爬取。
再根据这个ID值，爬取电影的信息包括  名称，类型，片长，制式等。存储进Dict中，再转入数据库。

![](_image/2.jpg)
部分Dict和存储代码实现：
```python
    movieDataDict = {'id':movieID,
                     'cname':None,
                     'ename':None,
                     'type':None,
                     'length':None,
                     'releasetime':None,
    ......

    for element in result1.stripped_strings:
        if isSumBoxOffice == True:
            movieDataDict['sumboxoffice'] = int(float(element[0:-1]) * 10000)
            isSumBoxOffice = False
        elif i == 0:
            movieDataDict['cname'] = element
        elif i == 2:
            movieDataDict['ename'] = element
        elif element[0] == '类':
            movieDataDict['type'] = element[3:]
    ......
```
除此之外，我们还爬取了部分影片的票价，观影人数和口碑指数。但是部分数据在服务器上未记录，所以未能获得所有数据。这部分内容是通过网页的json内容爬取。如下：

![](./_image/2017-05-25-00-00-44.jpg)


![](./_image/2017-05-24-23-58-31.jpg)
代码实现如下：
```python
    movieBoxOfficeList = json.loads(json_data)['data1']  #将json网页数据通过json库转换为list
    for movieBoxOfficeDict in movieBoxOfficeList:
        movieBoxOfficeDict['Date'] = MovieUtils.str2date(current_Date.strftime('%Y-%m-%d'))  #在每日的票房Dict中添加日期
        del movieBoxOfficeDict['MovieImg']   #删除Dict中的无效键值
        movieBoxOfficeDict['BoxOffice'] = 10000 * int(movieBoxOfficeDict['BoxOffice'])   #票房数值单位转换
    return movieBoxOfficeList
```
### 5.2 爬取影片的参演人员信息
**直接寻找html上的element信息：**跟爬取热门影片时类似，我们所需要的演员等的信息包括演员ID号，演员的中文名，英文名，国籍和所属公司。和大概过程如下。

![](./_image/2017-05-25-00-06-58.jpg)
代码中实现为：
```python
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
        ......
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
```
### 5.3 爬取影院信息
**json获取影院信息：**电影院的信息由于短时间内不会发生很大的变化，而全国电影院数量又有点多，于是我们选择把时光网影院信息的json文件下载下来保存到本地进行处理。保存下来的json文件如图：

![](./_image/2017-05-25-00-22-51.jpg)
处理保存这些电影院信息代码如下：
```python
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
```
对于这些影院的更加详细的信息，我们还在时光网上爬取了对应的影院座位数量，营业时间，地址，电话等信息。而这些信息的爬取方式是通过html中的element元素，上面已经有类似的爬取过程，不多展示。
### 5.4 爬取城市区域信息
**根据爬到的城市区域ID号来整理城市信息：**我们要爬取的城市大致分为一线城市和二线城市，如北京，上海，广州，成都等城市的城市号和下辖的县市的信息。
比如我们需要城市的url列表，我们从58921网站爬取这些信息，代码实现如下：
```python
    city_list = re.findall('<a href="(/film/.*?)" .*?>', html_text)
    return city_list, movie_name
```
### 5.5 爬取影院排片情况
**爬取时光网影片放映情况：**我们根据影院ID和放映日期来爬取对应影院的放映情况。由于放映情况是动态变化的，所以我们需要有一个解析javascript的库execjs，使用正则表达式匹配js的值，再用库处理js值。代码处理：
```python
    try:
        var = re.match(r'^var GetShowtimesJsonObjectByCinemaResult = (.+);', text).group(1)     # 获取javascript值
        if var:
            var = execjs.eval(var)      # 用库处理js值
            return var
    except:
        print('error in var = re.match ')
```
### 5.6  爬取影片排片占比
**爬取部分城市的排片占比：**除了时光网和CBO的影片数据，我们还爬取了58921的影片在城市的排片占比情况，但是58921有设置增加爬虫成本的部分。即网站的数据并不是用数字书写的，而是使用图片展示。如图中所示，

![](./_image/2017-05-25-12-52-57.jpg)
我们发现这个数字部分是一个img图片，增加了爬取难度。为此，我们需要首先获得这个img的url，代码实现：
```python
img_urls = re.findall('<img src="(http.*?)"', html_text)
```
解析完成后，照之前的处理，不过要写一个图片识别成数字的算法，这里不做过多说明。我们需要把图片解析结果替换原来的html文本。
```python
    for i in range(len(img_urls)):
        html_text = re.sub('<img src="(http.*?)" />', img_urls[i], html_text, count=1)
```
这里还使用到了pandas解析库，利用pandas的read_html函数获取表格
```python
# 用正则表达式提取出链接中的完整日期(带年份)
    reg = r'<a href="/hour/film_' + movie_id + '_(.*)" .*</a>'
    html_text = re.sub(reg, r'\1', html_text)
    # 利用pandas的read_html函数获取到表格
    table = pd.read_html(html_text, header=0)[0]
    return table, movie_name
```
当然，如果你不改变网页的编码的话，中文显示会出现乱码现象，所以还要有编码的修改。
```python
html_text = html_text.encode('latin1').decode('utf-8')
```
## 6.实现效果
### 6.1 影片信息数据表
影片数据表的字段说明：

属性名 | 属性说明 | 类型 | 主键 | 是否为空 
----|------|----|----|----
MovieID | 影片ID号  | Int | 主键 | 不为空
MovieCname | 影片中文名  | Char | | |
MovieEname | 影片英文名  | Char | | |
MovieType | 影片类型  | Char | | |
MovieLength | 影片放映长度  | Int | | |
MovieReleaseTime   | 影片首映日期  | Int | | |
MovieStandard | 影片制式  | Char | | |
MovieSumBoxOffice   | 票房总数  | Int | | |
MovieAvgPrice | 平均票价  | Int | | |
MovieAvgPeople | 平均观影人数  | Int | | |
MovieWomIndex  | 口碑指数  | Float | | |

![](./_image/2017-05-25-00-55-04.jpg)

### 6.2 演员信息数据表
演员数据表字段说明：

属性名 | 属性说明 | 类型 | 主键 | 是否为空 
----|------|----|----|----
ActorID | 演员ID号  | Int | 主键 | 不为空
ActorCName | 演员中文名  | Char | | |
ActorEName | 演员英文名  | Char | | |
ActorNation | 演员国籍  | Char | | |


![](./_image/2017-05-25-11-30-22.jpg)

### 6.3 城市信息数据表
城市数据表字段说明：

属性名 | 属性说明 | 类型 | 主键 | 是否为空 
----|------|----|----|----
DistrictID | 地区Id号  | Int | 主键 | 不为空
CityID | 城市Id号  | Int | | |
DistrictstringID | 地区字符串码  | Varchar | | |
CityCname | 城市中文名  | Char | | |
CityEname | 城市英文名  | Char | | |


![](./_image/2017-05-25-11-31-08.jpg)

### 6.4 影院信息数据表
电影院数据表字段说明：

属性名 | 属性说明 | 类型 | 主键 | 是否为空 
----|------|----|----|----
CinemaID | 影院Id号  | Int | 主键 | 不为空
CityID | 城市Id号  | Int | 主键 | |
DistrictID | 区域Id号  | Int | | |
CinemaName | 影院名称  | Varchar | | |
CinemaHallsum | 影院厅总数  | Int | | |
CinemaSeatsum   | 影院座位总数  | Int | | |
CinemaAddress | 影院地址  | Varchar | | 不为空 |
CinemaTel   | 影院联系电话  | Char | | |
CinemaBusinesshour | 影院营业时间  | Char | | |
CinemaParking | 影院是否有停车位  | Bit | | |


![](./_image/2017-05-25-11-31-34.jpg)

### 6.5 公司信息数据表
公司数据表字段说明：

属性名 | 属性说明 | 类型 | 主键 | 是否为空 
----|------|----|----|----
CompanyID | 公司Id号  | Int | 主键 | 不为空
CompanyCname | 公司中文名  | Char | | |
CompanyEname | 公司英文名  | Varchar | | |
CompanyNation | 公司所属国籍  | Char | | |


![](./_image/2017-05-25-11-32-32.jpg)

### 6.6 影片每日票房信息数据表
每日票房数据表：

属性名 | 属性说明 | 类型 | 主键 | 是否为空 
----|------|----|----|----
MovieID | 影片Id号  | Int | 主键 | 不为空
BoxOfficeDate | 票房日期  | Int | 主键 | 不为空 |
BoxOffice | 票房数量  | Int | | |
BoxOfficeAvgpeople | 平均观影人数  | Int | | |


![](./_image/2017-05-25-12-28-38.jpg)

### 6.7 影片所属公司信息数据表
影片公司映射表信息：

属性名 | 属性说明 | 类型 | 主键 | 是否为空 
----|------|----|----|----
MovieID | 影片Id号  | Int | 主键 | 不为空
CompanyID | 公司Id号  | Int | 主键 | 不为空 |
CompanyRank | 公司列表名次  | Int | | |
CompanyRole | 发行商和制作商  | Char | | |


![](./_image/2017-05-25-12-29-50.jpg)

### 6.8 时光网影片数据表
时光网影片信息表：

属性名 | 属性说明 | 类型 | 主键 | 是否为空 
----|------|----|----|----
MovieIDMtime | 时光网影片ID号  | Int | 主键 | 不为空
MovieENameMtime | 影片英文名  | Varchar |  | |
MovieCNameMtime | 影片中文名  | Varchar | | |
MovieTypeMtime | 影片类型  | Varchar | | |
MovieLengthMtime | 影片片场  | Int | | |
MovieDirectorMtime   | 导演  | Char | | |
MovieYearMtime | 年份  | Int | |  |


![](./_image/2017-05-25-12-31-23.jpg)

### 6.9 58921排片信息数据表
58921排片信息数据字段：

属性名 | 属性说明 | 类型 | 主键 | 是否为空 
----|------|----|----|----
MovieID58921 | 58921网的电影ID号58921网的电影ID号  | Int | 主键 | 不为空
MovieCName58921 | 影片中文名  | Varchar |  | 不为空 |
ScheduleDate | 排片信息日期  | Int | 主键 | 不为空 |
CityName58921 | 排片信息城市名称  | Varchar | 主键 | 不为空 |
ScheduleScene | 排片数  | Varchar | | |


![](./_image/2017-05-25-12-32-03.jpg)

### 6.10 时光网影院排片数据表
时光网影片在影院的排片信息字段：

属性名 | 属性说明 | 类型 | 主键 | 是否为空 
----|------|----|----|----
MovieIDMtime | 影片Id号  | Int | 主键 | 不为空
CinemaID | 电影院Id号  | Int | 主键 | 不为空 |
CinemaDate | 影片上映日期  |  Int | 主键 | 不为空 |
SceneMtime | 放映场次  |  Int |  |  |
CinemaSumBoxOffice | 总票房数  |  Int |  |  |
CinemaSumPeople   | 总观影人数  | Int | | |


![](./_image/2017-05-25-12-32-27.jpg)

### 6.11 时光网影片放映信息
具体的放映信息表字段：

属性名 | 属性说明 | 类型 | 主键 | 是否为空 
----|------|----|----|----
CinemaID | 电影院ID号  | Int | 主键 | 不为空
MovieIDMtime | 时光网影片ID号  | Int | 主键 | 不为空 |
ShowTimeID | 放映信息ID号  |  Int | 主键 | 不为空 |
ShowTimeIDMtime | 排片ID号  |  Int | 主键 | 不为空 |
HallID | 影厅ID号  |  Int | 主键 | 不为空 |
HallSeatCount   | 影厅座位数量  | Int | | |
HallName | 放映厅名称  | Char | | |
ShowTimeLanguage   | 语言  | Char | | |
ShowTimeStarTime | 开始放映时间  | Char | | |
ShowTimeEndTime | 结束时间  | Char | | |
PriceMtime  | 时光网票价  | Int | | |
StandardMtime  | 制式  | Char | | |


![](./_image/2017-05-25-12-33-05.jpg)

## 7. 系统测试

## 8. 遇到的问题以及解决方案

## 9. 总结