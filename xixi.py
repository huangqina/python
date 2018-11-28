from flask import Flask,abort
from flask import jsonify
from flask import render_template
from flask import request
from flask_pymongo import PyMongo
from flask_script import Manager
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:12345/test'  #如果部署在本上，其中ip地址可填127.0.0.1

mongo = PyMongo(app)
manager = Manager(app)
a = 0
@app.route('/test', methods=['GET'])
def add_user():
    global a
    a = 1 
    return '1'
while a == 1:
    mongo.db.www.insert({'a':1})
    a = 0
if __name__ == '__main__':
    # app.run(host = '0.0.0.0', por)t = 80, debug = True)
    app.run(host = '0.0.0.0', port = 8080, debug = True)