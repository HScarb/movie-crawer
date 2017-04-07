# Movie
## 表名称：actor	演员
[影人资料库](http://www.cbooo.cn/peoples)

	ActorID     演员ID号	Int  主键	不为空
	CName	    演员中文名	Char
	EName  	    演员英文名	Char
	Nation 	    演员国籍	Char

------------


## 表名称：cinema	电影院
[影院信息](cinemadata.json)

	CinemaID       影院Id号		Int  主键	不为空
	CityID	       城市Id号		Int  主键	不为空
	DistrictID     区域Id号		Int
	Name	       影院名称		Varchar
	Hallsum	       影院厅总数	Int
	Sitsum	       影院厅座位数	Int
	Address	       影院地址		Varchar
	Tel            影院联系电话	Char
	Businesshour   影院营业时间	Char

------------

## 表名称：city	城市
	CityID	   城市Id号	Int  主键	不为空
	ParentID   区域所在Id号	Int
	StringID   地区字符串Id号	Varchar
	Cname	   城市中文名	Char
	Ename	   城市英文名	Char

------------

## 表名称：company	公司
[影院公司](http://www.cbooo.cn/c/6)
>注：影院公司的ID号是特殊的，网站把影院资料库归类到影片资料库中，所以查找会有困难

	CompanyID	公司Id号		Int  主键	不为空
	Cname		公司中文名	Char
	Ename		公司英文名	Varchar
	Nation		公司所属国籍	Char

------------

## 表名称：movie	影片
[影片资料库](www.cbooo.cn/movie)

	MovieID	      影片Id号		Int  主键	不为空
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

## 表名称：movie_actor	影片演员
[影人资料库](http://www.cbooo.cn/peoples)

	MovieID	    影片Id号	Int  主键	不为空
	ActorID	    演员Id号	Int  主键	不为空
	Rank	    演员列表名次	Int
	Role	    影片职位	Char

------------

## 表名称：movie_boxoffice	影片票房
[票房信息](http://www.cbooo.cn/BoxOffice/GetDayBoxOffice?num=)

	MovieID	    影片Id号	Int  主键	不为空
	Date	    票房日期	Int  主键	不为空
	Boxoffice   票房数量	Int
	Avgpeople   平均观影人数	Int

------------

## 表名称：movie_cinema	放映电影院
[影院信息](cinemadata.json)

	MovieID		影片Id号		Int  主键	不为空
	CinemaID	电影院Id号	Int  主键	不为空
	Date		影片上映日期	Int  主键	不为空
	Scene		放映场次		Int
	Sumboxoffice	总票房数		Int
	Sumpeople	总观影人数	Int

------------

## 表名称：movie_company	影片发行制作公司
[影院公司](http://www.cbooo.cn/c/6)
>注：影院公司的ID号是特殊的，网站把影院资料库归类到影片资料库中，所以查找会有困难

	MovieID	       影片Id号		Int  主键	不为空
	CompanyID      公司Id号		Int  主键	不为空
	Rank	       公司列表名次	Int
	Role	       发行商和制作商	Char

------------

## 表名称：movie_scene	影片排片
[排片信息](http://www.cbooo.cn/Screen/getScreenData?days=)

	MovieID	     影片Id号		Int  主键	不为空
	CityID	     城市Id号		Int  主键	不为空
	Date         影片放映日期		Int  主键	不为空
	Scene	     影片放映场次数	Int

------------

## 表名称：movue_mtime	时光网影片信息
[时光网](http://www.mtime.com/)

	MtimeMovieID	时光网影片ID号	Int    主键	不为空
	EName		片英文名		Varchar
	CName		影片中文名	Varchar

------------

## 表名称：showtime	时光网放映信息
[时光网](http://www.mtime.com/)

	CinemaID	电影院ID号	Int  主键	不为空
	MtimeMovieID	时光网影片ID号	Int  主键	不为空
	ID号		放映ID号		Int  主键	不为空
	ShowtimeID	放映场次ID号	Int  主键	不为空
	HallID		放映厅ID号	Int  主键	不为空
	SeatCount	座位数量		Int
	HallName	放映厅名称	Char
	Language	影片语种		Char
	StarTime	影片开始放映时间	Char
	EndTime		影片结束时间	Char
	Price		影片价格		Int
	Version		影片制式		Char