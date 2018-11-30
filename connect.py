from flask import Flask#,abort
from flask import jsonify
#from flask import render_template
from flask import request
from flask_pymongo import PyMongo
from flask_script import Manager
import json

app = Flask(__name__)

#app.config['MONGO_DBNAME'] = 'ttt'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:12345/ttt'  #如果部署在本上，其中ip地址可填127.0.0.1

mongo = PyMongo(app)
manager = Manager(app)
mongo.db.panel.create_index([("Barcode", 1)])
#mongo.db.el
mongo.db.panel_status.create_index([("time", 1)])
mongo.db.panel_status.create_index([("Panel_ID", 1)]) 
mongo.db.defect.create_index([("time", 1)])
mongo.db.panel_defect.create_index([("Panel_ID", 1)])
mongo.db.panel_defect.create_index([("Defect_ID", 1)])

@app.route('/test', methods=['POST'])
def add_user():
  ID = request.data
  i = json.loads(ID)
  #t = i['Defects'][0]['Defect']
  return jsonify(i)

@app.route('/add/panel',methods=['POST'])
def add():
    PANEL = mongo.db.panel
    EL = mongo.db.el
    PANEL_STATUS = mongo.db.panel_status 
    DEFECT = mongo.db.defect 
    PANEL_DEFECT = mongo.db.panel_defect 
    #AI = mongo.db.ai 
    data = request.data
    info = json.loads(data)
    if not isinstance(info['barcode'],str):
        return 'barcode should be str'
    if info['cell_type'] not in ['mono','poly']:
        return 'cell_type wrong'
    if info['cell_size'] not in ['half','full']:
        return 'cell_size wrong'
    if info['cell_amount'] not in [60,72,120,144]:
        return 'cell_amount wrong'
    if not isinstance(info['el_no'],str):
        return 'el_no should be str'
    #if not isinstance(info['create_time'],str):
       # return 'create_time should be str'
    if info['ai_result'] not in [0,1,2]:
        return 'ai_result should be 0 or 1'
    if info['ai_defects']:
        for k in info['ai_defects'].keys():
            if k not in ['cr','cs','bc','mr']:
                return 'ai_defects wrong'
    if info['gui_result'] not in [0,1]:
        return 'gui_result should be 0 or 1'
    if info['gui_defects']:
        for k in info['gui_defects'].keys():
            if k not in ['cr','cs','bc','mr']:
                return 'gui_defects wrong'     
    panel_id = PANEL.insert({'Barcode' : info['barcode'], 'cell_type': info['cell_type'],'cell_size': info['cell_size'],'EL_no':info['el_no'],'create_time':info['create_time']})
    EL.insert({'EL_no': info['el_no']})
    #panel = PANEL.find_one({'_id': panel_id })
    PANEL_STATUS.insert({'Panel_ID':panel_id,'time':info['create_time'],'result':info['ai_result'],'by':'AI'})
    PANEL_STATUS.insert({'Panel_ID':panel_id,'time':info['create_time'],'result':info['gui_result'],'by':'OP'})
    if info['ai_defects']:
        for k in info['ai_defects'].keys():
            for v in info['ai_defects'][k]:
                if info['gui_defects'][k] and v in info['gui_defects'][k]:
                    defect_id = DEFECT.insert({'Type':k,'Position':v,'by':'AI','time':info['ai_time']})
                    PANEL_DEFECT.insert({'Panel_ID':panel_id,'Defect_ID':defect_id,'by':'AI','Status':'true'})
                    info['gui_defects'][k].remove(v)
                elif info['gui_defects'][k] and v not in info['gui_defects'][k]:
                    defect_id = DEFECT.insert({'Type':k,'Position':v,'by':'AI','time':info['ai_time']})
                    PANEL_DEFECT.insert({'Panel_ID':panel_id,'Defect_ID':defect_id,'by':'AI','Status':'false'})
    if info['gui_defects']:
        for k in info['gui_defects'].keys():
            if info['gui_defects'][k]:
                for v in info['gui_defects'][k]:
                    defect_id = DEFECT.insert({'Type':k,'Position':v,'by':'OP','time':info['gui_time']})
                    PANEL_DEFECT.insert({'Panel_ID':panel_id,'Defect_ID':defect_id,'by':'OP','Status':'true'})
    return 'OK'
@app.route('/find/barcode', methods=['GET','POST'])
def find(): 
    #user = mongo.db.users 
    collection = mongo.db.panel
    data = request.data
    Barcode = json.loads(data)
    Barcode = Barcode["Barcode"]
    #Barcode = request.args['Barcode']
    I = list(mongo.db.panel.find({"Barcode" : Barcode}).limit(1).sort([("_id" , -1)]))
    if I:
        ID = I[0]['_id']
    else: 
        ID = -1
    #username = user.find_one({"username":username}) 
    #if username: 
    #    return "你查找的用户名：" + username["username"] + " 密码是：" + username["password"] 
    #else: 
    #    return "你查找的用户并不存在!" 
    k = list(collection.aggregate([
    
    {'$match':{"_id":ID}},
    {'$project':{"_id":0}},
    {'$lookup': {'from':"panel_defect","pipeline":[
         
         {'$match':{ "Panel_ID": ID }},
         
         {'$lookup':{'from':"defect","localField":"Defect_ID",   "foreignField":"_id","as":"Defect"}
         },{'$project':
         {"_id":0,"Defect_ID":0,"Panel_ID":0}},{'$project':{"Defect":{"_id":0}}}],"as": "Defects"}}]))
   # a=str('ID:'+str(k[0]['ID'])+'  '+'Barcode:' + str(k[0]['Barcode'])+'  '+'type:'+str(k[0]['type'])+'  '+ 'size:'+ str(k[0]['size']) +'  '+'EL_no:'+ str(k[0]['EL_no']))

    #return str(a)+'\n'+str(k[0]['Defects'])
    #return str(k[0]['Defects'])
    return jsonify(k)
    # for i in k['Defects']:
          #  print(i['Defect'])
