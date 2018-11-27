import requests
import json
import time # 引入time模块
import datetime

#for  i in range(10000):
#    Time = time.time()
#    user_info = {'ID': i+10000, 'Type' : 'Type', 'Position': 'Position','By': 'By','Time': Time,'Size': 'Size','PanelID':i+10000}
#    r = requests.post("http://127.0.0.1:8080/adddefect", user_info)
use_info = {'Barcode': 1,'name':1}
#url = 'http://127.0.0.1:8080/finddefect' + use_info['ID']
l = requests.get("http://127.0.0.1:8080/find/defect", use_info)
#a = eval(str(l.txt))
a = eval(l.text)
for i in a:
    print(i)
#print(l.text)
Time = time.time()
user_info = {'ID': 88888+10000, 'Type' : 'Type', 'Position': 'Position','By': 'By','Time': Time,'Size': 'Size','PanelID':88888+10000}
r = requests.post("http://127.0.0.1:8080/adddefect", user_info)
#    r = requests.post("http://127.0.0.1:8080/adddefect", user_info)
ti = datetime.datetime(2018,11,23,10,17,45)
start = time.mktime(ti.timetuple())
end = time.time()
info = {'start':start,'end':end}
t = requests.get("http://127.0.0.1:8080/defecttime",info)
print(t.text)
#isn={'ID': 2, 'Barcode' : 5, 'Type': 3,'Size': 3,'EL_no': 3}
#d = requests.post("http://127.0.0.1:8080/addpanel",isn)
#print(d.text)