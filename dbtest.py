# 测试连接远程数据库的代码
# 连接到我的阿里云数据库
import mysql.connector
config = {
    'host': '115.28.48.229',
    'user': 'root',
    'password': 'cnscarb',
    'port':3306,
    'database': 'movie',
    'charset': 'utf8'
}

try:
    conn = mysql.connector.connect(**config)
    print('Connect success!')
except mysql.connector.Error as e:
    print('Connect fails! {}'.format(e))
finally:
    conn.close()