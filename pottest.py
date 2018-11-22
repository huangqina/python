import requests
import json
import time # 引入time模块
 
Time = time.time()
user_info = {'ID': 1, 'Type' : 'Type', 'Position': 'Position','By': 'By','Time': Time,'Size': 'Size','PanelID':54}
r = requests.post("http://127.0.0.1:8080/adddefect", user_info)
use_info = {'Barcode': 1,'name':1}
#url = 'http://127.0.0.1:8080/finddefect' + use_info['ID']
l = requests.get("http://127.0.0.1:8080/finddefect", use_info)
print(l.text)
info = {'start':1,'end':100}
t = requests.get("http://127.0.0.1:8080/findbytime",info)
print(t.text)