@app.route('/find/OK', methods=['GET','POST']) 
def findOK(): 
    data = request.data
    time = json.loads(data)
    #start = float(request.args['start'])
    #end = float(request.args['end'])
    #start = str(time[0])
    #end = str(time[1])
    start = time[0]
    end = time[1]
    a=list(mongo.db.panel_status.aggregate([
    {"$match":{'time':{"$gt":start,"$lt":end}}},
    {"$group":{
        '_id' : "$result"
            ,
        'count':{"$sum":1}}}
    ]
    ))
    return jsonify(a)
   # '''
    #if a:
   #     return str('OK'+':'+str(a[0]['count'])+' '+'Defect'+':'+str(a[1]['count']))
    #else:
   #     return 'False'
   # '''
@app.route('/find/NG', methods=['GET','POST']) 
def findNG(): 
    data = request.data
    time = json.loads(data)
    #start = float(request.args['start'])
    #end = float(request.args['end'])
    #start = str(time[0])
    #end = str(time[1])
    start = time[0]
    end = time[1]
    #start = float(request.args['start'])
    #end = float(request.args['end'])
    a=list(mongo.db.panel_status.aggregate([
    {"$match":{'time':{"$gt":start,"$lt":end}}},
    {
    "$group":{
        '_id' : "$result"
            ,
        'count':{"$sum":1}}}
    ]
    ))
    return jsonify(a)
    '''
    if a:
        return str('OK'+':'+str(a[0]['count'])+' '+'Defect'+':'+str(a[1]['count']))
    else:
        return 'False'
    '''
@app.route('/find/missrate', methods=['GET','POST']) 
def missrate(): 
    data = request.data
    time = json.loads(data)
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    start = time[0]
    end = time[1]
    k = list(mongo.db.defect.aggregate([
    
    {"$match":{'time':{"$gt":start,"$lt":end}}},
    {'$project':{"_id":1}},
    {'$lookup':{'from':'panel_defect',"localField":"_id",   "foreignField":"Defect_ID","as":"Defect"}
         },{'$project':{"Defect":
         {"_id":0,"Defect_ID":0,"Panel_ID":0}}},{'$project':{"_id":0}},{
    "$group":{
        '_id' : "$Defect.by"
            ,
        'count':{"$sum":1}}}]))
    #a=list(mongo.db.panel_defect.aggregate([
    #{'$match':{'time':{'$gt':start,'$lt':end}}},
    #{
    #'$group':{
    #    '_id' : "$by"
    #        ,
    #    'count':{'$sum':1}}}
    #]
    #))
    return jsonify(k)
    #return jsonify(a[0]['count']/(a[1]['count']+a[0]['count']))

@app.route('/find/overkillrate', methods=['GET','POST']) 
def overkillrate(): 
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    #{'$match':{'time':{'$gt':start,'$lt':end}}},
    #start = float(request.args['start'])
    #end = float(request.args['end'])
    data = request.data
    time = json.loads(data)
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    start = time[0]
    end = time[1]
    k = list(mongo.db.defect.aggregate([
    
    {"$match":{'time':{"$gt":start,"$lt":end}}},
    {'$project':{"_id":1}},
    {'$lookup':{'from':'panel_defect',"localField":"_id",   "foreignField":"Defect_ID","as":"Defect"}
         },{'$project':{"Defect":
         {"_id":0,"Defect_ID":0,"Panel_ID":0}}},{'$project':{"_id":0}},{
    "$group":{
        '_id' : "$Defect.Status"
            ,
        'count':{"$sum":1}}}]))
    '''
    if a:
        return str(a)
    else:
        return 'None'
    '''
    return jsonify(k)
    #return str(a[1]['count']/(a[1]['count']+a[0]['count']))
@app.route('/find/defect', methods=['GET','POST']) 
def defecttime(): 
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    data = request.data
    time = json.loads(data)
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    start = time[0]
    end = time[1]
    k = list(mongo.db.defect.aggregate([
    
    {"$match":{'time':{"$gt":start,"$lt":end}}},
    {'$project':{"_id":1}},
    {'$lookup':{'from':'panel_defect',"localField":"_id",   "foreignField":"Defect_ID","as":"Defect"}
         },{'$project':{"Defect":
         {"_id":0,"Defect_ID":0,"Panel_ID":0}}},{'$project':{"_id":0}},{
    "$group":{
        '_id' : "$Defect.Status"
            ,
        'count':{"$sum":1}}}]))
    '''
    if a:
        return str(a)
    else:
        return 'None'
    '''
    return jsonify(k)
if __name__ == '__main__':
    # app.run(host = '0.0.0.0', por)t = 80, debug = True)
    app.run(host = '0.0.0.0', port = 8080, debug = True)