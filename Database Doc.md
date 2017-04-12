[TOC]
# Movie
## 表名称：actor 演员表 (来源:CBO)
[影人资料库](http://www.cbooo.cn/peoples)

	ActorID     演员ID号	Int	主键	不为空
	CName	    演员中文名	Char
	EName  	    演员英文名	Char
	Nation 	    演员国籍	Char

------------


## 表名称：cinema	影院表 (来源:Mtime)
[影院信息](cinemadata.json)

	CinemaID       影院Id号		Int	主键	不为空
	CityID	       城市Id号		Int	主键	不为空
	DistrictID     区域Id号		Int
	Name	       影院名称		Varchar
	Hallsum	       影院厅总数	Int
	Sitsum	       影院座位总数	Int
	Address	       影院地址		Varchar
	Tel            影院联系电话	Char
	Businesshour   影院营业时间	Char

------------

## 表名称：city	城市表 (来源:Mtime)

	DistrictID	地区Id号	Int	主键	不为空
	CityID		城市Id号	Int
	StringID	地区字符串码	Varchar
	Cname		城市中文名	Char
	Ename		城市英文名	Char

------------

## 表名称：company	公司表 (来源:CBO)
[影院公司](http://www.cbooo.cn/c/6)
>注：影院公司的ID号是特殊的，网站把影院资料库归类到影片资料库中，所以查找会有困难

	CompanyID	公司Id号		Int	主键	不为空
	Cname		公司中文名	Char
	Ename		公司英文名	Varchar
	Nation		公司所属国籍	Char

------------

## 表名称：movie	影片表 (来源:CBO)
[影片资料库](www.cbooo.cn/movie)

	MovieID	      影片Id号		Int	主键	不为空
	Cname	      影片中文名		Char
	Ename	      影片英文名		Char
	Type	      影片类型		Char
	Length	      影片放映长度	Int
	Releasetime   影片首映日期	Int
	Standard      影片制式		Char
	Sumboxoffice  票房总数		Int
	Avgprice      平均票价		Int
	Avgpeople     平均观影人数	Int
	Womindex      口碑指数		Float

------------

## 表名称：movie_actor	影片演员映射表 (来源:CBO)
[影人资料库](http://www.cbooo.cn/peoples)

	MovieID	    影片Id号	Int	主键	不为空
	ActorID	    演员Id号	Int	主键	不为空
	Rank	    演员列表名次	Int
	Role	    影片职位	Char

------------

## 表名称：movie_boxoffice	影片票房表 (来源:CBO)
[票房信息](http://www.cbooo.cn/BoxOffice/GetDayBoxOffice?num=)

	MovieID	    影片Id号	Int	主键	不为空
	Date	    票房日期	Int	主键	不为空
	Boxoffice   票房数量	Int
	Avgpeople   平均观影人数	Int

------------

## 表名称：movie_cinema	影院-影片表 (来源:Mtime)(未完成)
[影院信息](cinemadata.json)

	MovieID		影片Id号		Int	主键	不为空
	CinemaID	电影院Id号	Int	主键	不为空
	Date		影片上映日期	Int	主键	不为空
	Scene		放映场次		Int
	Sumboxoffice	总票房数		Int
	Sumpeople	总观影人数	Int

------------

## 表名称：movie_company	影院-公司映射表 (来源:CBO)
[影院公司](http://www.cbooo.cn/c/6)
>注：影院公司的ID号是特殊的，网站把影院资料库归类到影片资料库中，所以查找会有困难

	MovieID	       影片Id号		Int	主键	不为空
	CompanyID      公司Id号		Int	主键	不为空
	Rank	       公司列表名次	Int
	Role	       发行商和制作商	Char

------------

## 表名称：movie_scene	影片排片表 (来源:CBO)
[排片信息](http://www.cbooo.cn/Screen/getScreenData?days=)

	MovieID	     影片Id号		Int	主键	不为空
	CityID	     城市Id号		Int	主键	不为空
	Date         影片放映日期		Int	主键	不为空
	Scene	     影片放映场次数	Int

------------

## 表名称：movie_mtime	时光网影片信息表 (来源:Mtime)
[时光网](http://www.mtime.com/)

	MovieIDMtime	时光网影片ID号	Int	主键	不为空
	EName		片英文名		Varchar
	CName		影片中文名	Varchar

------------

## 表名称：showtime	时光网放映信息 (来源:Mtime)
[时光网](http://www.mtime.com/)

	CinemaID	电影院ID号	Int	主键	不为空
	MovieIDMtime	时光网影片ID号	Int	主键	不为空
	ID		放映信息ID号	Int	主键	不为空
	ShowtimeID	排片ID号		Int	主键	不为空
	HallID		影厅ID号		Int	主键	不为空
	SeatCount	影厅座位数量	Int
	HallName	放映厅名称	Char
	Language	语言		Char
	StarTime	开始放映时间	Char
	EndTime		结束时间		Char
	Price		时光网票价	Int
	Version		制式		Char
	
------------

## 表名称：movie_schedule	影片每日排片 (来源:58921)
[58921/schedule](http://58921.com/schedule/)

	MovieID58921	58921网的电影ID号	int	主键	不为空
	Name		影片中文名		varchar		不为空
	Date		排片信息日期		int	主键	不为空
	City		排片信息城市		varchar	主键	不为空
	Scene		拍片数			varchar		不为空

------------

## 表名称：movie_dict	影片字典 (来源:CBO|Mtime|58921)

	ID		本地ID		int	主键	不为空
	MovieID 	CBO电影ID	int
	MovieIDMtime	时光网电影ID	int
	MovieID58921	58921电影ID	int