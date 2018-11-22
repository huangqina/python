import pymongo

client = pymongo.MongoClient(host='localhost',port=12345)
db = client.test
collection = db.Panel
Barcode = 1
I = list(collection.find({"Barcode" : Barcode}).limit(1).sort([("_id" , -1)]))
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
         }],"as": "Defects"}}]))
a=str('ID:'+str(k[0]['ID'])+'  '+'Barcode:' + str(k[0]['Barcode'])+'  '+'type:'+str(k[0]['type'])+'  '+ 'size:'+ str(k[0]['size']) +'  '+'EL_no:'+ str(k[0]['EL_no']))

print(str(a)+'\n'+str(k[0]['Defects']))