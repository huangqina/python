#coding=utf-8
#mongo.py
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
    #user = mongo.db.users 
    collection = mongo.db.Panel
    Barcode = float(request.args['Barcode'])
    I = list(mongo.db.Panel.find({"Barcode" : Barcode}).limit(1).sort([("_id" , -1)]))

    ID = float(I[0]['ID'])
    #username = user.find_one({"username":username}) 
    #if username: 
    #    return "你查找的用户名：" + username["username"] + " 密码是：" + username["password"] 
    #else: 
    #    return "你查找的用户并不存在!" 
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
@app.route('/add/user', methods=['POST'])
def add_user():
  star = mongo.db.User
  ID = request.form['ID']
  Type = request.form['Type']
  Name = request.form['Name']
  PW = request.form['PW']
  star_id = star.insert({'ID': int(ID), 'Type': Type,'Name': Name,'PW': PW})
  new_star = star.find_one({'_id': star_id })
  output = {'ID':
   new_star['ID'], 'Type': new_star['Type'],'Name':new_star['Name'], 'PW':new_star['PW']}
  return jsonify({'result' : output})
@app.route('/add/Panelstatus', methods=['POST'])
def add_Panelstatus():
  star = mongo.db.Panel_status
  PanelID = request.form['PanelID']
  Time = float(request.form['Time'])
  Result = request.form['Result']
  By = request.form['By']
  star_id = star.insert({'PanelID': int(PanelID), 'Time': Time,'Result':Result,'By':By})
  new_star = star.find_one({'_id': star_id })
  a = new_star
  #output = {'ID':
   #new_star['ID'], 'Type': new_star['Type'],'Name':new_star['Name'], 'PW':new_star['PW']}
  #return jsonify({'result' : output})
  return str(a)
@app.route('/add/Userlog', methods=['POST'])
def add_Userlog():
  star = mongo.db.User_log
  User_ID = request.form['User_ID']
  GUI_ID = request.form['GUI_ID']
  Time = request.form['Time']
  PW = request.form['PW']
  Action = request.form['Action']
  star_id = star.insert({'User_ID': float(User_ID), 'GUI_ID': GUI_ID,'Time':Time,'PW':PW,'Action':Action})
  new_star = star.find_one({'_id': star_id })
  a = new_star
  #output = {'ID':
   #new_star['ID'], 'Type': new_star['Type'],'Name':new_star['Name'], 'PW':new_star['PW']}
  #return jsonify({'result' : output})
  return str(a)
@app.route('/add/AI', methods=['POST'])
def add_ai():
  star = mongo.db.AI
  ID = request.form['AI_ID']
  AI_mode = request.form['AI_mode']
  AI_parameter = request.form['AI_parameter']
  star_id = star.insert({'AI_ID': int(ID), 'AI_mode': AI_mode,'AI_parameter': AI_parameter})
  new_star = star.find_one({'_id': star_id })
  a = new_star
  #output = {'ID':
   #new_star['ID'], 'Type': new_star['Type'],'Name':new_star['Name'], 'PW':new_star['PW']}
  #return jsonify({'result' : output})
  return str(a)
@app.route('/add/EL', methods=['POST'])
def add_EL():
  star = mongo.db.EL
  EL_no = request.form['EL_no']
  EL_location = request.form['EL_location']
  star_id = star.insert({'EL_no': float(EL_no), 'EL_location': EL_location})
  new_star = star.find_one({'_id': star_id })
  a = new_star
  #output = {'ID':
   #new_star['ID'], 'Type': new_star['Type'],'Name':new_star['Name'], 'PW':new_star['PW']}
  #return jsonify({'result' : output})
  return str(a)
@app.route('/add/panel', methods=['POST'])
def add_panel():
  star = mongo.db.Panel
  ID = request.form['ID']
  Barcode = request.form['Barcode']
  Type = request.form['Type']
  Size = request.form['Size']
  EL_no = request.form['EL_no']
  star_id = star.insert({'ID': int(ID), 'Barcode' : int(Barcode), 'type': Type,'size': Size,'EL_no': EL_no})
  new_star = star.find_one({'_id': star_id })
  output = {'ID':
   new_star['ID'], 'Barcode': new_star['Barcode'],'Type':new_star['type'], 'Size':new_star['size'],'EL_no':new_star['EL_no']}
  return jsonify(output)
