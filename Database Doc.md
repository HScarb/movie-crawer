[TOC]
# Movie
## 表名称：actor 演员表 (来源:CBO)
[影人资料库](http://www.cbooo.cn/peoples)

	ActorID     	    演员ID号	Int	主键	不为空
	ActorCName	    演员中文名	Char
	ActorEName  	    演员英文名	Char
	ActorNation 	    演员国籍	Char

------------


## 表名称：cinema	影院表 (来源:Mtime)
[影院信息](cinemadata.json)

	CinemaID       			影院Id号		Int	主键	不为空
	CinemaCityID	       		城市Id号		Int	主键	不为空
	CinemaDistrictID     		区域Id号		Int
	CinemaName	        	影院名称		Varchar
	CinemaHallsum	       		影院厅总数	Int
	CinemaSitsum	       		影院座位总数	Int
	CinemaAddress	       		影院地址		Varchar
	CinemaTel            		影院联系电话	Char
	CinemaBusinesshour   		影院营业时间	Char

------------

## 表名称：city	城市表 (来源:Mtime)

	DistrictID			地区Id号		Int	主键	不为空
	CityID				城市Id号		Int
	StringID			地区字符串码	Varchar
	CityCname			城市中文名	Char
	CityEname			城市英文名	Char

------------

## 表名称：company	公司表 (来源:CBO)
[影院公司](http://www.cbooo.cn/c/6)
>注：影院公司的ID号是特殊的，网站把影院资料库归类到影片资料库中，所以查找会有困难

	CompanyID		公司Id号		Int	主键	不为空
	CompanyCname		公司中文名	Char
	CompanyEname		公司英文名	Varchar
	CompanyNation		公司所属国籍	Char

------------

## 表名称：movie	影片表 (来源:CBO)
[影片资料库](www.cbooo.cn/movie)

	MovieID	      	  	  影片Id号		Int	主键	不为空
	MovieCname	  	  影片中文名		Char
	MovieEname	  	  影片英文名		Char
	MovieType	      	  影片类型		Char
	MovieLength	      	  影片放映长度		Int
	MovieReleasetime   	  影片首映日期		Int
	MovieStandard      	  影片制式		Char
	MovieSumboxoffice  	  票房总数		Int
	MovieAvgprice      	  平均票价		Int
	MovieAvgpeople     	  平均观影人数		Int
	MovieWomindex      	  口碑指数		Float

------------

## 表名称：movie_actor	影片演员映射表 (来源:CBO)
[影人资料库](http://www.cbooo.cn/peoples)

	MovieID	    影片Id号	Int	主键	不为空
	ActorID	    演员Id号	Int	主键	不为空
	ActorRank	    	    演员列表名次	Int
	ActorRole	      	    影片职位	Char

------------

## 表名称：movie_boxoffice	影片票房表 (来源:CBO)
[票房信息](http://www.cbooo.cn/BoxOffice/GetDayBoxOffice?num=)

	MovieID	    影片Id号	Int	主键	不为空
	BoxOfficeDate	    票房日期	Int	主键	不为空
	Boxoffice     房数量	Int
	BoxOfficeAvgpeople     平均观影人数	Int

------------

## 表名称：movie_cinema	影院-影片表 (来源:Mtime)(未完成)
[影院信息](cinemadata.json)

	MovieID		影片Id号		Int	主键	不为空
	CinemaCinemaID		电影院Id号	Int	主键	不为空
	CinemaDate			影片上映日期	Int	主键	不为空
	CinemaScene		放映场次		Int
	CinemaSumboxoffice		总票房数		Int
	CinemaSumpeople		总观影人数	Int

------------

## 表名称：movie_company	影院-公司映射表 (来源:CBO)
[影院公司](http://www.cbooo.cn/c/6)
>注：影院公司的ID号是特殊的，网站把影院资料库归类到影片资料库中，所以查找会有困难

	MovieID	       影片Id号		Int	主键	不为空
	CompanyID          公司Id号		Int	主键	不为空
	CompanyRank	       公司列表名次	Int
	CompanyRole	       发行商和制作商	Char

------------

## 表名称：movie_scene	影片排片表 (来源:CBO)
[排片信息](http://www.cbooo.cn/Screen/getScreenData?days=)

	MovieID	     影片Id号		Int	主键	不为空
	SceneCityName	     城市Id号		Int	主键	不为空
	SceneDate               影片放映日期		Int	主键	不为空
	SceneScene	     	     影片放映场次数	Int

------------

## 表名称：movie_mtime	时光网影片信息表 (来源:Mtime)
[时光网](http://www.mtime.com/)

	MovieIDMtime		时光网影片ID号	Int	主键	不为空
	MovieMtimeEName		影片英文名		Varchar
	MovieMtimeCName		影片中文名	Varchar
	MovieMtimeType		影片类型	varchar
	MovieMtimeLength	影片片场	int
	MovieMtimeDirector	导演	char
	MovieMtimeYear	年份	int

------------

## 表名称：showtime	时光网放映信息 (来源:Mtime)
[时光网](http://www.mtime.com/)

	CinemaID	电影院ID号	Int	主键	不为空
	MovieIDMtime	时光网影片ID号	Int	主键	不为空
	ShowTimeID		放映信息ID号	Int	主键	不为空
	ShowTimeShowTimeID		排片ID号		Int	主键	不为空
	ShowTimeHallID		影厅ID号		Int	主键	不为空
	ShowTimeSeatCount	影厅座位数量	Int
	ShowTimeHallName	放映厅名称	Char
	ShowTimeLanguage	语言		Char
	ShowTimeStarTime	开始放映时间	Char
	ShowTimeEndTime		结束时间		Char
	ShowTimePrice		时光网票价	Int
	ShowTimeVersion		制式		Char
	
------------

## 表名称：movie_schedule	影片每日排片 (来源:58921)
[58921/schedule](http://58921.com/schedule/)

	MovieID58921	58921网的电影ID号	int	主键	不为空
	Name58921		影片中文名		varchar		不为空
	ScheduleDate		排片信息日期		int	主键	不为空
	ScheduleCity		排片信息城市		varchar	主键	不为空
	ScheduleScene		排片数			varchar		不为空

------------

## 表名称：movie_dict	影片字典 (来源:CBO|Mtime|58921)

	MovieDictID		本地ID		int	主键	不为空
	MovieID 	CBO电影ID	int
	MovieIDMtime	时光网电影ID	int
	MovieID58921	58921电影ID	int