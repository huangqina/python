import pymongo

client = pymongo.MongoClient(host='localhost',port=12345)

db = client.test
collection = db.st
j = list(collection.find().sort([("i",-1)]).limit(1))
if 'i' in j[0]:
    i = j[0]['i'] +1 
else:
    i = 0
def insertUser(name,PW="pass"):
    collection = db.st
    global i
    st = {
        'id':i,
        'Name':str(name),
        'PW':PW
    }
    i += 1
    result = collection.insert(st)
    print(result)
def insertUserlog(User_ID,GUI_ID,time,action):
    User_log = {
        'Userid':User_ID,
        'GUI_ID':GUI_ID,
        'time':time,
        'action':action
    }
    collection = db.st
    result = collection.insert(User_log)
    print(result)
