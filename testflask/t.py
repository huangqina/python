from flask import Flask#,abort
from flask import jsonify
#from flask import render_template
from flask import request
from flask_pymongo import PyMongo
from flask_script import Manager
import json

app = Flask(__name__)

#app.config['MONGO_DBNAME'] = 'ttt'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:12345/tttt'  #如果部署在本上，其中ip地址可填127.0.0.1

mongo = PyMongo(app)
star = mongo.db.EL
star_id = star.insert({'EL_no': 1})
new_star = star.find_one({'_id': star_id })
a = new_star
  #output = {'ID':
   #new_star['ID'], 'Type': new_star['Type'],'Name':new_star['Name'], 'PW':new_star['PW']}
  #return jsonify({'result' : output})
print( str(a))

