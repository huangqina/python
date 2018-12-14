from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, NotMasterError
#client = MongoClient('localhost')
#db = client.ttt
#task = db.i
#print(task.count())
host = 'localhost'
port = 27017
def connect( host, port):
        count = 0
        while True:
            client = MongoClient(host, port, serverSelectionTimeoutMS=5)
            try:
                client.admin.command("ping")
            except ConnectionFailure:
                count = count + 1
            except NotMasterError:
                print('a')    
            else:
                break
            if count == 5 and port < 27019:
                return connect(host, port+1)
            elif count > 5:
                return False
        return client
connect(host, port)