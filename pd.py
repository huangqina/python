import pymongo

client = pymongo.MongoClient(host='localhost',port=12345)

db = client.test
def show_panel_defects(i):
    collection = db.Panel
    for k in collection.aggregate([
     {'$project':{"_id":0}},
     {'$match':{"ID":i}},
     {'$lookup': {'from':"Panel_Defect","pipeline":[
         {'$project':
         {"_id":0,"Defect_ID":1,"Panel_ID":1}},
         {'$match':{ "Panel_ID": i }},
         {'$lookup':{'from':"Defect","localField":"Defect_ID",   "foreignField":"ID","as":"Defect"}
         }
         ],
         "as": "Defects"}}
     ]
    ):
        print('ID:'+str(k['ID'])+'  '+'Barcode:' + str(k['Barcode'])+'  '+'type:'+str(k['type'])+'  '+ 'size:'+ str(k['size']) +'  '+'EL_no:'+ str(k['EL_no']))
        for i in k['Defects']:
            print(i['Defect'])
def show_user(i):
    collection = db.User
     #for k in collection.collection.find({"ID":i}):
    for k in collection.aggregate([
        {'$project':{"_id":0}},{'$match':{"ID":i}}]):
        print(k)
  