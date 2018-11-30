import requests
import json
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
#info = { 'barcode':'13245', 'cell_type':'mono','cell_size':'half', 'cell_amount':60,'el_no':'131','create_time':str(end),'ai_result': 0, 'ai_defects':{'cr':[[1,1]],'bc':[[1,2],[5,5]]},'ai_time':end,'gui_result':0,'gui_defects':{'cr':[[1,1]],'bc':[[5,5],[6,6]]},'gui_time':end}
#info = { 'barcode':'145', 'cell_type':'mono','cell_size':'half', 'cell_amount':60,'el_no':'131','create_time':str(end),'ai_result': 1, 'ai_defects':{},'ai_time':end,'gui_result':1,'gui_defects':{},'gui_time':end}
info = { 'Barcode':'450'}
time = [1543560351.27383,end]
i = json.dumps(time)
inf = json.dumps(info)

#t = requests.post("http://127.0.0.1:8080/add/panel",inf)
#a = requests.post("http://127.0.0.1:8080/find/barcode",inf)
d = requests.post("http://127.0.0.1:8080/find/defect",i)
#b = requests.post("http://127.0.0.1:8080/find/OK",i)
#c = requests.post("http://127.0.0.1:8080/find/overkillrate",i)
#for i in [a,b,c]:
   # print(i.text)
print(d.text)