import hashlib
import pymongo
#from config.setting import MYSQL_INFO, REDIS_INFO


def my_db(sql):
    client = pymongo.MongoClient(host='localhost',port=12345)  # 链接数据库,MYSQL_INFO本身就定义成了字典的，所以这边传入后会自动调整数据
    # 调整为key = value的格式
    cur = coon.cursor()  # 建立游标
    cur.execute(sql)  # 执行sql语句
    if sql.strip()[:6].upper() == 'SELECT':  # 判断sql语句是否是单纯的查询语句
        res = cur.fetchall()
    else:
        coon.commit()
        res = cur.fetchall()
    cur.close()  # 关闭游标
    coon.close()  # 关闭链接
    return res


def op_redis(k, v=None, time=None):
    r = redis.Redis(**REDIS_INFO)  # 链接redis数据库
    if v:  # 判断是否有value输入
        if time:  # 判断是否有时效时间输入
            r.setex(k, v, time)
            res = 'ok'
        else:
            r.set(k, v)
            res = 'ok'
    else:
        res = r.get(k)
        if res:
            res = res.decode()
        else:
            pass
    return res


def my_md5(s):
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()