@app.route('/add/defect', methods=['POST'])
def add_defect():
  star = mongo.db.Defect
  s = mongo.db.Panel_Defect
  ID = float(request.form['ID'])
  Type = request.form['Type']
  Position = request.form['Position']
  By = request.form['By']
  Time = float(request.form['Time'])
  Size = request.form['Size']
  PanelID = request.form['PanelID']
  star.insert({'ID': int(ID), 'type' : Type, 'Position': Position,'by': By,'time': Time,'size': Size})
  s.insert({'ID': int(ID),'PanelID':int(PanelID)})
  return 'ok'
  #new_star = star.find_one({'_id': star_id })
  #output = {'ID':
   #new_star['ID'], 'Barcode': new_star['Barcode'],'Type':new_star['Type'], 'Size':new_star['Size'],'EL_no':new_star['EL_no']}
  #return jsonify({'result' : output})
@app.route('/find/OK', methods=['GET','POST']) 
def findOK(): 
    start = float(request.args['start'])
    end = float(request.args['end'])
    a=list(mongo.db.Panel_status.aggregate([
    {"$match":{'Time':{"$gt":start,"$lt":end}}},
    {
    "$group":{
        '_id' : "$Result"
            ,
        'count':{"$sum":1}}}
    ]
    ))
    return jsonify(a[0])
    '''
    if a:
        return str('OK'+':'+str(a[0]['count'])+' '+'Defect'+':'+str(a[1]['count']))
    else:
        return 'False'
    '''
@app.route('/find/NG', methods=['GET','POST']) 
def findNG(): 
    start = float(request.args['start'])
    end = float(request.args['end'])
    a=list(mongo.db.Panel_status.aggregate([
    {"$match":{'Time':{"$gt":start,"$lt":end}}},
    {
    "$group":{
        '_id' : "$Result"
            ,
        'count':{"$sum":1}}}
    ]
    ))
    return jsonify(a[1])
    '''
    if a:
        return str('OK'+':'+str(a[0]['count'])+' '+'Defect'+':'+str(a[1]['count']))
    else:
        return 'False'
    '''
@app.route('/find/missrate', methods=['GET','POST']) 
def missrate(): 
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    a=list(mongo.db.User_log.aggregate([
    #{'$match':{'time':{'$gt':start,'$lt':end}}},
    {
    '$group':{
        '_id' : "$action"
            ,
        'count':{'$sum':1}}}
    ]
    ))
    return str(a[0]['count']/(a[1]['count']+a[0]['count']))

@app.route('/find/overkillrate', methods=['GET','POST']) 
def overkillrate(): 
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    #{'$match':{'time':{'$gt':start,'$lt':end}}},
    #start = float(request.args['start'])
    #end = float(request.args['end'])
    a=list(mongo.db.Panel_status.aggregate([
    #{'$match':{'time':{'$gt':start,'$lt':end}}},
    {
    '$group':{
        '_id' : "$result"
            ,
        'count':{'$sum':1}}}
    ]
    ))
    '''
    if a:
        return str(a)
    else:
        return 'None'
    '''
    return str(a[1]['count']/(a[1]['count']+a[0]['count']))
@app.route('/find/defect', methods=['GET','POST']) 
def defecttime(): 
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    start = float(request.args['start'])
    end = float(request.args['end'])
    a=list(mongo.db.Defect.aggregate([
    {'$match':{'time':{'$gt':start,'$lt':end}}},{
    '$group':{
        '_id' : "null"
            ,
        'count':{'$sum':1}}}
    ]
    ))
    b=list(mongo.db.User_log.aggregate([
    #{'$match':{'time':{'$gt':start,'$lt':end}}},
    {'$match':{'time':{'$gt':start,'$lt':end}}},{
    '$group':{
        '_id' : "$action"
            ,
        'count':{'$sum':1}}}
    ]
    ))
    if a and b:
        return str(a[0]['count']-b[0]['count'])
    elif a and not b:
        return str(a[0]['count'])
    else:
        return 'None'
    #else a and not b:
    #    return str(a[0]['count'])
if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port = 80, debug = True)
    app.run(host = '0.0.0.0', port = 8080, debug = True)
    #manager.run()




