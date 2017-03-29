import tushare as ts

df = ts.realtime_boxoffice()
print(df)

def _random(n=13):
    from random import randint
    start = 10**(n-1)
    end = (10**n)-1
    return str(randint(start, end))
