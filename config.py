#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time    : 2017/9/21 08:19 
# @Author  : Swper 
# @Site    : http://www.58jb.com/ 
# @File    : config.py 
# @Software: PyCharm 
 
#MONGODB CONFIG 
from flask import render_template,Flask
from flask_pymongo import PyMongo


app = Flask(__name__)


app.config['MONGO_URI'] = 'mongodb://localhost:12345/myDatabase'  #如果部署在本上，其中ip地址可填127.0.0.1

mongo = PyMongo(app)
class MongoDB(): 
    MONGO_HOST = "127.0.0.1" 
    MONGO_PORT = 27017 
    MONGO_DBNAME = "blog" 