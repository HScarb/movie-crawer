import tushare
import tushare as ts

for day in range(10,23):
    print(ts.day_boxoffice('2017-03-' + str(day)))
    print('2017-03-' + str(day))
pass

print(ts.day_boxoffice('2017-02-15'))
print(ts.day_boxoffice('2015-07-15'))