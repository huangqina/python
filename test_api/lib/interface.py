import flask
import json
from lib.tools import my_md5,op_redis
import time
# 导入一些必须的模块，还有tools文件下已定义的的函数


server = flask.Flask(__name__)  # __name__代表当前这个python文件，把当前这个python文件当做一个服务


@server.route('/reg', methods=['post'])
# 一个装置器，将函数变成一个接口
def register():
    username = flask.request.values.get('username')
    passwd = flask.request.values.get('passwd')
    if username and passwd:
        info = op_redis('user_info_gyx:%s' % username)
        if info:
            res = {'msg': '该账号已存在', 'msg_code': 1001}
        else:
            op_redis('user_info_gyx:%s' % username, my_md5(passwd))
            res = {'msg': '注册成功', 'msg_code': 0}
    else:
        res = {'msg': '缺失必填数据', 'msg_code': 2001}
    return json.dumps(res, ensure_ascii=False)
    @server.route('/log', methods=['post'])
def login():
    username = flask.request.values.get('username')
    passwd = flask.request.values.get('passwd')
    if username and passwd:
        info = op_redis('user_info_gyx:%s' % username)  # 判断该账号是否已经注册,注册接口记录的key=username，value=md5(pwd)
        if info == my_md5(passwd):  # 判断密码是否和注册账号记录的密码一致
            lg_time = op_redis('user_info_gyx:%s' % my_md5(username))  # 判断该数据是否已经登录
            if lg_time:  # redis中该key还未失效，说明登录中
                res = {'msg': '账号已登录',
                       'msg_code': 3001,
                       'logname': my_md5(username),
                       'time': lg_time}
            else:  # 无法获取到value说明没有登录或登录已失效，存储sessionid和失效时间
                op_redis('user_info_gyx:%s' % my_md5(username), time.time(), 600)
                res = {'msg': '登录成功',
                       'msg_code': 0,
                       'logname': my_md5(username),
                       'time': time.time()}
        else:
            res = {'msg': '密码错误', 'msg_code': 2001}
    else:
        res = {'msg': '必填参数未填写请检查接口文档', 'msg_code': 1001}  # 1001就表示必填字段未填
    return json.dumps(res, ensure_ascii=False)