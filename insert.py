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
#@app.route('/login', methods=['GET'])
#def get_all_users():
  #star = mongo.db.userInfo.find()
  #output = []
  #for s in star:
  #  output.append({'name' : s['name'], 'pwd' : s['pwd']})
  #return jsonify({'result' : output})

#@app.route('/findpanel/<int:num>') 
@app.route('/')
def re():
    return '<p>192.168.2.25:8080/finddefect     #defect of certain panel with given barcode</p><p>192.168.2.25:8080/adduser     #Insert  user</p><p>192.168.2.25:8080/addpanel      #Insert  panel</p><p>192.168.2.25:8080/defect      #Insert  defect</p><p>192.168.2.25:8080/findbytime       #no. of defect panel in given time period no. of ok panel in given time period</p><p>192.168.2.25:8080/missrate     #miss rate (new annotation by operator / cells checked)</p><p>192.168.2.25:8080/overkillrate     #overkill rate (deleted AI annotation by operator / cells checked)</p><p>192.168.2.25:8080/defecttime     #no. of certain defect in given time period</p>'
@app.route('/show')
def rei():
    return render_template("a.html")
@app.route('/find/defect', methods=['GET','POST'])
def find(): 
    collection = mongo.db.Panel
    Barcode = float(request.args['Barcode'])
    I = list(mongo.db.Panel.find({"Barcode" : Barcode}).limit(1).sort([("_id" , -1)]))
    ID = float(I[0]['ID'])
    k = list(collection.aggregate([
    {'$project':{"_id":0}},
    {'$match':{"ID":ID}},
    {'$lookup': {'from':"Panel_Defect","pipeline":[
         {'$project':
         {"_id":0,"Defect_ID":1,"Panel_ID":1}},
         {'$match':{ "Panel_ID": ID }},
         {'$lookup':{'from':"Defect","localField":"Defect_ID",   "foreignField":"ID","as":"Defect"}
         },{'$project':{"Defect":{"_id":0}}}],"as": "Defects"}}]))
   # a=str('ID:'+str(k[0]['ID'])+'  '+'Barcode:' + str(k[0]['Barcode'])+'  '+'type:'+str(k[0]['type'])+'  '+ 'size:'+ str(k[0]['size']) +'  '+'EL_no:'+ str(k[0]['EL_no']))

    #return str(a)+'\n'+str(k[0]['Defects'])
    #return str(k[0]['Defects'])
    return jsonify(k)
    # for i in k['Defects']:
          #  print(i['Defect'])
@app.route('/add/Panel', methods=['POST'])
def add_Panel():
  Barcode = float(request.args['Barcode'])
  EL.no = float(request.args['EL.no'])
  Panel_type = request.form['Panel-type']
  Type = request.form['Type']
  Name = request.form['Name']
  Time = request.form['Time']
  star_id = star.insert({'ID': int(ID), 'Type': Type,'Name': Name,'PW': PW})
  new_star = star.find_one({'_id': star_id })
  output = {'ID':
   new_star['ID'], 'Type': new_star['Type'],'Name':new_star['Name'], 'PW':new_star['PW']}
  return jsonify({'result' : output})