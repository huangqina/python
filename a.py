import pymongo

client = pymongo.MongoClient(host='localhost',port=12345)

db = client.test

collection = db.Panel
k = list(collection.aggregate([
    {'$project':{"_id":0}},
    {'$match':{"ID":7}},
    {'$lookup': {'from':"Panel_Defect","pipeline":[
         {'$project':
         {"_id":0,"Defect_ID":1,"Panel_ID":1}},
         {'$match':{ "Panel_ID": 7 }},
         {'$lookup':{'from':"Defect","localField":"Defect_ID",   "foreignField":"ID","as":"Defect"}
         }],"as": "Defects"}}]))
#print('ID:'+str(k['ID'])+'  '+'Barcode:' + str(k['Barcode'])+'  '+'type:'+str(k['type'])+'  '+ 'size:'+ str(k['size']) +'  '+'EL_no:'+ str(k['EL_no']))
#for i in k['Defects']:
b= ID:'+str(k['ID'])+'  '+'Barcode:' + str(k['Barcode'])+'  '+'type:'+str(k['type'])+'  '+ 'size:'+ str(k['size']) +'  '+'EL_no:'+ str(k['EL_no'])
b = str(k)
a = 1