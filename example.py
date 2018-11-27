import requests
#import json
import time 
import datetime



#panel = {'ID': 1, 'Barcode' : 1, 'Type': 'AI','Size': 'Size','EL_no': 1} 
#r = requests.post("http://192.168.2.25:8080/addpanel", panel) 
#print(r.text)
#info = {'Barcode': 1}
#url = 'http://127.0.0.1:8080/finddefect' + use_info['ID']
#l = requests.get("http://127.0.0.1:8080/finddefect", info)
#a = eval(str(l.txt))
#a = eval(l.text)
#for i in a:
    #print(i)
#print(l.text)
'''
Time = time.time()
for i in range(100):
    if i%3:
        by = 'HUNAM'
        re = 'OK'
    else:
        by = 'AI'
        re = 'NG'
    info = {'PanelID': i+15000, 'Time': Time,'Result':re,'By':by}

    requests.post("http://192.168.2.25:8080/addPanelstatus", info) 
'''
ti = datetime.datetime(2018,11,23,10,17,45)
start = time.mktime(ti.timetuple())
end = time.time()
info = {'start':start,'end':end}
t = requests.get("http://127.0.0.1:8080/find/OK",info)
print(t.text)