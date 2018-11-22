#注册接口
import flask
from flask import request #想获取到请求参数的话，就得用这个
server = flask.Flask(__name__) #把这个python文件当做一个web服务
def md5_passwd(str,salt='123456'):
    #satl是盐值，默认是123456
    str=str+salt
    import hashlib
    md = hashlib.md5()  # 构造一个md5对象
    md.update(str.encode())
    res = md.hexdigest()
    return res

def conn_mysql(sql):
    import pymysql
    conn = pymysql.connect(host='211.149.218.16',user='jxz',password='123456',db='jxz',charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    res = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return res
@server.route('/register',methods=['get','post'])#router里面第一个参数，是接口的路径
def reg():
    # username = request.values.get('username')#这里就是你调用接口的是传入的参数
    # password = request.values.get('password')#这里就是你调用接口的是传入的参数
    print(request.json)
    username = request.json.get("username")#入参类型是json的话，那么必须得用.json方法才能获取到数据
    password = request.json.get("password")
    if username and password:
        sql = 'select username,password from user where username="%s";'%username
        res = conn_mysql(sql)#执行sql
        if res:
            return '{"code":300,"msg":"你注册的用户已经存在"}'
        else:
            password = md5_passwd(password)#调用加密的函数
            sql = 'insert into user  (username,password) values ("%s","%s");'%(username,password)
            conn_mysql(sql)
            return '{"code":200,"msg":"注册成功！"}'
    else:
        return '{"code":938,"msg":"必填参数未填，请看接口文档！"}'

@server.route('/login')
def login():

    return '{"msg":"登录成功"}'

server.run(port=8000,debug=True,host='0.0.0.0')