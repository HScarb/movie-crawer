# Movie
## 表名称：actor
	ActorID 	演员ID号   Int 主键	不为空
	CName	    演员中文名  Char
	EName  	    演员英文名  Char
	Nation 	    演员国籍    Char

------------


## 表名称：cinema
	CinemaID	   影院Id号    Int	   主键	不为空
	CityID	       城市Id号    Int    主键	不为空
	DistrictID     区域Id号    Int
	Name	       影院名称     Varchar
	Hallsum	       影院厅总数   Int
	Sitsum	       影院厅座位数 Int
	Address	       影院地址    Varchar
	Tel	    	   影院联系电话 Char
	Businesshour   影院营业时间 Char

------------

## 表名称：city
	CityID	   城市Id号 	   Int    主键	不为空
	ParentID   区域所在Id号    Int
	StringID   地区字符串Id号   Varchar
	Cname	   城市中文名 	  Char
	Ename	   城市英文名 	  Char

------------

## 表名称：company
	CompanyID	  公司Id号    Int 主键    不为空
	Cname	  	  公司中文名   Char
	Ename	  	  公司英文名   Varchar
	Nation	      公司所属国籍 Char

------------

## 表名称：movie
	MovieID	      影片Id号     Int 主键	不为空
	Cname	      影片中文名    Char
	Ename	      影片英文名    Char
	Type	      影片类型      Char
	Length	      影片放映长度  Int
	Releasetime   影片首映日期  Int
	Standard      影片制式     Char
	Sumboxoffice  票房总数     Int
	Avgprice      平均票价     Int
	Avgpeople     平均观影人数  Int
	Womindex      口碑指数     Float

------------

## 表名称：movie_actor
	MovieID	    影片Id号    Int 主键不为空
	ActorID	    演员Id号    Int 主键不为空
	Rank	    演员列表名次 Int
	Role	    影片职位    Char

------------

## 表名称：movie_boxoffice
	MovieID	    影片Id号    Int 主键不为空
	Date	    票房日期    Int 主键不为空
	Boxoffice   票房数量    Int
	Avgpeople   平均观影人数 Int

------------

## 表名称：movie_cinema
	MovieID	       影片Id号      Int 主键	不为空
	CinemaID	   电影院Id号    Int 主键	不为空
	Date	       影片上映日期   Int 主键	不为空
	Scene	       放映场次      Int
	Sumboxoffice   总票房数      Int
	Sumpeople	   总观影人数    Int

------------

## 表名称：movie_company
	MovieID	       影片Id号     Int 主键	不为空
	CompanyID      公司Id号     Int 主键	不为空
	Rank	       公司列表名次  Int
	Role	       发行商和制作商 Char

------------

## 表名称：movie_scene
	MovieID	     影片Id号  	Int 主键	不为空
	CityID	     城市Id号  	Int 主键	不为空
	Date         影片放映日期   Int 主键  不为空
	Scene	     影片放映场次数 Int
