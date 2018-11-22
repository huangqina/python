#coding=utf-8
#mongo.py
from flask import Flask,abort
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'rest'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:12345/rest'  #如果部署在本上，其中ip地址可填127.0.0.1

mongo = PyMongo(app)

@app.route('/login', methods=['GET'])
def get_all_users():
  star = mongo.db.userInfo.find()
  output = []
  for s in star:
    output.append({'name' : s['name'], 'pwd' : s['pwd']})
  return jsonify({'result' : output})


@app.route('/register', methods=['POST'])
def add_user():
  star = mongo.db.userInfo
  name = request.json['name']
  pwd = request.json['pwd']
  star_id = star.insert({'name': name, 'pwd': pwd})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'pwd' : new_star['pwd']}
  return jsonify({'result' : output})

@app.route('/modify/<string:name>', methods=['PUT'])
def update_user(name):
    user = mongo.db.userInfo.find({"name":name})
    output = []
    for s in user:
      output.append({'name': s['name'], 'pwd': s['pwd']})
    if len(output) == 0:
      abort(404)
    mongo.db.userInfo.update({"name":name},{'$set':{"name":"LZ111"}})
    return jsonify({'result': output})

@app.route('/delete/<string:name>', methods=['DELETE'])
def delete_user(name):
    user = mongo.db.userInfo.find({"name": name})
    output = []
    for s in user:
      output.append({'name': s['name'], 'pwd': s['pwd']})
    if len(output) == 0:
      abort(404)
    mongo.db.userInfo.remove({'name': name})
    return jsonify({'result': True})



if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port = 80, debug = True)
    app.run(host = '127.0.0.1', port = 8080, debug = True)