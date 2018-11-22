from flask import Flask,render_template 
from flask_pymongo import PyMongo 
from config import MongoDB 
 
app = Flask(__name__) 
#实例化数据库配置，可以直接一行解决

app.config['MONGO_URI'] = 'mongodb://localhost:12345/myDatabase' 
mongo = PyMongo(app) 
 
#也可以两行来实例化配置,这里会把所有以MONGO开头的配置加入。
# app.config.from_object(MongoDB) 
# mongo.init_app(app,config_prefix="MONGO%") 
 
@app.route('/') 
def index(): 
    # 测试数据库是否连接成功，如果成功就会返回Pymongo一个游标对象。
    onlines_users = mongo.db.system.users.find() 
    return render_template('index.html',onlines_usersonlines_users=onlines_users) 
#如果想在Index.html文件里显示效果就要加入{{ onlines_users }}调用方法。
 
#插入数据[这里指定了数据]
@app.route('/add/')          #后面加入了一个"/"作用跟不加的效果自己可以测试。
def add(): 
    user = mongo.db.users 
    user.insert({"username":"swper","password":"123456"}) 
    if  user: 
        return "用户已经存在！" 
    else: 
        return "Added User!" 
 
#查询数据，通过后面的<username>传入要查询的用户名 
@app.route('/find/<username>') 
def find(username): 
    user = mongo.db.users 
    username = user.find_one({"username":username}) 
    if username: 
        return "你查找的用户名：" + username["username"] + " 密码是：" + username["password"] 
    else: 
        return "你查找的用户并不存在!" 
 
#更新数据[monogodb版本可能有所不同] 
@app.route('/update/<username>') 
def update(username): 
    user = mongo.db.users 
    passwd = "abcd10023" 
    userusername = user.find_one({"username":username}) 
    username["password"] = passwd 
    user.save(username) 
    return "Update OK " + username["username"] 
 
#删除数据 
@app.route('/delete/<username>') 
def delete(username): 
    user = mongo.db.users 
    userusername = user.find_one({"username":username}) 
    user.remove(username) 
    if username: 
        return "Remove " + username["username"] + " Ok!" 
    else: 
        return "用户不存在，请核对后再操作!" 
 
 
if __name__ == '__main__': 
    app.run(debug=True) 