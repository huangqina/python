from flask import Flask,abort
from flask import jsonify
from flask import render_template
from flask import request
from flask_pymongo import PyMongo
from flask_script import Manager
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'tttt'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:12345/tttt'  #如果部署在本上，其中ip地址可填127.0.0.1

mongo = PyMongo(app)
manager = Manager(app)

@app.route('/test', methods=['POST'])
def add_user():
  ID = request.data
  i = json.loads(ID)
  t = i['Defects'][0]['Defect']
  return jsonify(t)
  
@app.route('/add/panel',methods=['POST'])
def add():
    PANEL = mongo.db.panel
    EL = mongo.db.el
    PANEL_STATUS = mongo.db.panel_status 
    DEFECT = mongo.db.defect 
    PANEL_DEFECT = mongo.db.panel_defect 
    AI = mongo.db.ai 
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
    if not isinstance(info['create_time'],str):
        return 'create_time should be str'
    if info['ai_result'] not in [0,1]:
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
    panel = PANEL.find_one({'_id': panel_id })
    PANEL_STATUS.insert({'Panel_ID':panel['Barcode'],'time':info['create_time'],'result':info['ai_result'],'by':'AI'})
    PANEL_STATUS.insert({'Panel_ID':panel['Barcode'],'time':info['create_time'],'result':info['gui_result'],'by':'OP'})
    if info['ai_defects']:
        for k in info['ai_defects'].keys():
            for v in info['ai_defects'][k]:
                if info['gui_defects'][k] and v in info['gui_defects'][k]:
                    defect_id = DEFECT.insert({'Type':k,'Position':v,'by':'AI','time':info['ai_time']})
                    PANEL_DEFECT.insert({'Panel_ID':panel_id,'Defect_id':defect_id,'by':'AI','Status':'true'})
                    info['gui_defects'][k].remove(v)
                elif info['gui_defects'][k] and v not in info['gui_defects'][k]:
                    defect_id = DEFECT.insert({'Type':k,'Position':v,'by':'AI','time':info['ai_time']})
                    PANEL_DEFECT.insert({'Panel_ID':panel_id,'Defect_id':defect_id,'by':'AI','Status':'false'})
    if info['gui_defects']:
        for k in info['gui_defects'].keys():
            if info['gui_defects'][k]:
                for v in info['gui_defects'][k]:
                    defect_id = DEFECT.insert({'Type':k,'Position':v,'by':'OP','time':info['gui_time']})
                    PANEL_DEFECT.insert({'Panel_ID':panel_id,'Defect_id':defect_id,'by':'OP','Status':'true'})
    return 'OK'
if __name__ == '__main__':
    # app.run(host = '0.0.0.0', por)t = 80, debug = True)
    app.run(host = '0.0.0.0', port = 8080, debug = True)