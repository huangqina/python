import requests
import json
import time 
import datetime

import threading
import random
import threading

def test(): 
    while(True):
        barcode = random.randint(1,1000)
        ai_d = {}
        gui_d = {}
        for k in ['cr','cs','bc','mr']:
            ai_d[k] = []
            for j in range(random.randint(0,50)):
                l = [random.randint(0,100),random.randint(0,100)]
                ai_d[k].append(l)
        for k in ['cr','cs','bc','mr']:
            gui_d[k] = []
            for i in range(random.randint(0,50)):
                l = [random.randint(0,100),random.randint(0,100)]
                gui_d[k].append(l)

        end = time.time()
        info = { 'barcode':str(barcode), 'cell_type':'mono','cell_size':'half', 'cell_amount':60,'el_no':'131','create_time':end,'ai_result': 1, 'ai_defects':ai_d,'ai_time':end,'gui_result':1,'gui_defects':gui_d,'gui_time':end}

        inf = json.dumps(info)
        t = requests.post("http://127.0.0.1:8080/add/panel",inf)
        print(t.text)
threads = []
t1 = threading.Thread(target=test)
threads.append(t1)
t2 = threading.Thread(target=test)
threads.append(t2)
t3 = threading.Thread(target=test)
threads.append(t3)
t4 = threading.Thread(target=test)
threads.append(t4)
t5 = threading.Thread(target=test)
threads.append(t5)


if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()